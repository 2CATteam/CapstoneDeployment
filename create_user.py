from passlib.hash import sha256_crypt
import sys
import sqlite3

def insert_user(username, password, hospital):
	conn = sqlite3.connect("users.db")
	cursor = conn.cursor()
	cursor.execute("INSERT INTO users VALUES (?, ?, ?)", username, password, hospital)

if __name__ == "__main__":
	if (len(sys.argv) < 3):
		print('''Usage is as follows:

python3 create_user.py username password hospitalId

For example:

python3 create_user.py admin hunter2 3''')
		return
	username = sys.argv[1]
	password = sys.argv[2]
	permissions = int(sys.argv[3])
	insert_user(username, password, parmissions)
