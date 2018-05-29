from eift_core.api.models.article import article, article_source


class ArticleResponse:
    """
    Object representing what is returned when we queue the News API for articles
    """
    def __init__(self, status, articles):
        self.status = status
        self.articles = []
        for (entry) in articles:
            self.articles.append(article.Article(article_source.ArticleSource(entry['source']['id'],
                                                                              entry['source']['name']), entry['author'],
                                                 entry['title'], entry['description'], entry['url'],
                                                 entry['urlToImage'], entry['publishedAt']))
