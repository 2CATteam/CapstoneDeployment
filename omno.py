from flask import Flask, request, jsonify, make_response
app = Flask(__name__, static_url_path="/static", static_folder="static")
import sqlite3
import secrets
from passlib.hash import sha256_crypt

user_db = '/home/ubuntu/capstone/users.db'
data_db = '/home/ubuntu/capstone/data.db'

user_tokens = []
admin_tokens = []

@app.route('/login', methods=['POST'])
def generateToken():
	username = request.form.get("username")
	password = request.form.get("password")
	users_conn = sqlite3.connect(user_db)
	users_conn.row_factory = sqlite3.Row
	cur = users_conn.cursor()
	cur.execute("SELECT * FROM admins WHERE username = ?", (username,))
	results = cur.fetchall()
	if (len(results) == 1):
		if (sha256_crypt.verify(password, results[0]["password"])):
			token = secrets.token_urlsafe(32)
			toAdd = {}
			toAdd["user"] = results[0]["username"]
			toAdd["token"] = token
			admin_tokens.append(toAdd)
			res = make_response("Logged in as admin", 200)
			res.set_cookie("token", token)
			return res

	cur.execute("SELECT * FROM users WHERE username = ?", (username,))
	results = cur.fetchall()
	if (len(results) == 1):
		if (sha256_crypt.verify(password, results[0]["password"])):
			token = secrets.token_urlsafe(32)
			toAdd = {}
			toAdd["user"] = results[0]["username"]
			toAdd["token"] = token
			toAdd["hospital"] = results[0]["hospital"]
			user_tokens.append(toAdd)
			res = make_response("Logged in as user", 200)
			res.set_cookie("token", token)
			return res

	return jsonify(request.form), 400

def userCheck(token):
	for x in user_tokens:
		if x["token"] == token:
			return True
	for x in admin_tokens:
		if x["token"] == token:
			return True
	return False

def adminCheck(token):
	for x in admin_tokens:
		if x["token"] == token:
			return True
	return False

@app.route('/createUser', methods=['POST'])
def createUser():
	if (adminCheck(request.cookies.get("token"))):
		users_conn = sqlite3.connect(user_db)
		users_conn.row_factory = sqlite3.Row
		cur = users_conn.cursor()
		username = request.form.get("username")
		password = request.form.get("password")
		hospital = request.form.get("hospital")
		try:
			hospital = int(hospital)
		except ValueError as e:
			return "Invalid hospital ID", 400
		if not (username and password and hospital):
			return "400 bad request", 400
		cur.execute("INSERT INTO users VALUES (?, ?, ?)", (username, sha256_crypt.hash(password), hospital))
		users_conn.commit()
	else:
		return "403 Unauthorized", 403

@app.route('/createAdmin', methods=['POST'])
def createAdmin():
	if (adminCheck(request.cookies.get("token"))):
		users_conn = sqlite3.connect(user_db)
		users_conn.row_factory = sqlite3.Row
		cur = users_conn.cursor()
		username = request.form.get("username")
		password = request.form.get("password")
		if not (username and password):
			return "400 bad request", 400
		cur.execute("INSERT INTO admins VALUES (?, ?)", (username, sha256_crypt.hash(password)))
		users_conn.commit()
	else:
		return "403 Unauthorized", 403

@app.route('/', methods=['GET'])
def mainPage():
	if request.cookies.get("token"):
		if userCheck(request.cookies.get("token")):
			return app.send_static_file("OmnoDashboard.html")
	return app.send_static_file("LoginView.html")

@app.route('/data', methods=['POST'])
def data():
	y = request.form.get("y")
	x = request.form.get("x")
	conditions = request.form.get("conditions")
	if (x and y):
		toReturn = {}
	elif (y):
		toReturn = {}

if (__name__ == "__main__"):
	app.run()
print('Running website')
