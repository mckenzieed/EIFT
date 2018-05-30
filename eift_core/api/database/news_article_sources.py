import mysql.connector as db_connection
from eift_core import settings
from eift_core.api.database.models import meta_source
from eift_core.news_api import news_api
from eift_core.api.database.helpers import source_helpers


class NewsSources:
    @staticmethod
    def get_all_sources(conn):
        """
        Gets all news sources in the database.

        :returns: A list of all active news sources returned in the query.
        """

        try:
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

            return source_list
        except db_connection.Error as err:
            print(err)

    @staticmethod
    def insert_sources(conn, api_key):
        """Insert new round of sources (to be ran every so often to keep database updated)"""

        source_list_from_api = news_api.get_sources(api_key)
        source_list_in_database = NewsSources.get_all_sources(conn)
        sources_to_insert = source_helpers.get_sources_to_insert(source_list_from_api, source_list_in_database)

        try:
            cursor = conn.cursor()

            query = ("INSERT INTO article_sources "
                     "(source_id, name, description, url, category, language, country, active) "
                     "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")

            for source_to_insert in sources_to_insert:
                cursor.execute(query, (source_to_insert.source_id, source_to_insert.name, source_to_insert.description,
                                       source_to_insert.url, source_to_insert.category, source_to_insert.language,
                                       source_to_insert.language, source_to_insert.country, 1))

            cursor.close()

        except db_connection.Error as err:
            print(err)


    @staticmethod
    def set_sources_inactive(conn, api_key):
        """Sets sources that no longer exist as inactive."""

        source_list_from_api = news_api.get_sources(api_key)
        source_list_in_database = NewsSources.get_all_sources(conn)
        sources_to_set_inactive = source_helpers.get_sources_to_set_inactive(source_list_from_api,
                                                                             source_list_in_database)

        try:
            cursor = conn.cursor()

            query = ("UPDATE article_sources "
                     "SET active = 0 "
                     "WHERE id = %s")

            # The value here has to be a tuple, which is what the weird "," is doing there after the id is inserted
            # into the query. If you don't put that, it comes back as a syntax error. SQL Injection related?
            for source_to_set_inactive in sources_to_set_inactive:
                cursor.execute(query, (source_to_set_inactive,))

            cursor.close()

        except db_connection.Error as err:
            print(err)

    @staticmethod
    def update_sources(conn, api_key):
        """Update sources who have information that has changed."""

        source_list_from_api = news_api.get_sources(api_key)
        source_list_in_database = NewsSources.get_all_sources(conn)
        sources_to_update = source_helpers.get_sources_to_update(source_list_from_api, source_list_in_database)

        try:
            cursor = conn.cursor()

            query = ("UPDATE article_sources "
                     "SET source_id = %s, name = %s, description = %s, "
                     "url = %s, category = %s, language = %s, country = %s "
                     "WHERE id = %s")

            for source_to_update in sources_to_update:
                cursor.execute(query, (source_to_update.source_id, source_to_update.name, source_to_update.description,
                                       source_to_update.url, source_to_update.category, source_to_update.language,
                                       source_to_update.country, sources_to_update.db_id))

            cursor.close()

        except db_connection.Error as err:
            print(err)
