from flask import Blueprint, request, jsonify
from utils.bedrock import bedrock_service
from utils.database import db
from utils.helpers import serialize_document
from datetime import datetime, timedelta
from bson import ObjectId
from utils.database import db
import json
import random
from random import randint

random.seed(datetime.now().timestamp())
crud_bp = Blueprint('crud', __name__)

@crud_bp.route('/api/schedule', methods=['GET'])
def get_current_schedule():
    stationdb = db.stations  
    orderdb = db.orders
    itemdb = db.items
    datas = db.schedules.find({}).to_list()

    for data in datas:
        priority = randint(0, 2)
        name = "John Doe"
        if priority == 0:
            priority = "high"
            name = "Jane Doe"
        elif priority == 1:
            priority = "low"
        else:
            priority = "medium"
            name = "Jane Doe"

        stationId = data["station_id"]
        orderId = data["order_id"]
        stationData = stationdb.find_one({ "_id": stationId })
        orderData = orderdb.find_one({ '_id': orderId })
        data["station"] = stationData["id"]
        data["priority"] = priority
        data["estimatedTime"] = data["end_time"] - data["start_time"]
        data["customerName"] = name
        orderItems = orderData["items"]
        items = []
        for item in orderItems:
            itemData = itemdb.find_one({'_id': item['item_id']})
            items.append(itemData["proper_name"])
        data["items"] = items
        data["id"] = data["_id"]
    return json.dumps(datas, default=str)
