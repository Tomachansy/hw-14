from flask import Flask, render_template, request
from functions import *

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/movie')
def main_page():
    return render_template('movie.html')


@app.route('/movie/title')
def search_by_title():
    if request.method == 'GET':
        title = request.args.get('title')
        response = []
        if title:
            query = f""" 
                    SELECT  title,
                            country,
                            release_year,
                            listed_in,
                            description
                    FROM    netflix
                    WHERE   type = 'Movie'
                    AND     title 
                    LIKE    '{title}%'
                    ORDER BY release_year DESC
                    LIMIT   1; 
                    """
            result = db_connect('netflix.db', query)
            if len(result):
                response = {"title": result[0][0],
                            "country": result[0][1],
                            "release_year": result[0][2],
                            "listed_in": result[0][3],
                            "description": result[0][4]
                            }
            else:
                return f"<h2>Таких фильмов нет!\n Иди гулять!!!</h2>"
        elif title == "":
            return render_template('movie_title.html', search="Что искать-то?")
        return render_template('movie_title.html', result=response)


@app.route('/movie/year')
def search_by_years():
    if request.method == 'GET':
        _from = request.args.get('from', type=int)
        _to = request.args.get('to', default=_from, type=int)
        response = []
        if _from or _to:
            response = get_year(_from, _to)
            if _from is None:
                _from = 1942
                response = get_year(_from, _to)
        elif _from == "" and _to == "":
            return render_template('movie_year.html')
        return render_template('movie_year.html', result=response)


@app.route('/movie/rating')
def search_by_rating():
    kids_movie = ('TV-Y', 'TV-Y7', 'TV-Y7-FV', 'G', 'TV-G', 'PG', 'TV-PG')
    teens_movie = ('PG-13', 'TV-14')
    adults_movie = ('R', 'TV-MA', 'NC-17')
    not_rated_movie = ('NR', 'UR', '')

    if request.method == 'GET':
        kids = request.args.get('Kids', type=str)
        teens = request.args.get('Teens', type=str)
        adults = request.args.get('Adults', type=str)
        not_rated = request.args.get('Not rated', type=str)
        response = []
        if kids:
            response = get_rating(kids_movie)
        if teens:
            response = get_rating(teens_movie)
        if adults:
            response = get_rating(adults_movie)
        if not_rated:
            response = get_rating(not_rated_movie)
        return render_template('movie_rating.html', result=response)


@app.route('/movie/genre')
def search_by_genre():
    if request.method == 'GET':
        genre = request.args.get('genre')
        response = []
        if genre:
            query = f""" 
                    SELECT  title,
                            listed_in,
                            description
                    FROM    netflix
                    WHERE   type = 'Movie'
                    AND     listed_in
                    LIKE    '{genre}%'
                    ORDER BY release_year DESC
                    LIMIT 10
                    """
            result = db_connect('netflix.db', query)
            if len(result):
                for line in result:
                    response.append({"title": line[0],
                                     "listed_in": line[1],
                                     "description": line[2]})
            else:
                return f"<h2>Чего искал того нет!</h2>"
        elif genre == "":
            return render_template('movie_genre.html', search="Попробуй ввести 'Anime'")
        return render_template('movie_genre.html', result=response)


@app.route('/movie/actors')
def search_by_actors():
    if request.method == 'GET':
        actor_1 = request.args.get('actor_1')
        actor_2 = request.args.get('actor_2')
        if actor_1 and actor_2:
            response = get_actors(actor_1, actor_2)
            if len(response) == 0:
                return render_template('movie_actors.html')
            return render_template('movie_actors.html', result=response, actors=[actor_1, actor_2])
        else:
            return render_template('movie_actors.html')


@app.route('/movie/search')
def search_by_param():
    if request.method == 'GET':
        type = request.args.get('type', type=str)
        release_year = request.args.get('release_year', type=int)
        listed_in = request.args.get('listed_in', type=str)
        response = []
        if type and release_year and listed_in:
            response = get_results(type, release_year, listed_in)
            if len(response) == 0:
                return render_template('movie_search.html')
        return render_template('movie_search.html', result=response)


if __name__ == "__main__":
    app.run(debug=True)
