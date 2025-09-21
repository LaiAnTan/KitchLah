from datetime import datetime, timedelta, timezone
from bson import ObjectId
import json

def serialize_document(doc):
    """Convert MongoDB document to JSON serializable format"""
    if doc is None:
        return None
    
    if isinstance(doc, list):
        return [serialize_document(item) for item in doc]
    
    if isinstance(doc, dict):
        serialized = {}
        for key, value in doc.items():
            if key == '_id' and isinstance(value, ObjectId):
                serialized['_id'] = str(value)
            elif isinstance(value, ObjectId):
                serialized[key] = str(value)
            elif isinstance(value, datetime):
                serialized[key] = value.isoformat()
            elif isinstance(value, dict):
                serialized[key] = serialize_document(value)
            elif isinstance(value, list):
                serialized[key] = serialize_document(value)
            else:
                serialized[key] = value
        return serialized
    
    return doc

def calculate_expiry_date(restock_date, best_used_days):
    """Calculate expiry date based on restock date and best used days"""
    if isinstance(restock_date, str):
        restock_date = datetime.fromisoformat(restock_date.replace('Z', '+00:00'))
    elif isinstance(restock_date, datetime):
        pass
    else:
        restock_date = datetime.now()

    return restock_date + timedelta(days=best_used_days)

# def get_stock_status(current_stock, expiry_date):
#     """Determine stock status based on current stock and expiry date"""
#     if current_stock <= 0:
#         return 'out_of_stock'
#     elif current_stock < 5:
#         return 'low_stock'
#     elif expiry_date:
#         days_until_expiry = (expiry_date - datetime.now()).days
#         if days_until_expiry < 0:
#             return 'expired'
#         elif days_until_expiry <= 2:
#             return 'expiring_soon'
    
#     return 'sufficient'

def get_days_until_expiry(expiry_date):
    """Calculate days until expiry"""
    if not expiry_date:
        return None
    
    if isinstance(expiry_date, str):
        expiry_date = datetime.fromisoformat(expiry_date.replace('Z', '+00:00'))

    # Make sure now is also aware
    now = datetime.now(timezone.utc)
    
    return (expiry_date - now).days