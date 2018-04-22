from eift.api.database.news_article_sources import NewsSources
import mysql.connector as db_connection
from eift import settings
import os


def test_get_sources():
    """
    Get sources from db, pass if successful.
    """
    settings.init(os.path.abspath("eift\\configurations\\dev_config_ethan.json"))
    conn = db_connection.connect(**settings.EIFT_ARTICLES_CONNECTION)
    source_list = NewsSources.get_all_sources(conn)
    conn.close()

    pass


def test_insert_sources():
    """
    Attempt to insert new sources, pass if successful, without committing.
    """
    settings.init(os.path.abspath("eift\\configurations\\dev_config_ethan.json"))
    conn = db_connection.connect(**settings.EIFT_ARTICLES_CONNECTION)
    NewsSources.insert_sources(conn)
    conn.close()

    pass


def test_update_sources():
    """
    Attempt to update sources, pass if successful, without committing.
    """
    settings.init(os.path.abspath("eift\\configurations\\dev_config_ethan.json"))
    conn = db_connection.connect(**settings.EIFT_ARTICLES_CONNECTION)
    NewsSources.update_sources(conn)
    conn.close()

    pass


def test_set_sources_inactive():
    """
    Attempt to set sources that no longer exist as inactive. Pass if successful, without committing
    """
    settings.init(os.path.abspath("eift\\configurations\\dev_config_ethan.json"))
    conn = db_connection.connect(**settings.EIFT_ARTICLES_CONNECTION)
    NewsSources.set_sources_inactive(conn)
    conn.close()

    pass
