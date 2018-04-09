from eift.core.models import source


class SourceResponse:
    def __init__(self, status, sources):
        self.status = status
        self.sources = []
        for(entry) in sources:
            self.sources.append(source.Source(entry['id'], entry['name'], entry['description'], entry['url'],
                                              entry['category'], entry['language'], entry['country'], 1))
