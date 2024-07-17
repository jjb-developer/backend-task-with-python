from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
import auth
from datetime import datetime, timedelta
import db
from dotenv import load_dotenv
from os import getenv



def create_app():
	app = Flask(__name__)
	app.config["JWT_SECRET_KEY"] = getenv('SECRET_KEY')
	jwt = JWTManager(app)



	# Middleware para los CORS
	@app.after_request
	def add_cors_headers(response):
		response.headers.add('Access-Control-Allow-Origin', getenv('FRONTEND_LOCAL'))
		response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
		response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE')
		return response



	# Ruta de Bienvenida
	@app.route("/", methods=['GET'])
	def home():
		return jsonify({"message": "Bienvenidos a Ideaspace."})



	# Ruta para registrar usuarios
	@app.route("/register", methods=['POST'])
	def register_user():
		user = request.json
		return db.register_user(user)



	# Ruta para autenticar usuarios
	@app.route("/login", methods=['POST'])
	def autentication_user():
		is_valid_credenciales, id_user, username = db.autentication_user(request.json.get('username'),request.json.get('password'))
		try:
			if is_valid_credenciales:
				token = create_access_token(identity=id_user, additional_claims={"username": username}, expires_delta=timedelta(minutes=30))
				return jsonify({"status": 200, "token": str(token,'utf-8'), "username": username})
			else:
				return jsonify({"message": "credenciales incorrectas."})
		except Exception as error:
			return jsonify({"Details error:": str(error)})



	# Ruta para obtener la informacion del usuario autenticado y generarle un token de acceso
	@app.route("/info", methods=['GET'])
	@jwt_required()
	def get_info():
		id_user = get_jwt_identity()
		if id_user:
			info = db.get_info(id_user)
			return jsonify({"code": 200, "info": info})
		else:
			return jsonify({"message": "Token caducado.", "code": 401 })



	return app



if __name__ == "__main__":
	app = create_app()
	app.run(debug=True, port=8080)