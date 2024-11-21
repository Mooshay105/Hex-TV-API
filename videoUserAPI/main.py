from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

debug = True
configPath = "/hexagontv/password.txt"

def getDbConnection():
	try:
		with open(configPath, 'r') as file:
			dbPassword = file.readline().strip()
	except FileNotFoundError:
		raise RuntimeError(f"Configuration file not found at {configPath}")

	try:
		return mysql.connector.connect(
			host="localhost",
			user="hexagon",
			password=dbPassword,
			database="hexagonUsersInfodb"
		)
	except mysql.connector.Error as err:
		raise RuntimeError(f"Database connection failed: {err}")

@app.route('/getWatchlist', methods=['GET'])
def getWatchlist():
	username = request.args.get('username')

	if not username:
		return jsonify({"error": "Missing username parameter"}), 400

	connection = getDbConnection()
	cursor = connection.cursor(dictionary=True)

	try:
		query = """
		SELECT username, name, urlName, thumbnailURL 
		FROM watchlist 
		WHERE username = %s
		"""
		cursor.execute(query, (username,))
		results = cursor.fetchall()
		response = results if results else []
	except Exception as e:
		response = {"error": str(e)} if debug else {"error": "Internal server error"}
	finally:
		cursor.close()
		connection.close()

	return jsonify(response)

@app.route('/addToWatchlist', methods=['POST'])
def addToWatchlist():
	name = request.json.get('name')
	urlName = request.json.get('urlName')
	thumbnailUrl = request.json.get('thumbnailURL')
	username = request.json.get('username')

	if not all([name, urlName, thumbnailUrl, username]):
		return jsonify({"error": "Missing required parameters"}), 400

	connection = getDbConnection()
	cursor = connection.cursor()

	try:
		query = """
		INSERT INTO watchlist (username, name, urlName, thumbnailURL)
		VALUES (%s, %s, %s, %s)
		"""
		cursor.execute(query, (username, name, urlName, thumbnailUrl))
		connection.commit()
		response = {"message": "Data inserted successfully"}
	except mysql.connector.IntegrityError:
		response = {"error": "Entry already exists"}
		return jsonify(response)
	except Exception as e:
		response = {"error": str(e)} if debug else {"error": "Internal server error"}
		return jsonify(response)
	finally:
		cursor.close()
		connection.close()

	return jsonify(response)

@app.route('/removeFromWatchlist', methods=['DELETE'])
def removeFromWatchlist():
	urlName = request.json.get('urlName')
	username = request.json.get('username')

	if not urlName or not username:
		return jsonify({"error": "Missing required parameters"})

	connection = getDbConnection()
	cursor = connection.cursor()

	try:
		query = """
		DELETE FROM watchlist
		WHERE urlName = %s AND username = %s
		"""
		cursor.execute(query, (urlName, username))
		connection.commit()
		response = {"message": "Data removed successfully"}
	except Exception as e:
		response = {"error": str(e)} if debug else {"error": "Internal server error"}
		return jsonify(response)
	finally:
		cursor.close()
		connection.close()

	return jsonify(response)

@app.route('/getContinueWatching', methods=['GET'])
def getContinueWatching():
	username = request.args.get('username')

	if not username:
		return jsonify({"error": "Missing username parameter"}), 400

	connection = getDbConnection()
	cursor = connection.cursor(dictionary=True)

	try:
		query = """
		SELECT username, name, urlName, thumbnailURL 
		FROM continueWatching 
		WHERE username = %s
		"""
		cursor.execute(query, (username,))
		results = cursor.fetchall()
		response = results if results else []
	except Exception as e:
		response = {"error": str(e)} if debug else {"error": "Internal server error"}
	finally:
		cursor.close()
		connection.close()

	return jsonify(response)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8070)
