import requests

apiKey = '2b7d70632f0149b4b8e38e5ade0aa88e'


def get_news_articles(keyword, domains, date_from, sort_by):
    url = ('https://newsapi.org/v2/everything?'
           f'q={keyword}&'
           f'domains={domains}'
           f'from={date_from}&'
           f'sort_by={sort_by}&'
           f'apiKey={apiKey}')

    response = requests.get(url)

    return response.json()
