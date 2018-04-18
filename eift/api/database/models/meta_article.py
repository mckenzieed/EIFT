from eift.api.models.article.article import Article


class MetaArticle(Article):
    """A class representing an article from the database"""

    def __init__(self, db_id, source, author, title, description, url, url_to_image, date_published):
        """
        Initialize an article.

        :param db_id: Database id of article.
        """
        super().__init__(source, author, title, description, url, url_to_image, date_published)
        self.db_id = db_id
