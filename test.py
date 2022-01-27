from collections import Counter

from functions import *


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
        for actor in result_list:
            if result_list.count(actor) > 2:
                response.append(actor)
                result_list.remove(actor)
    return response


# get_actors('Jack Black', 'Dustin Hoffman')
# print(type(get_actors('Jack Black', 'Dustin Hoffman')))
print(get_actors('Jack Black', 'Dustin Hoffman'))
