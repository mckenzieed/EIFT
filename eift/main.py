from eift import settings
from eift.api.database import news_articles
from datetime import datetime, timedelta

def main():
    # initialize config
    settings.init("eift\\configurations\\dev_config_ethan.json")

    #response = news_api_delete.get_news_articles_with_keyword("Apple", datetime.now() - timedelta(1), datetime.now(), "popularity")

    #response = news_api_delete.get_sources()

    #response = news_api_delete.get_news_articles(datetime.now() - timedelta(1), datetime.now(), "abcnews.com", "popularity")
    #print(len(response.articles))


    news_articles.NewsArticles.insert_articles()
   # news_articles.NewsArticles.get_news_articles(keyword=['Apple', 'HBO', 'Euro', 'Fox News'])

    # date_time = "2016-05-05T19:05:05Z"
    # parsed = datetime.strptime("%Y-%m")

    #response = news_article_sources.NewsSources.get_all_sources()

    #print(response)


main()
