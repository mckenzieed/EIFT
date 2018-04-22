import eift.news_api.news_api as news_api
from datetime import datetime, timedelta
from eift import settings
import os


def test_get_news_articles():
    """
    We want this to return a status of "ok" so that we know the query was successful
    """
    settings.init(os.path.abspath("eift\\dev_config.json"))

    response = news_api.get_news_articles('Apple',
                                          datetime.strftime(datetime.now() - timedelta(1),
                                                            '%Y-%m-%d'),
                                          datetime.today().strftime('%Y-%m-%d'),
                                          'popularity')

    assert response['status'] == 'ok'
