from datetime import datetime
import json
import base64

obj = {
	"orderID": "1",
	"datetime": str(datetime.now()),
	"items": [
		{
			"item_id": "68cfbac49cd6acf342686777",
			"quantity": 1,
			"remarks": "More Spaghetti"
		},
		{
			"item_id": "68cfbac49cd6acf342686778",
			"quantity": 4,
			"remarks": "More Chicken Chop"
		}
	]
}

print(base64.b64encode(json.dumps(obj).encode('utf-8')))

import bson

print(bson.ObjectId("68cfbac49cd6acf342686777"))