from eift_core.api.models.source.source import Source


class MetaSource(Source):
    """A class representing a news source (cnn.com, abcnews.com, etc.) from the database"""

    def __init__(self, db_id, source_id, name, description, url, category, language, country, active):
        """
        Initialize an article.

        :param db_id: the id of the source from the database.
        :param source_id: The id of the source (usually its name).
        :param name: The name of the source (usually not much different from id).
        :param description: A description of the goal of the source.
        :param url: A url linking to the source.
        :param category: The general category of news this source provides.
        :param language: The language this source uses.
        :param country: What country the source is based out of/does news for.
        """
        super().__init__(source_id, name, description, url, category, language, country, active)
        self.db_id = db_id

