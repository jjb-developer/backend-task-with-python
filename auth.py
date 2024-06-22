import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv


def generateToken(payload):
	token = jwt.encode(payload, os.getenv("SECRET_KEY"), algorithm="HS256")
	return token


def validedToken(token):
	try:
		payload_token = jwt.decode(token, os.getenv("SECRET_KEY"), algorithm="HS256")
		return payload_token
	except:
		return False