class Source:
    """A class representing a news source (cnn.com, abcnews.com, etc.)"""

    def __init__(self, source_id, name, description, url, category, language, country, active):
        """
        Initialize an article.

        :param source_id: The id of the source (usually its name).
        :param name: The name of the source (usually not much different from id).
        :param description: A description of the goal of the source.
        :param url: A url linking to the source.
        :param category: The general category of news this source provides.
        :param language: The language this source uses.
        :param country: What country the source is based out of/does news for.
        """
        self.source_id = source_id
        self.name = name
        self.description = description
        self.url = url
        self.category = category
        self.language = language
        self.country = country
        self.active = active
