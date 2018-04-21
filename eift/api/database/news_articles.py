import mysql.connector as db_connection
from datetime import datetime, timedelta
from eift import settings
from eift.api.database.news_article_sources import NewsSources
from eift.api.database.models import meta_article
from eift.api.news_api import news_api
from eift.api.database.helpers import source_helpers
from eift.api.database.helpers import article_helpers


class NewsArticles:
    @staticmethod
    def get_news_articles(sources=None, authors=None, keyword=None, date_from=None, date_to=None):
        """
        Returns all news articles in the database

        :returns: A list of all articles returned in the query.
        """

        try:
            conn = db_connection.connect(**settings.EIFT_ARTICLES_CONNECTION)
            cursor = conn.cursor()
            where_clause = article_helpers.build_where_clause(sources, authors, keyword, date_from, date_to)
            parameters = article_helpers.get_parameter_object(sources, authors, keyword, date_from, date_to)

            query = ("SELECT ac.id, ac.source, ac.fk_source_id, ac.author, ac.title, ac.description, ac.url, "
                     "ac.urlToImage, ac.datePublished "
                     "FROM article_collection ac "
                     "JOIN article_sources a on ac.fk_source_id = a.id "
                     + where_clause +
                     "ORDER BY datePublished DESC")

            cursor.execute(query, parameters)

            article_list = []
            for (db_id, source, source_db_id, author, title, description, url, urlToImage, datePublished) in cursor:
                new_meta_article = meta_article.MetaArticle(db_id, source_db_id, source, author, title, description,
                                                            url, urlToImage, datePublished)
                article_list.append(new_meta_article)

            cursor.close()
            conn.close()

            return article_list
        except db_connection.Error as err:
            print(err)

    @staticmethod
    def get_news_articles_from(date_from, date_to):
        """
        Returns all news articles from date_from to date_to

        :param date_from: The start date of the articles to retrieve.
        :param date_to: the end date of the articles to retrieve.

        :returns: A list of articles returned in the query.
        """

        try:
            conn = db_connection.connect(**settings.EIFT_ARTICLES_CONNECTION)
            cursor = conn.cursor()

            query = ("SELECT id, source, author, title, description, url, urlToImage, datePublished "
                     "FROM article_collection "
                     "WHERE datePublished BETWEEN %s AND %s "
                     "ORDER BY datePublished DESC")

            cursor.execute(query, (date_from, date_to))

            article_list = []
            for (db_id, source, author, title, description, url, urlToImage, datePublished) in cursor:
                new_meta_article = meta_article.MetaArticle(db_id, source, author, title, description,
                                                            url, urlToImage, datePublished)
                article_list.append(new_meta_article)

            cursor.close()
            conn.close()

            return article_list
        except db_connection.Error as err:
            print(err)

    @staticmethod
    def get_news_articles_based_on_keyword(keyword):
        """
        Returns all news articles that are based on keyword

        Args:
            keyword: The keyword used to determine what articles to bring back.

        Returns:
            A list of articles returned in the query.
        """

        try:
            conn = db_connection.connect(**settings.EIFT_ARTICLES_CONNECTION)
            cursor = conn.cursor()

            query = ("SELECT id, source, author, title, description, url, urlToImage, datePublished "
                     "FROM article_collection "
                     "WHERE INSTR(title, %s) > 0 "
                     "ORDER BY datePublished DESC")

            cursor.execute(query, keyword)

            article_list = []
            for (db_id, source, author, title, description, url, urlToImage, datePublished) in cursor:
                new_meta_article = meta_article.MetaArticle(db_id, source, author, title, description,
                                                            url, urlToImage, datePublished)
                article_list.append(new_meta_article)

            cursor.close()
            conn.close()

            return article_list
        except db_connection.Error as err:
            print(err)

    @staticmethod
    def insert_articles():
        """Used to insert initial round of article insertions. Running more than once will result in duplicates."""

        datetime_now = datetime.now()
        last_hour = datetime_now - timedelta(minutes=10)

        api_key = settings.VARIABLES["api_key"]
        source_list = NewsSources.get_all_sources()
        sources_string = source_helpers.get_source_name_list(source_list)
        article_response_list = news_api.get_news_articles_everything(api_key=api_key, date_from=last_hour,
                                                                      date_to=datetime.now(), sources=sources_string,
                                                                      language="en")

        try:
            conn = db_connection.connect(**settings.EIFT_ARTICLES_CONNECTION)
            cursor = conn.cursor()

            query = ("INSERT INTO article_collection "
                     "(source, fk_source_id, author, title, description, url, urlToImage, datePublished) "
                     "VALUES (%s, %s, %s, %s, %s, %s, %s)")

            for article_response in article_response_list:
                for article in article_response.articles:
                    source_id = (source for source in source_list if source.name == article.source.name)
                    try:
                        cursor.execute(query, (article.source.name, article.author, article.title,
                                               article.description, article.url, article.url_to_image,
                                               datetime.strptime(article.date_published, "%Y-%m-%dT%H:%M:%SZ")))
                    except db_connection.Error as err:
                        print(err)

            conn.commit()
            cursor.close()
            conn.close()

        except db_connection.Error as err:
            print(err)

    @staticmethod
    def insert_new_articles():
        """Insert new round of sources (to be ran every so often to keep database updated)"""

        source_list_from_api = news_api.get_sources()
        source_list_in_database = NewsSources.get_all_sources()
        sources_to_insert = source_helpers.get_sources_to_insert(source_list_from_api, source_list_in_database)

        try:
            conn = db_connection.connect(**settings.EIFT_ARTICLES_CONNECTION)
            cursor = conn.cursor()

            query = ("INSERT INTO article_sources "
                     "(source_id, name, description, url, category, language, country, active) "
                     "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")

            for source_to_insert in sources_to_insert:
                cursor.execute(query, (source_to_insert.source_id, source_to_insert.name, source_to_insert.description,
                                       source_to_insert.url, source_to_insert.category, source_to_insert.language,
                                       source_to_insert.language, source_to_insert.country, 1))

            conn.commit()
            cursor.close()
            conn.close()

        except db_connection.Error as err:
            print(err)

    @staticmethod
    def update_articles():
        """To be ran once to initialize eift_sources table in the eift_articles database"""

        news_sources_from_api = news_api.get_sources()

        try:
            conn = db_connection.connect(**settings.EIFT_ARTICLES_CONNECTION)
            cursor = conn.cursor()

            query = ("INSERT INTO article_sources "
                     "(source_id, name, description, url, category, language, country, active) "
                     "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")

            for entry in news_sources_from_api.sources:
                new_source = (entry.source_id, entry.name, entry.description, entry.url, entry.category,
                              entry.language, entry.country, entry.active)
                cursor.execute(query, new_source)

            conn.commit()
            cursor.close()
            conn.close()

        except (db_connection.Error, RuntimeError, TypeError, NameError) as err:
            print(err)

    @staticmethod
    def set_article_inactive():
        """Set any article to inactive in case they are revoked by the source."""

        source_list_from_api = news_api.get_sources()
        source_list_in_database = NewsSources.get_all_sources()
        sources_to_set_inactive = source_helpers.get_sources_to_set_inactive(source_list_from_api,
                                                                             source_list_in_database)

        try:
            conn = db_connection.connect(**settings.EIFT_ARTICLES_CONNECTION)
            cursor = conn.cursor()

            query = ("UPDATE article_sources "
                     "SET active = 0 "
                     "WHERE id = %s")

            # The value here has to be a tuple, which is what the weird "," is doing there after the id is inserted
            # into the query. If you don't put that, it comes back as a syntax error. SQL Injection related?
            for source_to_set_inactive in sources_to_set_inactive:
                cursor.execute(query, (source_to_set_inactive,))

            conn.commit()
            cursor.close()
            conn.close()

        except db_connection.Error as err:
            print(err)
