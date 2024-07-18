import psycopg2
import bcrypt
import os



def register(user):
	try:
		conexion = psycopg2.connect(os.getenv('DB_URL'))
		cursor = conexion.cursor()

		query = "INSERT INTO users (name,lastname,email,username,password) VALUES (%s,%s,%s,%s,%s)"

		salt = b'$2b$12$GDieQzheal5usWG8OAYziO'
		password_encrypted = bcrypt.hashpw(user['password'].encode(), salt).decode('utf-8')

		cursor.execute(query, (user['nombre'],user['apellido'],user['email'],user['username'],password_encrypted))
		conexion.commit()
		conexion.close()
		return "El usuario fue registrado exisotsamente.", 201
	except Exception as error:
		return str(error), 401

	


def login(username,password):
	try:
		conexion = psycopg2.connect(os.getenv('DB_URL'))
		cursor = conexion.cursor()

		query = "SELECT id_user FROM users WHERE username=%s and password=%s"

		salt = b'$2b$12$GDieQzheal5usWG8OAYziO'
		password_encrypted = bcrypt.hashpw(password.encode(), salt).decode('utf-8')

		cursor.execute(query,(username,password_encrypted))
		row = cursor.fetchall()
		conexion.close()
		return row[0][0], 201
	except Exception as error:
		return str(error), 401




def information(id_user):
	try:
		conexion = psycopg2.connect(os.getenv('DB_URL'))
		cursor = conexion.cursor()
		query = "SELECT id_info,category,title,details,created_at,color,priority FROM info WHERE id_user=%s"
		cursor.execute(query,(id_user,))
		row = cursor.fetchall()
		conexion.close()
		return list(map(lambda user: {
				"id_info": user[0],
				"category": user[1],
				"title": user[2],
				"details": user[3],
				"created_at": user[4],
				"color": user[5],
				"priority": user[6]
		}, row)), 201
	except Exception as error:
		return str(error), 401