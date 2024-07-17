import psycopg2
import bcrypt
import os




def register_user(user):
	conexion = psycopg2.connect(os.getenv('DB_URL'))
	cursor = conexion.cursor()
	query = "INSERT INTO users (name, lastname, email, password, username) VALUES (%s,%s,%s,%s,%s)"

	salt = b'$2b$12$GDieQzheal5usWG8OAYziO'
	password_encrypted = bcrypt.hashpw(user['password'].encode(), salt).decode('utf-8')

	cursor.execute(query, (user['nombre'], user['apellido'], user['email'], password_encrypted, user['username']))
	conexion.commit()
	conexion.close()
	return {'code': 200}




def autentication_user(username, password):
	conexion = psycopg2.connect(os.getenv('DB_URL'))
	cursor = conexion.cursor()

	salt = b'$2b$12$GDieQzheal5usWG8OAYziO'
	password_encrypted = bcrypt.hashpw(password.encode(), salt).decode('utf-8') #[:50]

	try:
		query = "SELECT id_user, username FROM users WHERE username=%s and password=%s"
		cursor.execute(query,(username,password_encrypted))
		row = list(cursor.fetchall()[0])
		conexion.close()
		if len(row) > 0:
			return True, row[0], row[1]
	except Exception as error:
		return False, None, None




def get_info(id_user):
	conexion = psycopg2.connect(os.getenv('DB_URL'))
	cursor = conexion.cursor()
	query = "SELECT id_info, category, title, details, created_at, color, priority FROM info WHERE id_user=%s"
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
	}, row))