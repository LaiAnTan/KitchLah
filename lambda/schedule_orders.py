import json, base64
from datetime import datetime
from pymongo import MongoClient

client = MongoClient()
db = client["restaurant"]
orders = db["orders"]


def lambda_handler(event, context):

	for record in event["Records"]:

		payload = base64.b64decode(record["kinesis"]["data"])
		data = json.loads(payload)
		orders.insert_one(data)
		print(f"Inserted order: {data}")
	
	return {"status": "ok"}



