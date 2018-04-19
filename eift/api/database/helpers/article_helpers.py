def build_where_clause(sources, authors, keywords, date_from, date_to):
    where_clause = "WHERE "
    arguments_used = []
    if sources is not None and isinstance(sources, list):
        arguments_used.append("sources")
        for source in sources:
            where_clause += 'source LIKE %s OR '
        where_clause += 'AND '

    if authors is not None and isinstance(sources, list):
        arguments_used.append("authors")
        for author in authors:
            where_clause += 'author LIKE %s OR '
        where_clause += 'AND '

    if keywords is not None and isinstance(keywords, list):
        arguments_used.append("keywords")
        for keyword in keywords:
            where_clause += 'description LIKE %s OR '
        where_clause += 'AND '

    if date_from is not None:
        arguments_used.append("date_from")
        where_clause += 'datePublished > %s AND '

    if date_to is not None:
        arguments_used.append("date_to")
        where_clause += 'datePublished < %s AND '

    if arguments_used.__len__() > 0:
        where_clause = where_clause[0:where_clause.__len__()-5]
    else:
        where_clause = ''

    return [where_clause, arguments_used]


def get_parameter_object(sources, authors, keywords, date_from, date_to):
    data = []
    if sources is not None and isinstance(sources, list):
        for source in sources:
            data.append(source.name)

    if authors is not None and isinstance(sources, list):
        for author in authors:
            data.append(au)

    if keywords is not None and isinstance(keywords, list):
        for keyword in keywords:
            where_clause += 'description LIKE %s OR '
        where_clause += 'AND '

    if date_from is not None:
        where_clause += 'datePublished > %s AND '

    if date_to is not None:
        where_clause += 'datePublished < %s AND '

    if arguments_used.__len__() > 0:
        where_clause = where_clause[0:where_clause.__len__() - 5]
    else:
        where_clause = ''

    return [where_clause, arguments_used]