import mysql.connector as db_connection
from eift import settings
from eift.core.models import source
from eift.core.news_api import news_api


class NewsSources:
    @staticmethod
    def get_all_sources():
        """
        Returns all news sources in the database

        Returns:
            A list of all active news sources returned in the query.
        """
        credentials = {
            "user": settings.CONFIG["DBVARIABLES"]["USER"],
            "password": settings.CONFIG["DBVARIABLES"]["PASSWORD"],
            "host": settings.CONFIG["DBVARIABLES"]["HOST"],
            "database": settings.CONFIG["DBVARIABLES"]["DATABASE"]
        }

        try:
            conn = db_connection.connect(**credentials)
            cursor = conn.cursor()

            query = ("SELECT name, description, url, category, language, country, active "
                     "FROM article_sources "
                     "WHERE active = 1 "
                     "ORDER BY id DESC")

            cursor.execute(query)

            source_list = []
            for (source_id, name, description, url, category, language, country, active) in cursor:
                new_source = source.Source(source_id, name, description, url, category,
                                           language, country, active)
                source_list.append(new_source)

            cursor.close()
            conn.close()

            return source_list
        except db_connection.Error:
            print("Something went wrong")

    @staticmethod
    def insert_new_sources():
        """Insert new round of sources (to be ran every so often to keep database updated)"""
        credentials = {
            "user": settings.CONFIG["DBVARIABLES"]["USER"],
            "password": settings.CONFIG["DBVARIABLES"]["PASSWORD"],
            "host": settings.CONFIG["DBVARIABLES"]["HOST"],
            "database": settings.CONFIG["DBVARIABLES"]["DATABASE"]
        }

        source_list_from_api = news_api.get_sources()
        source_list_in_database = NewsSources.get_all_sources()

        try:
            conn = db_connection.connect(credentials)
            cursor = conn.cursor()

            query = ("INSERT INTO article_sources "
                     "(id, source_id, name, description, url, category, language, country, active) "
                     "VALUES (%s, %s, %s, %s, %s, %s, %s, %s")

            for (article_object) in source_list:
                cursor.execute(query, (article_object.source, article_object.author, article_object.title,
                                       article_object.description, article_object.url, article_object.url_to_image,
                                       article_object.date_published))

        except db_connection.Error:
            print("Something went wrong")

    @staticmethod
    def insert_sources():
        """To be ran once to initialize eift_sources table in the eift_articles database"""
        credentials = {
            "user": settings.CONFIG["DBVARIABLES"]["USER"],
            "password": settings.CONFIG["DBVARIABLES"]["PASSWORD"],
            "host": settings.CONFIG["DBVARIABLES"]["HOST"],
            "database": settings.CONFIG["DBVARIABLES"]["DATABASE"]
        }

        news_sources_from_api = news_api.get_sources()

        try:
            conn = db_connection.connect(**credentials)
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
