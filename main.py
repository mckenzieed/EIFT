import api.eift_api
import datetime


def main():
    response = api.eift_api.get_news_articles('Apple', 'cnn.com, techcrunch.com', datetime.datetime.today().strftime('%Y-%m-%d'),
                                   'popularity')
    print(response.articles)


main()
