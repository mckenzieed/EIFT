import requests
import json
from eift import settings
from eift.core.database.news_article_sources import NewsSources
from eift.core.models.source import source_response
from eift.core.models.article import article_response


def get_news_articles_everything(api_key, keyword=None, sources=None, domains=None, date_from=None, date_to=None,
                                 language=None, sort_by=None, page_size=None, page=None):
    """
    Gets all news articles based on the arguments provided.

    :param api_key: Required to query.
    :param keyword: Used to determine keywords to look for in articles.
    :param sources: Only bring back articles with sources that are in this list.
    :param domains: Only bring back articles with sources that have domains in this list.
    :param date_from: Articles that were written on or after this date are retrieved.
    :param date_to: Articles that were written on or before this date are retrieved.
    :param language: Only bring back articles defined with this language.
    :param sort_by: How articles are sorted. (relevancy, popularity, publishedAt)
    :param page_size: How many pages of articles to bring back. Default is 20, max is 100.
    :param page: Which page of the 1-100 page_size pages to bring back.

    :return: List of articles retrieved in JSON form.
    """

    # Build the initial url.
    url = build_url(api_key, keyword, sources, domains, date_from, date_to, language, sort_by, page_size, page)

    response = requests.get(url).json()
    total_results = response['totalResults']
    article_list = [response['articles']]
    page += 1
    num_pages = total_results / 100
    while page < num_pages:
        # Rebuild the url with the new page size.
        url = build_url(api_key, keyword, sources, domains, date_from, date_to, language, sort_by, page_size, page)
        response = requests.get(url).json()
        article_list.append(response['articles'])
        page += 1

    new_articles_response_list = []
    for articles in article_list:
        new_articles_response_list.append(article_response.ArticleResponse(response['status'], articles))

    return new_articles_response_list


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


def build_url(api_key, keyword=None, sources=None, domains=None, date_from=None, date_to=None,
              language=None, sort_by=None, page_size=None, page=None):
    """
    Create a url string based on the arguments provided.

    :param api_key: Required to query.
    :param keyword: Used to determine keywords to look for in articles.
    :param sources: Only bring back articles with sources that are in this list.
    :param domains: Only bring back articles with sources that have domains in this list.
    :param date_from: Articles that were written on or after this date are retrieved.
    :param date_to: Articles that were written on or before this date are retrieved.
    :param language: Only bring back articles defined with this language.
    :param sort_by: How articles are sorted. (relevancy, popularity, publishedAt)
    :param page_size: How many pages of articles to bring back. Default is 20, max is 100.
    :param page: Which page of the 1-100 page_size pages to bring back.

    :return: List of articles retrieved in JSON form.
    """

    url = f'https://newsapi.org/v2/everything?'

    if keyword is not None:
        url += f'q={keyword}&'
    if sources is not None:
        url += f'sources={sources}&'
    if domains is not None:
        url += f'domains={domains}&'
    if date_from is not None and date_to is not None:
        url += f'from={date_from}&'
        url += f'to={date_to}&'
    elif date_from is not None:
        print("Please supply a 'date_to' argument if 'date_from' is supplied.")
    elif date_to is not None:
        print("Please supply a 'date_from' argument if 'date_to' is supplied.")
    if language is not None:
        url += f'language={language}&'
    if sort_by is not None:
        url += f'sortBy={sort_by}&'
    if page_size is not None:
        url += f'pageSize={page_size}&'
    if page is not None:
        url += f'page={page}&'

    url += f'apiKey={api_key}'

    return url
