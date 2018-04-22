import mysql.connector as db_connection
from eift import settings
from eift.api.database.models import meta_source
from eift.news_api import news_api
from eift.api.database.helpers import source_helpers


class NewsSources:
    @staticmethod
    def get_all_sources():
        """
        Gets all news sources in the database.

        :returns: A list of all active news sources returned in the query.
        """

        try:
            conn = db_connection.connect(**settings.EIFT_ARTICLES_CONNECTION)
            cursor = conn.cursor()

            query = ("SELECT id, source_id, name, description, url, category, language, country, active "
                     "FROM article_sources "
                     "WHERE active = 1 AND language = 'en' "
                     "ORDER BY source_id")

            cursor.execute(query)

            source_list = []
            for (db_id, source_id, name, description, url, category, language, country, active) in cursor:
                new_meta_source = meta_source.MetaSource(db_id, source_id, name, description, url, category,
                                                         language, country, active)
                source_list.append(new_meta_source)

            cursor.close()
            conn.close()

            return source_list
        except db_connection.Error as err:
            print(err)

    @staticmethod
    def insert_new_sources():
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
    def insert_sources():
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
    def set_sources_inactive():
        """Sets sources that no longer exist as inactive."""

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

    @staticmethod
    def update_sources():
        """Update sources who have information that has changed."""

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
