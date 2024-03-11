import sqlite3
from flask import Flask, request, jsonify
from flasgger import Swagger

app = Flask(__name__)
Swagger(app)  # Initialize Flasgger for Swagger documentation

DATABASE_NAME = 'jokes.db'


def get_connection_db():
    """Creates a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE_NAME)
    return conn


def create_table():
    """Creates the jokes table if it doesn't exist."""
    conn = get_connection_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jokes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            joke TEXT NOT NULL,
            category TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def create_joke(joke, category):
    """Adds a new joke to the database."""
    conn = get_connection_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO jokes (joke, category) VALUES (?, ?)", (joke, category))
    conn.commit()
    conn.close()


def get_joke(category):
    """Retrieves a random joke from the specified category."""
    conn = get_connection_db()
    cursor = conn.cursor()
    cursor.execute("SELECT joke FROM jokes WHERE category = ? ORDER BY RANDOM() LIMIT 1", (category,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None


@app.route('/jokes', methods=['POST'])
def add_joke():
    """
    Adds a new joke to the database.
    ---
    parameters:
      - name: joke
        in: body
        type: string
        required: true
      - name: category
        in: body
        type: string
        required: true
        example: {"joke":"enter joke here",
            "category": "Chuck Norris" }
    responses:
      200:
        description: Joke added successfully
      400:
        description: Missing or invalid parameters
    """
    data = request.get_json()
    print(data)
    joke = data['joke']
    category = data['category']
    if not joke or not category:
        return jsonify({'error': 'Missing joke or category'}), 400

    create_joke(joke, category)
    return jsonify({'message': 'Joke added successfully'}), 200


@app.route('/jokes/<category>', methods=['GET'])
def get_random_joke(category):
    """
    Retrieves a random joke from the specified category.
    ---
    parameters:
      - name: category
        in: path
        type: string
        required: true
        description: The category of the joke (Chuck Norris, Your Momma)
        example: { "category": "Chuck Norris"}
    responses:
      200:
        description: A random joke from the category
        schema:
          type: object
          properties:
            joke:
              type: string
      404:
        description: No jokes found in the category
    """
    joke = get_joke(category)
    if joke:
        return jsonify({'joke': joke})
    else:
        return jsonify({'error': 'No jokes found in that category'}), 404


if __name__ == '__main__':
    create_table()  # Ensure the table exists
    app.run(debug=True, port=8088)