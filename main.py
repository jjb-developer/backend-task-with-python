from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
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
		return jsonify({"message": "Bienvenido a Flask"})


	#@jwt_required()
	@app.route("/info", methods=['GET'])
	def info_user():
		return jsonify({"message": "Hemos enviado toda la informacion. [GET]"})



	@app.route("/login", methods=['POST'])
	def login_user():
		return jsonify({"message": "Te has logeado satisfactoriamente. [POST]"})



	@app.route("/register", methods=['POST'])
	def register_user():
		return jsonify({"message": "Te has registrado exitosamente. [POST]"})


	return app


"""
if __name__ == "__main__":
	app = create_app()
	app.run(debug=True, port=8080)
"""