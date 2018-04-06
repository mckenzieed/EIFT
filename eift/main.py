import eift.core.get_news_articles
from datetime import datetime, timedelta
from eift import settings


def main():
    # initialize config
    settings.init()

    response = eift.core.get_news_articles.get_news_articles('Apple', 'cnn.com, techcrunch.com',
                                                             datetime.strftime(datetime.now() - timedelta(1),
                                                                               '%Y-%m-%d'),
                                                             datetime.today().strftime('%Y-%m-%d'),
                                                             'popularity')
    print(response['articles'])


main()
