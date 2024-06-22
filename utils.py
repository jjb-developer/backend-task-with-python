def createPayload(email):
	return {
		"email": email,
		"exp": datetime.utcnow() + timedelta(hours=7)
	}