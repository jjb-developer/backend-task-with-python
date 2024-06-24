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


	@app.route("/", methods=['GET'])
	def home():
		return "Pagina Principal."


	@app.route("/index", methods=['GET'])
	@jwt_required()
	def getInfoUser():
		usuario_actual = get_jwt_identity()
		if usuario_actual:
			return jsonify({"message": "El user {} ha esta logeado.".format(usuario_actual)}) #"user": db.informacionUsuario(payload_token['email'])[0]
		else:
			return jsonify({"message": "Token caducado." })



	@app.route("/login", methods=['POST'])
	def authUser():
		responseDB = db.autenticacionUsuario(request.json.get('email'),request.json.get('password'))
		try:
			if responseDB:
				token = create_access_token(identity=username, expires_delta=timedelta(minutes=30))
				return jsonify({"status": 200, "token": str(token,'utf-8')})
				#return jsonify(access_token=access_token), 200
			else:
				return jsonify({"message": "credenciales incorrectas."})
		except Exception as error:
			return jsonify({"error": str(error)})



	@app.route("/register", methods=['POST'])
	def registerUser():
		user = request.json
		return db.registrarUsuario(user.get('nombre'), user.get('apellido'), user.get('email'), user.get('password'))

	return app

if __name__ == "__main__":
	app = create_app()
	app.run(debug=True, port=8080)