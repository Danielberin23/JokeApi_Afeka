from flask import Flask,request,redirect,jsonify
from flasgger import Swagger
import sqlite3

app = Flask(__name__)
swagger = Swagger(app)


def get_db_connection():
    connection = sqlite3.connect('Jokes.db')
    connection.row_factory = sqlite3.Row
    return connection


def create_table():
    connection = get_db_connection()
    connection.execute('''CREATE TABLE IF NOT EXISTS ChuckNoris(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        joke TEXT NOT NULL)''')
    connection.commit()
    connection.execute('''CREATE TABLE IF NOT EXISTS YourMomma(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            joke TEXT NOT NULL)''')
    connection.commit()
    connection.close()


@app.route('/joke',methods=['POST'])
def create_joke(category,joke):
    joke = request.json['joke']
    db_connection = get_db_connection()

    return jsonify({'category':})


if __name__ == '__main__':
    app.run(debug=True, port=8088)

