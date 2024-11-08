from flask import Flask, request, jsonify
import mysql.connector
import os
import json

app = Flask(__name__)

path = "/hexagontv/password.txt"

with open(path, 'r') as file:
    configPassword = file.readline().strip()

mydb = mysql.connector.connect(
    host="localhost",
    user="hexagon",
    password=configPassword,
    database="hexagonMoviedb"
)

db = mydb.cursor()

db.execute("CREATE TABLE IF NOT EXISTS movies (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255) NOT NULL, description TEXT, thumbnailURL VARCHAR(255), videoURL VARCHAR(255), date DATE, urlName VARCHAR(255) UNIQUE, rating VARCHAR(10), category VARCHAR(50));")
db.execute("CREATE TABLE IF NOT EXISTS tvshows (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255) NOT NULL, description TEXT, thumbnailURL VARCHAR(255), videoURL VARCHAR(255), date DATE, urlName VARCHAR(255) UNIQUE, rating VARCHAR(10), category VARCHAR(50));")
db.execute("CREATE TABLE IF NOT EXISTS documentaries (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255) NOT NULL, description TEXT, thumbnailURL VARCHAR(255), videoURL VARCHAR(255), date DATE, urlName VARCHAR(255) UNIQUE, rating VARCHAR(10), category VARCHAR(50));")
def loadData(tableName):
    query = f"SELECT * FROM {tableName}"
    db.execute(query)
    result = db.fetchall()
    column_names = [desc[0] for desc in db.description]
    data = []
    for row in result:
        row_data = {column_names[i]: row[i] for i in range(len(row))}
        row_data['id'] = str(row_data['id'])
        row_data['rating'] = str(row_data['rating'])
        data.append(row_data)
    return data

def setCorsHeaders(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    return response

movies = loadData('movies')
tvshows = loadData('tvshows')
documentaries = loadData('documentaries')

@app.route('/movies', methods=['GET'])
def getMovies():
    return setCorsHeaders(jsonify(movies))

@app.route('/tvshows', methods=['GET'])
def getTVShows():
    return setCorsHeaders(jsonify(tvshows))

@app.route('/documentaries', methods=['GET'])
def getDocumentaries():
    return setCorsHeaders(jsonify(documentaries))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
