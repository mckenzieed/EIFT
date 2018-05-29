import mysql.connector as db_connection
from datetime import datetime, timedelta
from eift_core import settings
from eift_core.api.database.news_article_sources import NewsSources
from eift_core.api.database.models import meta_article
from eift_core.news_api import news_api
from eift_core.api.database.helpers import source_helpers
from eift_core.api.database.helpers import article_helpers


class NewsArticles:
    @staticmethod
    def get_news_articles(conn, sources=None, authors=None, keyword=None, date_from=None, date_to=None):
        """
        Returns all news articles in the database

        :returns: A list of all articles returned in the query.
        """

        try:
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
    def _insert_articles(conn):
        """Used to insert initial round of article insertions. Running more than once will result in duplicates."""

        datetime_now = datetime.now()
        last_hour = datetime_now - timedelta(minutes=10)

        api_key = settings.VARIABLES["api_key"]
        source_list = NewsSources.get_all_sources(conn)
        sources_string = source_helpers.get_source_name_list(source_list)
        article_response_list = news_api.get_news_articles_everything(api_key=api_key, date_from=last_hour,
                                                                      date_to=datetime.now(), sources=sources_string,
                                                                      language="en")

        try:
            cursor = conn.cursor()

            query = ("INSERT INTO article_collection "
                     "(source, fk_source_id, author, title, description, url, urlToImage, datePublished) "
                     "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")

            for article_response in article_response_list:
                for article in article_response.articles:
                    # Get the db_id for the source.
                    source_id = [source.db_id for source in source_list if source.name == article.source.name][0]
                    try:
                        cursor.execute(query, (article.source.name, source_id, article.author, article.title,
                                               article.description, article.url, article.url_to_image,
                                               datetime.strptime(article.date_published, "%Y-%m-%dT%H:%M:%SZ")))
                    except db_connection.Error as err:
                        print(err)

            cursor.close()

        except db_connection.Error as err:
            print(err)
