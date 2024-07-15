from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, get_jwt
import auth
from datetime import datetime, timedelta
import db
from dotenv import load_dotenv
from os import getenv



def create_app():

	app = Flask(__name__)

	CORS(app, resources={r"/*": {"origins": [getenv('FRONTEND_LOCAL'),getenv('FRONTEND_ONLINE')]}})

	app.config["JWT_SECRET_KEY"] = getenv('SECRET_KEY')
	jwt = JWTManager(app)



	@app.route("/", methods=['GET'])
	def home():
		return "Backend Activo!."





	@app.route("/register", methods=['POST'])
	def register_user():
		user = request.json
		return db.register_user(user)





	@app.route("/login", methods=['POST'])
	def autentication_user():
		is_valid_credenciales, id_user, username = db.autentication_user(request.json.get('username'),request.json.get('password'))
		try:
			if is_valid_credenciales:
				token = create_access_token(identity=id_user, additional_claims={"username": username}, expires_delta=timedelta(minutes=60))
				return jsonify({"status": 200, "token": str(token,'utf-8'), "username": username})
			else:
				return jsonify({"message": "Error en username o password."})
		except Exception as error:
			return jsonify({"Details error:": str(error)})





# ---------------------------  INFO  ----------------------------



	@app.route("/info", methods=['GET'])
	@jwt_required()
	def get_info():
		id_user = get_jwt_identity()
		if id_user:
			info = db.get_info(id_user)
			return jsonify({"code": 200, "info": info})
		else:
			return jsonify({"message": "Token caducado.", "code": 401 })




	@app.route("/info", methods=['POST'])
	@jwt_required()
	def create_info():
		id_user = get_jwt_identity()
		if id_user:
			code = db.create_info(id_user,request.json)
			return jsonify({"code": code})
		else:
			return jsonify({"message": "El token a expirado."})



	@app.route("/info", methods=['PATCH'])
	@jwt_required()
	def update_info():
		id_user = get_jwt_identity()
		if id_user:
			code = db.update_info(id_user,request.json)
			return jsonify({"code": code})
		else:
			return jsonify({"message": "El token a expirado."})




	@app.route("/info", methods=['DELETE'])
	@jwt_required()
	def delete_info():
		id_user = get_jwt_identity()
		if id_user:
			code = db.delete_info(request.json.get('id_info'),id_user)
			return jsonify({"code": code})
		else:
			return jsonify({"message": "El token a expirado."})



	return app



if __name__ == "__main__":
	app = create_app()
	app.run(debug=True, port=8081)