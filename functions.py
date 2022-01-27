import sqlite3


def db_connect(db, query):
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return result


def get_year(_from, _to):
    response = []
    query = f"""
            SELECT  title, 
                    release_year
            FROM    netflix
            WHERE   type = 'Movie'
            AND     release_year 
            BETWEEN '{_from}' AND '{_to}'
            ORDER BY release_year
            LIMIT   100;
            """
    result = db_connect('netflix.db', query)
    for line in result:
        response.append({"title": line[0],
                         "release_year": line[1]})
    return response


def get_rating(rating):
    response = []
    if rating:
        query = f""" 
                SELECT  title, 
                        rating, 
                        description
                FROM    netflix
                WHERE   type = 'Movie'
                AND     rating IN {rating}
                """
        result = db_connect('netflix.db', query)
        for line in result:
            response.append({"title": line[0],
                             "rating": line[1],
                             "description": line[2]})
    return response


def get_actors(actor_1, actor_2):
    response = []
    if actor_1 and actor_2:
        query = f""" 
                SELECT "cast"
                FROM netflix
                WHERE "cast" LIKE '%{actor_1}%'
                AND "cast" LIKE '%{actor_2}%'
                ORDER BY "cast"
                """
        result = db_connect('netflix.db', query)
        result_list = []
        for lines in result:
            for line in lines:
                result_list += (line.split(", "))
        if len(result_list):
            for actor in result_list:
                if result_list.count(actor) > 2:
                    response.append(actor)
                    result_list.remove(actor)
            response.remove(actor_1)
            response.remove(actor_2)
        return response


def get_results(type, release_year, listed_in):
    response = []
    if type and release_year and listed_in:
        query = f"""
                SELECT title, description
                FROM netflix
                WHERE type = '{type}'
                AND release_year = '{release_year}'
                AND listed_in = '{listed_in}'
                """
        result = db_connect('netflix.db', query)
        for line in result:
            response.append({"title": line[0],
                             "description": line[1]})
        return response
