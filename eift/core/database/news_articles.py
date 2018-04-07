import _mysql_connector
from eift import settings


def get_news_articles():
    conn = _mysql_connector.MySQL()

    credentials = {
        "user": settings.CONFIG["DBVARIABLES"]["USER"],
        "password": settings.CONFIG["DBVARIABLES"]["PASSWORD"],
        "host": settings.CONFIG["DBVARIABLES"]["HOST"],
        "database": settings.CONFIG["DBVARIABLES"]["HOST"] 
    }

    conn.connect(**credentials)
