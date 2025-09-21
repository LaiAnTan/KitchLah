from flask import Blueprint, request, jsonify
from utils.bedrock import bedrock_service
from utils.database import db
from utils.helpers import serialize_document
from datetime import datetime, timedelta
from bson import ObjectId
from utils.database import db
import json

crud_bp = Blueprint('crud', __name__)

@crud_bp.route('/api/schedule', methods=['GET'])
def get_current_schedule():
    data = db.schedules.find({}).to_list()
    return json.dumps(data, default=str)
