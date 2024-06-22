from flask import Flask, request, jsonify
import auth
from datetime import datetime, timedelta
import json
import db


def create_app():
	app = Flask(__name__)



	@app.route("/", methods=['GET'])
	def home():
		return "Pagina Principal."



	@app.route("/index", methods=['GET'])
	def getInfoUser():
		token = request.json.get('token')
		payload_token = auth.validedToken(token)
		if payload_token:
			return jsonify({"message": "El user {} ha esta logeado.".format(payload_token['email']), "user": db.informacionUsuario(payload_token['email'])[0]})
		else:
			return jsonify({"message": "Token caducado." })



	@app.route("/login", methods=['POST'])
	def authUser():
		responseDB = db.autenticacionUsuario(request.json.get('email'),request.json.get('password'))
		if responseDB:
			payload = {
				"email": request.json.get('email'),
				"exp": datetime.now() + timedelta(hours=7)
			}
			token = auth.generateToken(payload)
			return jsonify({"status": 200, "token": token.decode('utf-8')})
		else:
			return jsonify({"message": "credenciales incorrectas."})



	@app.route("/register", methods=['POST'])
	def registerUser():
		user = request.json
		return db.registrarUsuario(user.get('nombre'), user.get('apellido'), user.get('email'), user.get('password'))

	return app

if __name__ == "__main__":
	app = create_app()
	app.run()