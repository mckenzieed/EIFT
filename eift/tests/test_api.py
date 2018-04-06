import eift.core.get_news_articles
from datetime import datetime, timedelta


def test_get_news_articles():
    """
    As long as this returns something, the test will pass. If something is wrong with the
    url, then response should come back null. No easy way to test this.
    """
    response = eift.core.get_news_articles.get_news_articles('Apple', 'cnn.com, techcrunch.com',
                                                             datetime.strftime(datetime.now() - timedelta(1),
                                                                               '%Y-%m-%d'),
                                                             datetime.today().strftime('%Y-%m-%d'),
                                                             'popularity')

    assert response is not None
