from datetime import datetime
from bson import ObjectId
from utils.database import db
from utils.helpers import serialize_document, get_stock_status, get_days_until_expiry

class Ingredient:
    def __init__(self, name, category, best_used_days, price_per_unit, unit, current_stock=0, last_restock_date=None):
        self.name = name
        self.category = category
        self.best_used_days = best_used_days
        self.price_per_unit = price_per_unit
        self.unit = unit
        self.current_stock = current_stock
        self.last_restock_date = last_restock_date

    def to_dict(self):
        """Convert ingredient instance to dictionary"""
        return {
            'name': self.name,
            'category': self.category,
            'best_used_days': self.best_used_days,
            'price_per_unit': self.price_per_unit,
            'unit': self.unit,
            'current_stock': self.current_stock,
            'last_restock_date': self.last_restock_date,
        }

    @staticmethod
    def get_all_with_analysis():
        """Get all ingredients with stock analysis"""
        pipeline = [
            {
                '$lookup': {
                    'from': 'restocks',
                    'localField': '_id',
                    'foreignField': 'ingredient_id',
                    'as': 'restocks'
                }
            },
            {
                '$addFields': {
                    'active_restocks': {
                        '$filter': {
                            'input': '$restocks',
                            'as': 'restock',
                            'cond': {
                                '$or': [
                                    {
                                        '$and':[
                                            {'$gt': ['$$restock.items_left', 0]},
                                            {'$gte': ['$$restock.expiry_date', datetime.now()]}
                                        ]
                                    },
                                    {
                                        '$and': [
                                            {'$lt': ['$$restock.expiry_date', datetime.now()]},
                                            {'$eq': ['$$restock.clear', False]}
                                        ]
                                    }
                                ]
                            }
                        }
                    }
                }
            },
            {
                '$addFields': {
                    'earliest_expiry': {
                        '$min': '$active_restocks.expiry_date'
                    }
                }
            },
            {
                '$sort': {'category': 1, 'name': 1}
            }
        ]
        
        ingredients = list(db.ingredients.aggregate(pipeline))
        
        # Add analysis fields
        for ingredient in ingredients:
            expiry_date = ingredient.get('earliest_expiry')
            current_stock = ingredient.get('current_stock', 0)
            
            ingredient['days_until_expiry'] = get_days_until_expiry(expiry_date) # thinking of logic
            ingredient['expiry_date'] = expiry_date
            
            del ingredient['restocks']
            del ingredient['active_restocks']
        
        return serialize_document(ingredients)

    @staticmethod
    def get_by_id(ingredient_id):
        """Get ingredient by ID"""
        try:
            ingredient = db.ingredients.find_one({'_id': ObjectId(ingredient_id)})
            return serialize_document(ingredient)
        except Exception as e:
            print(f"Error getting ingredient: {e}")
            return None

    # @staticmethod
    # def create(ingredient_data):
    #     """Create new ingredient"""
    #     ingredient = Ingredient(**ingredient_data)
    #     result = db.ingredients.insert_one(ingredient.to_dict())
    #     return str(result.inserted_id)

    # @staticmethod
    # def update_stock(ingredient_id, quantity_change, last_restock_date=None):
    #     """Update ingredient stock"""
    #     try:
    #         update_data = {'$inc': {'current_stock': quantity_change}}
    #         if last_restock_date:
    #             update_data['$set'] = {'last_restock_date': last_restock_date}
            
    #         result = db.ingredients.update_one(
    #             {'_id': ObjectId(ingredient_id)},
    #             update_data
    #         )
    #         return result.modified_count > 0
    #     except Exception as e:
    #         print(f"Error updating stock: {e}")
    #         return False

    @staticmethod
    def initialize_sample_data():
        """Initialize sample data if collection is empty"""
        if db.ingredients.count_documents({}) == 0:
            sample_ingredients = []
            
            result = db.ingredients.insert_many(sample_ingredients)
            print(f"Inserted {len(result.inserted_ids)} sample ingredients")
            return result.inserted_ids
        
        return []