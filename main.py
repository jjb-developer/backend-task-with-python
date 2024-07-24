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
		#response.headers.add('Access-Control-Allow-Origin', getenv('FRONTEND_LOCAL'))
		response.headers.add('Access-Control-Allow-Origin', getenv('FRONTEND_ONLINE'))
		response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
		response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE')
		return response


	@app.route("/", methods=['GET'])
	def home():
		return jsonify({"message": "Bienvenido a Ideaspace :D" })



	@app.route("/register", methods=['POST'])
	def register():
		user = request.json
		response, status = db.register(user)
		return jsonify({"response": response})



	@app.route("/login", methods=['POST'])
	def login():
		response, status = db.login(request.json.get('username'),request.json.get('password'))

		if status == 201:
			token = create_access_token(identity=response['id_user'], expires_delta=timedelta(minutes=30))
			return jsonify({"status": status, "ideaspace": {"token": str(token), "user": response['name_completed']}}) # PRODUCTION
			#return jsonify({"status": status, "ideaspace": {"token": str(token,'UTF-8'), "user": response['name_completed']}}) # DEVELOPER
		else:
			return jsonify({"message": response, "status": status})




	@app.route("/info", methods=['GET'])
	@jwt_required()
	def informationRead():
		id_user = get_jwt_identity()
		if id_user:
			response, status = db.information(id_user)
			if status == 201:
				return jsonify({"response": response, "status": status})
			else:
				return jsonify({"response": response, "status": status})



	@app.route("/info", methods=['POST'])
	@jwt_required()
	def informationCreate():
		id_user = get_jwt_identity()
		if id_user:
			response, status = db.create(id_user,request.json)
			if status == 201:
				return jsonify({"response": response, "status": status})
			else:
				return jsonify({"response": response, "status": status})



	@app.route("/info", methods=['PUT'])
	@jwt_required()
	def informationUpdate():
		id_user = get_jwt_identity()
		if id_user:
			response, status = db.update(id_user,request.json)
			if status == 201:
				return jsonify({"response": response, "status": status})
			else:
				return jsonify({"response": response, "status": status})




	@app.route("/info", methods=['DELETE'])
	@jwt_required()
	def informationDelete():
		id_user = get_jwt_identity()
		if id_user:
			response, status = db.delete(id_user,request.json.get('id_info'))
			if status == 201:
				return jsonify({"response": response, "status": status})
			else:
				return jsonify({"response": response, "status": status})



	return app




#if __name__ == "__main__":
#	app = create_app()
#	app.run(debug=True, port=8000)
