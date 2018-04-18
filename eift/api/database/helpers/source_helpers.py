

def get_sources_to_insert(source_list_from_api, source_list_in_database):
    """
    Compares a source list from the api and database and finds sources that are in the api, but not the database.
    Those items will then be inserted into the database.

    :param source_list_from_api: Source list that comes from the api query.
    :param source_list_in_database: Source list that comes from the database.
    :return: a list of sources to insert into the database.
    """
    sources_to_insert_list = []
    for db_source in source_list_in_database:
        source_to_insert = None
        value_found = False
        for api_source in source_list_from_api.sources:
            if ((db_source.source_id is not None and db_source.source_id == api_source.source_id)
                    or db_source.name == api_source.name):
                value_found = True
                source_to_insert = api_source

                # Remove from list. Not necessary. I do this only because the two lists are in alphabetical order, so
                # every time this for-loop runs, it will generally only need to run once to find what its looking for.
                # It only won't run once when the two lists are different.
                source_list_from_api.sources.remove(api_source)
                break
        if not value_found:
            sources_to_insert_list.append(source_to_insert)

    return sources_to_insert_list


def get_sources_to_set_inactive(source_list_from_api, source_list_in_database):
    """
    Compares a source list from the api and database and finds sources that are in the database, but not the api.
    Those items will then be set as inactive.

    :param source_list_from_api: Source list that comes from the api query.
    :param source_list_in_database: Source list that comes from the database.
    :return: a list of db_ids of sources to set to inactive in the database.
    """
    sources_to_set_inactive_list = []
    for api_source in source_list_from_api.sources:
        source_to_set_inactive = None
        value_found = False
        for db_source in source_list_in_database:
            if ((db_source.source_id is not None and db_source.source_id == api_source.source_id)
                    or db_source.name == api_source.name):
                value_found = True
                source_to_set_inactive = db_source.db_id

                # Remove from list. Not necessary. I do this only because the two lists are in alphabetical order, so
                # every time this for-loop runs, it will generally only need to run once to find what its looking for.
                # It only won't run once when the two lists are different.
                source_list_in_database.remove(db_source)
                break
        if not value_found:
            sources_to_set_inactive_list.append(source_to_set_inactive)

    return sources_to_set_inactive_list


def get_sources_to_update(source_list_from_api, source_list_in_database):
    """
    Compares a source list from the api and database and finds sources that are in the database, but have changed.

    :param source_list_from_api: Source list that comes from the api query.
    :param source_list_in_database: Source list that comes from the database.
    :return: a list of sources that need to be updated in the database.
    """
    sources_to_update_list = []
    for api_source in source_list_from_api.sources:
        for db_source in source_list_in_database:
            if ((db_source.source_id is not None and db_source.source_id == api_source.source_id)
                    or db_source.name == api_source.name):
                if (db_source.name != api_source.name
                        or db_source.description != api_source.description
                        or db_source.url != api_source.url
                        or db_source.category != api_source.category
                        or db_source.language != api_source.language
                        or db_source.country != api_source.country):
                    sources_to_update_list.append(db_source)
                break

    return sources_to_update_list


def get_source_name_list(list_of_sources):
    source_list_to_return = []
    for source_obj in list_of_sources:
        source_list_to_return.append(source_obj.source_id)

    return ','.join(map(str, source_list_to_return))
