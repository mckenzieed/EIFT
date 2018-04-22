class ArticleSource:
    """
    Object that represents a source within an article response object.
    """

    def __init__(self, source_id, name):
        """

        :param source_id: Id of source.
        :param name: Name of source.
        """

        self.id = source_id
        self.name = name
