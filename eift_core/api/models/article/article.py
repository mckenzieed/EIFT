class Article:
    """A class representing a new article"""

    def __init__(self, source, author, title, description, url, url_to_image, date_published):
        """
        Initialize an article.

        :param source: Where the article came from.
        :param author: Who wrote the article.
        :param title: The title of the article.
        :param description: A description of the article.
        :param url: A URL that directs to the article.
        :param url_to_image: A URL that directs to the image of the thumbnail for the article.
        :param date_published: The date the article was published.
        """
        self.source = source
        self.author = author
        self.title = title
        self.description = description
        self.url = url
        self.url_to_image = url_to_image
        self.date_published = date_published
