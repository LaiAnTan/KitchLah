from flask import Blueprint, request, jsonify
from models.ingredient import Ingredient

ingredients_bp = Blueprint('ingredients', __name__)

@ingredients_bp.route('/api/ingredients', methods=['GET'])
def get_all_ingredients():
    """Get all ingredients with stock analysis"""
    try:
        ingredients = Ingredient.get_all_with_analysis()
        return jsonify(ingredients), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ingredients_bp.route('/api/ingredients/<ingredient_id>', methods=['GET'])
def get_ingredient(ingredient_id):
    """Get ingredient by ID"""
    try:
        ingredient = Ingredient.get_by_id(ingredient_id)
        if not ingredient:
            return jsonify({'error': 'Ingredient not found'}), 404
        return jsonify(ingredient), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# @ingredients_bp.route('/api/ingredients', methods=['POST'])
# def create_ingredient():
#     """Create new ingredient"""
#     try:
#         data = request.get_json()
        
#         # Validate required fields
#         required_fields = ['name', 'category', 'best_used_days', 'price_per_unit', 'unit']
#         for field in required_fields:
#             if field not in data:
#                 return jsonify({'error': f'Missing required field: {field}'}), 400
        
#         # Validate category
#         valid_categories = ['vegetable', 'meat', 'dairy', 'pantry', 'spices']
#         if data['category'] not in valid_categories:
#             return jsonify({'error': f'Invalid category. Must be one of: {", ".join(valid_categories)}'}), 400
        
#         ingredient_id = Ingredient.create(data)
#         return jsonify({
#             'id': ingredient_id,
#             'message': 'Ingredient created successfully'
#         }), 201
        
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @ingredients_bp.route('/api/ingredients/<ingredient_id>', methods=['PUT'])
# def update_ingredient(ingredient_id):
#     """Update ingredient"""
#     try:
#         data = request.get_json()
        
#         # Remove fields that shouldn't be updated directly
#         data.pop('_id', None)
#         data.pop('created_at', None)
#         data.pop('current_stock', None)  # Stock should be updated via restocks
        
#         from utils.database import db
#         from bson import ObjectId
        
#         result = db.ingredients.update_one(
#             {'_id': ObjectId(ingredient_id)},
#             {'$set': data}
#         )
        
#         if result.matched_count == 0:
#             return jsonify({'error': 'Ingredient not found'}), 404
        
#         return jsonify({'message': 'Ingredient updated successfully'}), 200
        
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @ingredients_bp.route('/api/ingredients/<ingredient_id>', methods=['DELETE'])
# def delete_ingredient(ingredient_id):
#     """Delete ingredient"""
#     try:
#         from utils.database import db
#         from bson import ObjectId
        
#         # First check if ingredient exists
#         ingredient = db.ingredients.find_one({'_id': ObjectId(ingredient_id)})
#         if not ingredient:
#             return jsonify({'error': 'Ingredient not found'}), 404
        
#         # Delete associated restocks
#         db.restocks.delete_many({'ingredient_id': ObjectId(ingredient_id)})
        
#         # Delete ingredient
#         result = db.ingredients.delete_one({'_id': ObjectId(ingredient_id)})
        
#         return jsonify({'message': 'Ingredient deleted successfully'}), 200
        
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500