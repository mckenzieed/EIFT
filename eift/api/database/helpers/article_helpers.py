def build_where_clause(sources, authors, keywords, date_from, date_to):
    where_clause = "WHERE "
    need_where_clause = False
    if sources is not None and isinstance(sources, list):
        need_where_clause = True
        for source in sources:
            where_clause += 'ac.source = %s OR '
        where_clause = where_clause[0:-3] + 'AND '

    if authors is not None and isinstance(sources, list):
        need_where_clause = True
        for author in authors:
            where_clause += 'ac.author = %s OR '
        where_clause = where_clause[0:-3] + 'AND '

    if keywords is not None and isinstance(keywords, list):
        need_where_clause = True
        for keyword in keywords:
            where_clause += 'ac.description LIKE %s OR '
        where_clause = where_clause[0:-3] + 'AND '

    if date_from is not None:
        need_where_clause = True
        where_clause += 'ac.datePublished > %s AND '

    if date_to is not None:
        need_where_clause = True
        where_clause += 'ac.datePublished < %s AND '

    if need_where_clause:
        where_clause = where_clause[0:-5]
    else:
        where_clause = ''

    return where_clause


def get_parameter_object(sources, authors, keywords, date_from, date_to):
    data = []
    if sources is not None and isinstance(sources, list):
        for source in sources:
            data.append(source.name)

    if authors is not None and isinstance(sources, list):
        for author in authors:
            data.append(author)

    if keywords is not None and isinstance(keywords, list):
        for keyword in keywords:
            data.append("%" + keyword + "%")

    if date_from is not None:
        data.append(date_from)

    if date_to is not None:
        data.append(date_to)


    return data