import psycopg2
import bcrypt
import os

def registrarUsuario(url,user):
	pass


def obtenerFullUsuarios():
	conexion = psycopg2.connect(os.getenv('DB_URL'))
	cursor = conexion.cursor()
	cursor.execute("SELECT * FROM usuarios")
	users = cursor.fetchall()
	conexion.close()
	return users


def registrarUsuario(nombre, apellido, email, password):
	conexion = psycopg2.connect(os.getenv('DB_URL'))
	cursor = conexion.cursor()
	query = "INSERT INTO usuarios (nombre,apellido,email,password) VALUES (%s,%s,%s,%s)"

	salt = b'$2b$12$GDieQzheal5usWG8OAYziO'
	password_encrypted = bcrypt.hashpw(password.encode(), salt).decode('utf-8')

	cursor.execute(query, (nombre, apellido, email, password_encrypted[:50]))
	conexion.commit()
	conexion.close()
	return "Usuario regsitrado exitosamente."


def autenticacionUsuario(email, password):
	conexion = psycopg2.connect(os.getenv('DB_URL'))
	cursor = conexion.cursor()

	salt = b'$2b$12$GDieQzheal5usWG8OAYziO'
	password_encrypted = bcrypt.hashpw(password.encode(), salt).decode('utf-8')[:50]

	query = "SELECT * FROM usuarios WHERE email='{}' and password='{}'".format(email,password_encrypted)
	cursor.execute(query)
	row = cursor.fetchall()
	conexion.close()
	if len(row) > 0:
		return True
	else:
		return False


def informacionUsuario(email):
	conexion = psycopg2.connect(os.getenv('DB_URL'))
	cursor = conexion.cursor()
	query = "SELECT * FROM usuarios WHERE email='{}'".format(email)
	cursor.execute(query)
	row = cursor.fetchall()
	conexion.close()

	return list(map(lambda user: {
			"id": user[0],
			"nombre": user[1],
			"apellido": user[2],
			"email": user[3]
	}, row))