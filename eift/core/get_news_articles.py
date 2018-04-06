import requests
from eift import settings


def get_news_articles(keyword, domains, date_from, date_to, sort_by):
    """
    Gets all news articles based on the arguments provided.

    :param keyword: Articles retrieved will be based on this keyword.
    :param domains: Sources to retrieve articles from.
    :param date_from: Articles that were written on or after this date are retrieved.
    :param date_to: Articles that were written on or before this date are retrieved.
    :param sort_by: How articles are sorted. (relevancy, popularity, publishedAt)
    :return: List of articles retrieved in JSON form.
    """

    api_key = settings.CONFIG["VARIABLES"]["API_KEY"]
    url = ('https://newsapi.org/v2/everything?'
           f'q={keyword}&'
           f'domains={domains}'
           f'from={date_from}&'
           f'to={date_to}&'
           f'sort_by={sort_by}&'
           f'apiKey={api_key}')

    response = requests.get(url)

    return response.json()


def get_news_articles_by_language(keyword, domains, date_from, date_to, language, sort_by):
    """
    Gets all news articles based on the arguments provided, including the language.

    :param keyword: Articles retrieved will be based on this keyword.
    :param domains: Sources to retrieve articles from.
    :param date_from: Articles that were written on or after this date are retrieved.
    :param date_to: Articles that were written on or before this date are retrieved.
    :param language: 2-letter ISO-639-1 code for language of articles.
    :param sort_by: How articles are sorted. (relevancy, popularity, publishedAt)
    :return: List of articles retrieved in JSON form.
    """

    api_key = settings.CONFIG["VARIABLES"]["API_KEY"]
    url = ('https://newsapi.org/v2/everything?'
           f'q={keyword}&'
           f'domains={domains}'
           f'from={date_from}&'
           f'to={date_to}&'
           f'language={language}'
           f'sort_by={sort_by}&'
           f'apiKey={api_key}')

    response = requests.get(url)

    return response.json()

