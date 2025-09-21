from datetime import datetime
from bson import ObjectId
from utils.database import db
from utils.helpers import serialize_document, calculate_expiry_date

class Restock:
    def __init__(self, ingredient_id, quantity_added, date, items_left=None, expiry_date=None, clear=False):
        self.ingredient_id = ObjectId(ingredient_id) if isinstance(ingredient_id, str) else ingredient_id
        self.quantity_added = quantity_added
        self.date = date if isinstance(date, datetime) else datetime.fromisoformat(date.replace('Z', '+00:00'))
        self.items_left = items_left if items_left is not None else quantity_added
        self.expiry_date = expiry_date
        self.clear = clear if clear is not None else False


    def to_dict(self):
        """Convert restock instance to dictionary"""
        return {
            'ingredient_id': self.ingredient_id,
            'quantity_added': self.quantity_added,
            'date': self.date,
            'items_left': self.items_left,
            'expiry_date': self.expiry_date,
            'clear': self.clear
        }

    @staticmethod
    def create(restock_data):
        """Create new restock record"""
        try:
            # Get ingredient details to calculate expiry
            ingredient = db.ingredients.find_one({'_id': ObjectId(restock_data['ingredient_id'])})
            if not ingredient:
                return None, "Ingredient not found"

            # Calculate expiry date
            expiry_date = calculate_expiry_date(
                restock_data['date'], 
                ingredient['best_used_days']
            )

            # Create restock record
            restock = Restock(
                ingredient_id=restock_data['ingredient_id'],
                quantity_added=restock_data['quantity_added'],
                date=restock_data['date'],
                items_left=restock_data['quantity_added'],
                expiry_date=expiry_date
            )

            # Insert restock
            result = db.restocks.insert_one(restock.to_dict())
            restock_id = str(result.inserted_id)
            
            # Update ingredient stock
            db.ingredients.update_one(
                {'_id': ObjectId(restock_data['ingredient_id'])},
                {
                    '$inc': {'current_stock': restock_data['quantity_added']},
                    '$set': {'last_restock_date': restock.date}
                }
            )

            return str(restock_id), "Restock added successfully"
        except Exception as e:
            print(f"Error creating restock: {e}")
            return None, str(e)

    @staticmethod
    def get_all_with_details():
        """Get all restocks with ingredient details"""
        pipeline = [
            {
                '$lookup': {
                    'from': 'ingredients',
                    'localField': 'ingredient_id',
                    'foreignField': '_id',
                    'as': 'ingredient'
                }
            },
            {
                '$unwind': '$ingredient'
            },
            {
                '$addFields': {
                    'ingredient_name': '$ingredient.name',
                    'unit': '$ingredient.unit',
                    'category': '$ingredient.category',
                    'price_per_unit': '$ingredient.price_per_unit'
                }
            },
            {
                '$project': {
                    'ingredient': 0  # Remove the full ingredient object to keep response clean
                }
            },
            {
                '$sort': {'date': -1}
            }
        ]
        
        restocks = list(db.restocks.aggregate(pipeline))
        return serialize_document(restocks)

    @staticmethod
    def get_by_ingredient_id(ingredient_id):
        """Get restocks for specific ingredient, show all the stocks that haven't expired, including the one have expired but stock isn't clear"""
        try:
            restocks = list(db.restocks.find({
                'ingredient_id': ObjectId(ingredient_id),
                '$or': [
                    {   # Case 1: Still usable
                        'items_left': {'$gt': 0},
                        'expiry_date': {'$gte': datetime.now()}
                    },
                    {   # Case 2: Expired but not yet cleared
                        'expiry_date': {'$lt': datetime.now()},
                        'clear_flag': False
                }
                ]
            }).sort('date', -1))  
        
            return serialize_document(restocks)
        except Exception as e:
            print(f"Error getting restocks: {e}")
            return []

    @staticmethod
    def update_items_left(ingredient_id, items_consumed):
        """Update items left after consumption"""
        try:
            result = db.restocks.find_one_and_update(
                {
                    'ingredient_id': ObjectId(ingredient_id),
                    'items_left': {'$gt': 0}, # only if stock is available
                    'expiry_date': {'$gte': datetime.now()}
                },
                {
                    '$inc': {'items_left': -items_consumed}
                },
                sort=[('date', 1)],  # 1 = ascending → earliest date first
                return_document=True
            )
            return result is not None
        except Exception as e:
            print(f"Error updating items left (FIFO): {e}")
            return False
        
    @staticmethod
    def get_by_restock_id(restock_id):
        """Get restock by restock_id"""
        try:
            restock = db.restocks.find_one({'_id': ObjectId(restock_id)})
            return serialize_document(restock)
        except Exception as e:
            print(f"Error getting restock by ID: {e}")
            return None
        
    @staticmethod
    def mark_as_cleared(restock_id):
        """Mark expired restock as cleared"""
        try:
            restock = db.restocks.find_one({'_id': ObjectId(restock_id)})
            
            if not restock:
                return False, "Restock not found"
            
            result = db.restocks.update_one(
                {'_id': ObjectId(restock_id)},
                {'$set': {'clear': True}}
            )
            
            if result.modified_count > 0:
                ingredient_update = db.ingredients.update_one(
                    {'_id': restock['ingredient_id']},
                    {'$inc': {'current_stock': -restock['items_left']}}
                )
                
                if ingredient_update > 0:
                    return True, "Restock marked as cleared and ingredient stock updated"
            return False, "Failed to update ingredient stock"
        except Exception as e:
            print(f"Error marking restock as cleared: {e}")
            return False
        
    @staticmethod
    def initialize_sample_data(ingredient_ids):
        """Initialize sample restock data"""
        if db.restocks.count_documents({}) == 0 and ingredient_ids:
            sample_restocks = []
            
            result = db.restocks.insert_many(sample_restocks)
            print(f"Inserted {len(result.inserted_ids)} sample restocks")
            return result.inserted_ids
        
        return []