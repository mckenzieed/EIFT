import requests
from eift import settings
from eift.core.models.source import source_response
from eift.core.models.article import article_response


def get_news_articles(date_from, date_to, sort_by):
    """
    Gets all news articles based on the arguments provided.

    :param date_from: Articles that were written on or after this date are retrieved.
    :param date_to: Articles that were written on or before this date are retrieved.
    :param sort_by: How articles are sorted. (relevancy, popularity, publishedAt)
    :return: List of articles retrieved in JSON form.
    """

    api_key = settings.CONFIG["VARIABLES"]["API_KEY"]
    url = ('https://newsapi.org/v2/everything?'
           f'from={date_from}&'
           f'to={date_to}&'
           f'sort_by={sort_by}&'
           f'apiKey={api_key}')

    response = requests.get(url).json()
    new_articles_response = article_response.ArticleResponse(response['status'], response['articles'])

    return new_articles_response


def get_news_articles_with_keyword(keyword, date_from, date_to, sort_by):
    """
    Gets all news articles based on the arguments provided.

    :param keyword: Articles retrieved will be based on this keyword.
    :param date_from: Articles that were written on or after this date are retrieved.
    :param date_to: Articles that were written on or before this date are retrieved.
    :param sort_by: How articles are sorted. (relevancy, popularity, publishedAt)
    :return: List of articles retrieved in JSON form.
    """

    api_key = settings.CONFIG["VARIABLES"]["API_KEY"]
    url = ('https://newsapi.org/v2/everything?'
           f'q={keyword}&'
           f'from={date_from}&'
           f'to={date_to}&'
           f'sort_by={sort_by}&'
           f'apiKey={api_key}')

    response = requests.get(url).json()
    new_articles_response = article_response.ArticleResponse(response['status'], response['articles'])

    return new_articles_response


def get_news_articles_by_domains(keyword, domains, date_from, date_to, sort_by):
    """
    Gets all news articles based on the arguments provided.

    :param keyword: Articles retrieved will be based on this keyword.
    :param domains: Sources to retrieve articles from.
    :param date_from: Articles that were written on or after this date are retrieved.
    :param date_to: Articles that were written on or before this date are retrieved.
    :param sort_by: How articles are sorted. (relevancy, popularity, publishedAt)
    :return: List of articles retrieved in JSON form.
    """

    api_key = settings.VARIABLES["api_key"]
    url = ('https://newsapi.org/v2/everything?'
           f'q={keyword}&'
           f'domains={domains}'
           f'from={date_from}&'
           f'to={date_to}&'
           f'sort_by={sort_by}&'
           f'apiKey={api_key}')

    response = requests.get(url).json()
    new_articles_response = article_response.ArticleResponse(response['status'], response['articles'])

    return new_articles_response


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

    api_key = settings.VARIABLES["api_key"]
    url = ('https://newsapi.org/v2/sources?'
           f'q={keyword}&'
           f'domains={domains}'
           f'from={date_from}&'
           f'to={date_to}&'
           f'language={language}'
           f'sort_by={sort_by}&'
           f'apiKey={api_key}')

    response = requests.get(url).json()
    new_articles_response = article_response.ArticleResponse(response['status'], response['articles'])

    return new_articles_response


def get_sources():
    """
        Gets all news articles based on the arguments provided, including the language.

        :return: List of sources retrieved in JSON form.
    """

    api_key = settings.VARIABLES["api_key"]
    url = ('https://newsapi.org/v2/sources?'
           f'language=en&'
           f'apiKey={api_key}')

    response = requests.get(url).json()
    new_source_response = source_response.SourceResponse(response['status'], response['sources'])

    return new_source_response
