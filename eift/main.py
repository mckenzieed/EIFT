from eift import settings
from eift.api.database import news_articles


def main():
    # initialize config
    settings.init("eift\\dev_config.json")

    #response = news_api.get_news_articles_with_keyword("Apple", datetime.now() - timedelta(1), datetime.now(), "popularity")

    #response = news_api.get_sources()

    #response = news_api.get_news_articles(datetime.now() - timedelta(1), datetime.now(), "abcnews.com", "popularity")
    #print(len(response.articles))


    news_articles.NewsArticles.insert_articles()

    # date_time = "2016-05-05T19:05:05Z"
    # parsed = datetime.strptime("%Y-%m")

    #response = news_article_sources.NewsSources.get_all_sources()

    #print(response)


main()
