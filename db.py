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

		query = "SELECT id_user, name || ' ' || lastname AS name_complete FROM users WHERE username=%s and password=%s"

		salt = b'$2b$12$GDieQzheal5usWG8OAYziO'
		password_encrypted = bcrypt.hashpw(password.encode(), salt).decode('utf-8')

		cursor.execute(query,(username,password_encrypted))
		row = cursor.fetchall()
		conexion.close()
		return {"id_user": row[0][0], "name_completed": row[0][1]}, 201
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




def create(id_user,info):
	try:
		conexion = psycopg2.connect(os.getenv('DB_URL'))
		cursor = conexion.cursor()
		query = "INSERT INTO info (id_user,category,title,details,color,priority) VALUES (%s,%s,%s,%s,%s,%s)"
		cursor.execute(query,(id_user,info['category'],info['title'],info['details'],info['color'],info['priority']))
		conexion.commit()
		conexion.close()
		return "Se ha registrado la informacion exisotsamente.", 201
	except Exception as error:
		return str(error), 401



def update(id_user,info):
	try:
		conexion = psycopg2.connect(os.getenv('DB_URL'))
		cursor = conexion.cursor()
		query = "UPDATE info SET category=%s, title=%s, details=%s, color=%s, priority=%s WHERE id_info=%s AND id_user=%s"
		cursor.execute(query,(info['category'],info['title'],info['details'],info['color'],info['priority'],info['id_info'],id_user))
		conexion.commit()
		conexion.close()
		return "Se ha actualizado la informacion exisotsamente.", 201
	except Exception as error:
		return str(error), 401




def delete(id_user,id_info):
	try:
		conexion = psycopg2.connect(os.getenv('DB_URL'))
		cursor = conexion.cursor()
		query = "DELETE FROM info WHERE id_info=%s AND id_user=%s"
		cursor.execute(query,(id_info,id_user))
		conexion.commit()
		conexion.close()
		return "Se eliminado la informacion exisotsamente.", 201
	except Exception as error:
		return str(error), 401