import mysql.connector as db_connection
from datetime import datetime, timedelta
from eift import settings
from eift.core.models import article
from eift.core.news_api import news_api


class NewsArticles:
    @staticmethod
    def get_all_news_articles():
        """
        Returns all news articles in the database

        Returns:
            A list of all articles returned in the query.
        """
        credentials = {
            "user": settings.CONFIG["DBVARIABLES"]["USER"],
            "password": settings.CONFIG["DBVARIABLES"]["PASSWORD"],
            "host": settings.CONFIG["DBVARIABLES"]["HOST"],
            "database": settings.CONFIG["DBVARIABLES"]["DATABASE"]
        }

        try:
            conn = db_connection.connect(credentials)
            cursor = conn.cursor()

            query = ("SELECT source, author, title, description, url, urlToImage, datePublished "
                     "FROM article_collection "
                     "ORDER BY datePublished DESC")

            cursor.execute(query)

            article_list = []
            for (source, author, title, description, url, urlToImage, datePublished) in cursor:
                new_article = article.Article(source, author, title, description, url, urlToImage, datePublished)
                article_list.append(new_article)

            cursor.close()
            conn.close()

            return article_list
        except db_connection.Error:
            print("Something went wrong")


    @staticmethod
    def get_news_articles_from(date_from, date_to):
        """
        Returns all news articles from date_from to date_to

        Args:
            date_from: The start date of the articles to retrieve.
            date_to: the end date of the articles to retrieve.

        Returns:
            A list of articles returned in the query.
        """

        credentials = {
            "user": settings.CONFIG["DBVARIABLES"]["USER"],
            "password": settings.CONFIG["DBVARIABLES"]["PASSWORD"],
            "host": settings.CONFIG["DBVARIABLES"]["HOST"],
            "database": settings.CONFIG["DBVARIABLES"]["DATABASE"]
        }

        try:
            conn = db_connection.connect(credentials)
            cursor = conn.cursor()

            query = ("SELECT source, author, title, description, url, urlToImage, datePublished "
                     "FROM article_collection "
                     "WHERE datePublished BETWEEN %s AND %s "
                     "ORDER BY datePublished DESC")

            cursor.execute(query, (date_from, date_to))

            article_list = []
            for (source, author, title, description, url, urlToImage, datePublished) in cursor:
                new_article = article.Article(source, author, title, description, url, urlToImage, datePublished)
                article_list.append(new_article)

            cursor.close()
            conn.close()

            return article_list
        except db_connection.Error:
            print("Something went wrong")

    @staticmethod
    def get_news_articles_based_on_keyword(keyword):
        """
        Returns all news articles that are based on keyword

        Args:
            keyword: The keyword used to determine what articles to bring back.

        Returns:
            A list of articles returned in the query.
        """

        credentials = {
            "user": settings.CONFIG["DBVARIABLES"]["USER"],
            "password": settings.CONFIG["DBVARIABLES"]["PASSWORD"],
            "host": settings.CONFIG["DBVARIABLES"]["HOST"],
            "database": settings.CONFIG["DBVARIABLES"]["DATABASE"]
        }

        try:
            conn = db_connection.connect(credentials)
            cursor = conn.cursor()

            query = ("SELECT source, author, title, description, url, urlToImage, datePublished "
                     "FROM article_collection "
                     "WHERE INSTR(title, %s) > 0 "
                     "ORDER BY datePublished DESC")

            cursor.execute(query, keyword)

            article_list = []
            for (source, author, title, description, url, urlToImage, datePublished) in cursor:
                new_article = article.Article(source, author, title, description, url, urlToImage, datePublished)
                article_list.append(new_article)

            cursor.close()
            conn.close()

            return article_list
        except db_connection.Error:
            print("Something went wrong")

    @staticmethod
    def insert_articles():
        """Insert new round of articles (to be ran every so often to keep database updated)"""
        credentials = {
            "user": settings.CONFIG["DBVARIABLES"]["USER"],
            "password": settings.CONFIG["DBVARIABLES"]["PASSWORD"],
            "host": settings.CONFIG["DBVARIABLES"]["HOST"],
            "database": settings.CONFIG["DBVARIABLES"]["DATABASE"]
        }

        datetime_now = datetime.now()
        last_hour = datetime_now - timedelta(hours=1)

        article_list = news_api.get_news_articles(last_hour, datetime_now, "publishedAt")

        try:
            conn = db_connection.connect(credentials)
            cursor = conn.cursor()

            query = ("INSERT INTO article_collection "
                     "(source, author, title, description, url, urlToImage, datePublished) "
                     "VALUES (%s, %s, %s, %s, %s, %s, %s, %s")

            for (article_object) in article_list:
                cursor.execute(query, (article_object.source, article_object.author, article_object.title,
                                       article_object.description, article_object.url, article_object.url_to_image,
                                       article_object.date_published))

            conn.commit()
            cursor.close()
            conn.close()

        except db_connection.Error:
            print("Something went wrong")