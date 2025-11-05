from flask import Flask, render_template, request, redirect, url_for
import sqlite3



app = Flask(__name__)



def get_db_connection():

    conn = sqlite3.connect('movies.db')

    return conn


@app.route('/')

def index():

    conn = get_db_connection()

    movies = conn.execute('SELECT * FROM movies').fetchall()

    conn.close()

    return render_template('index.html', movies=movies)

@app.route('/add', methods=['GET', 'POST'])

def add_movie():
    # On a form submission (POST)

    if request.method == 'POST':

        title = request.form['title']

        director = request.form['director']

        year = int(request.form['year'])

        rating = float(request.form['rating'])

        

        conn = get_db_connection()

        conn.execute('INSERT INTO movies (title, director, year, rating) VALUES (?, ?, ?, ?)',

                     (title, director, year, rating))

        conn.commit()

        conn.close()

        return redirect(url_for('index'))

    
    # On visiting the page (GET)

    return render_template('add.html')


@app.route('/search')

def search_movies():

    query = request.args.get('query', '')

    conn = get_db_connection()

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()
    cursor.execute(f'SELECT title, year FROM movies WHERE director = "{query}"')

    directors_movies = cursor.fetchall()

    print(f"\nMovies from {query}:")

    for movie in directors_movies:

        print(f"{movie[0]} ({movie[1]})")

    movies = conn.execute('Your SQL query here', ('%' + query + '%',)).fetchall()

    conn.close()

    return render_template('search.html', movies=movies, query=query)


if __name__ == '__main__':

    app.run(debug=True)