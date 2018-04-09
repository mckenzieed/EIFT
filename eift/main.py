import eift.core.news_api.news_api
from datetime import datetime, timedelta
from eift import settings
import eift.core.database as db_api
from eift.core.news_api import news_api
from eift.core.database import news_article_sources


def main():
    # initialize config
    settings.init("eift\\dev_config.json")

    #response = news_api.get_news_articles_with_keyword("Apple", datetime.now() - timedelta(1), datetime.now(), "popularity")

    #response = news_api.get_sources()

    news_article_sources.NewsSources.insert_sources()

    #print(response.articles[0].source['name'])


main()
