from eift.api.database.news_articles import NewsArticles
import mysql.connector as db_connection
from datetime import datetime, timedelta
from eift import settings
import os


def test_get_news_articles():
    """
    We want this to return a list of articles successfully.
    """
    settings.init(os.path.abspath("eift\\configurations\\dev_config_ethan.json"))
    conn = db_connection.connect(**settings.EIFT_ARTICLES_CONNECTION)

    article_list = NewsArticles.get_news_articles(conn, keyword=['Apple', 'HBO', 'Euro', 'Fox News'],
                                                                date_from=datetime.now() - timedelta(minutes=10),
                                                                date_to=datetime.now())
    conn.close()
    pass


def test_insert_articles():
    """
    Attempt to insert new articles into database, pass if successful, but without committing.
    """
    settings.init(os.path.abspath("eift\\configurations\\dev_config_ethan.json"))
    conn = db_connection.connect(**settings.EIFT_ARTICLES_CONNECTION)
    NewsArticles.insert_articles(conn)
    conn.close()

    # Pass if we successfully hit this point without breaking.
    pass

