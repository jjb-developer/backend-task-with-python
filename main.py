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


	@app.after_request
	def add_cors_headers(response):
		response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
		response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
		response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE')
		return response


	@app.route("/", methods=['GET'])
	def home():
		return jsonify({"message": "Bienvenidos a Flask." })



	@app.route("/register", methods=['POST'])
	def register():
		user = request.json
		response, status = db.register(user)
		return jsonify({"response": response})



	@app.route("/login", methods=['POST'])
	def login():
		response, status = db.login(request.json.get('username'),request.json.get('password'))

		if status == 201:
			token = create_access_token(identity=response, expires_delta=timedelta(minutes=30))
			return jsonify({"status": status, "token": str(token,'utf-8'), "username": "lionel"})
		else:
			return jsonify({"message": response, "status": status})




	@app.route("/info", methods=['GET'])
	@jwt_required()
	def information():
		id_user = get_jwt_identity()
		if id_user:
			response, status = db.information(id_user)
			if status == 201:
				return jsonify({"response": response, "status": status})
			else:
				return jsonify({"response": response, "status": status})



	return app




if __name__ == "__main__":
	app = create_app()
	app.run(debug=True, port=8000)
