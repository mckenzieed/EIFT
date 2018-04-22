from eift.api.models.article.article import Article


class MetaArticle(Article):
    """A class representing an article from the database"""

    def __init__(self, db_id, source_db_id, source, author, title, description, url, url_to_image, date_published):
        """
        Initialize an article with database variables.

        :param db_id: Database id of article.
        :param source: Where the article came from.
        :param author: Who wrote the article.
        :param title: The title of the article.
        :param description: A description of the article.
        :param url: A URL that directs to the article.
        :param url_to_image: A URL that directs to the image of the thumbnail for the article.
        :param date_published: The date the article was published.
        """
        super().__init__(source, author, title, description, url, url_to_image, date_published)
        self.db_id = db_id
        self.source_db_id = source_db_id
