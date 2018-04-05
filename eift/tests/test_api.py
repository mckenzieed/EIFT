import eift.api.eift_api
from datetime import datetime, timedelta


def test_get_news_articles():
    response = eift.api.eift_api.get_news_articles('Apple', 'cnn.com, techcrunch.com',
                                                   datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d'),
                                                   datetime.today().strftime('%Y-%m-%d'),
                                                   'popularity')

    assert response is not None

