from flask import Flask, render_template, request, redirect, url_for
import sqlite3



app = Flask(__name__)



def get_db_connection():

    conn = sqlite3.connect('movies.db')

    return conn


@app.route('/', methods=['GET', 'POST'])

def index():
    if request.method == 'POST':
        title = request.form['title']
        return redirect(url_for(index)+f'?query={title}')

    conn = get_db_connection()
    query = request.args.get('query')

    if query:
        
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM movies WHERE title LIKE "{query}"')

        directors_movies = cursor.fetchall()
        print(f"\nMovies from {query}:")

        return render_template('search.html', movie=directors_movies, query=query)


    else:
        movies = conn.execute('SELECT * FROM movies').fetchall()
        return render_template('index.html', movies=movies)
    
    conn.close()
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


@app.route('/search', methods=['GET', 'POST'])

def search_movies():

    query = request.args.get('query', ' ')

    conn = get_db_connection()

    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM movies WHERE title LIKE "{query}"')

    directors_movies = cursor.fetchall()
    print(f"\nMovies from {query}:")

    #movies = conn.execute('Your SQL query here', ('FROM movies WHERE ' + query + ' LIKE',)).fetchall()

    conn.close()

    return render_template('search.html', movie=directors_movies, query=query)


if __name__ == '__main__':

    app.run(debug=True)