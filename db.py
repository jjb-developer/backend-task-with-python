import psycopg2
import bcrypt
import os



def registrar_user(user):
	conexion = psycopg2.connect(os.getenv('DB_URL'))
	cursor = conexion.cursor()
	query = "INSERT INTO users (name,lastname,email,username,password) VALUES (%s,%s,%s,%s,%s)"

	salt = b'$2b$12$GDieQzheal5usWG8OAYziO'
	password_encrypted = bcrypt.hashpw(password.encode(), salt).decode('utf-8')

	cursor.execute(query, (name,lastname,email,username,password_encrypted))
	conexion.commit()
	conexion.close()
	return 201


def login_user(username, password):
	conexion = psycopg2.connect(os.getenv('DB_URL'))
	cursor = conexion.cursor()

	salt = b'$2b$12$GDieQzheal5usWG8OAYziO'
	password_encrypted = bcrypt.hashpw(password.encode(), salt).decode('utf-8')[:50]

	query = "SELECT * FROM users WHERE username=%s and password=%s"
	cursor.execute(query,(username,password_encrypted))
	row = cursor.fetchall()
	conexion.close()
	if len(row) > 0:
		return True
	else:
		return False


def info_user(username):
	conexion = psycopg2.connect(os.getenv('DB_URL'))
	cursor = conexion.cursor()
	query = "SELECT * FROM usuarios WHERE email=%s"
	cursor.execute(query,(username,))
	row = cursor.fetchall()
	conexion.close()

	return list(map(lambda user: {
			"id": user[0],
			"nombre": user[1],
			"apellido": user[2],
			"email": user[3]
	}, row))