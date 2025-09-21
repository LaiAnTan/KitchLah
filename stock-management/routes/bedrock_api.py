from flask import Blueprint, request, jsonify
from utils.bedrock import bedrock_service
from utils.database import db
from utils.helpers import serialize_document
from datetime import datetime, timedelta
from bson import ObjectId

bedrock_bp = Blueprint('bedrock', __name__)

@bedrock_bp.route('/api/bedrock/generate-recipes', methods=['POST'])
def generate_recipes():
    """Generate recipes based on ingredient ID using Nova model"""
    try:
        data = request.get_json()
        
        if 'ingredient_id' not in data:
            return jsonify({'error': 'ingredient_id is required'}), 400
        
        ingredient_id = data['ingredient_id']
        
        try:
            ingredient = db.ingredients.find_one({'_id': ObjectId(ingredient_id)})
            if not ingredient:
                return jsonify({'error': 'Ingredient not found'}), 404
        except Exception as e:
            return jsonify({'error': f'Invalid ingredient_id format: {str(e)}'}), 400
        
        # Get related restock information
        restocks = list(db.restocks.find({
            'ingredient_id': ObjectId(ingredient_id),
            'items_left': {'$gt': 0},
            'clear': False
        }))
        
        # Prepare ingredient data for Nova
        ingredient_data = {
            'ingredient_id': ingredient_id,
            'name': ingredient['name'],
            'category': ingredient['category'],
            'current_stock': ingredient.get('current_stock', 0),
            'unit': ingredient['unit'],
            'price_per_unit': ingredient.get('price_per_unit', 0),
            'best_used_days': ingredient.get('best_used_days', 7),
            'stock_analysis': {
                'total_available': sum(restock.get('items_left', 0) for restock in restocks),
                'batches_count': len(restocks),
                'earliest_expiry': min(restock.get('expiry_date') for restock in restocks) if restocks else None,
                'urgency_level': 'high' if ingredient.get('current_stock', 0) > 10 else 'medium'
            }
        }
        
        # Call Nova model to generate recipes
        result = bedrock_service.generate_recipes(ingredient_data=ingredient_data)
        
        if not result['success']:
            return jsonify({
                'success': False,
                'error': result['error'],
                'raw_response': result.get('raw_response', '')
            }), 500
        
        # Return only recipes in response
        return jsonify({
            'recipes': result['recipes']
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bedrock_bp.route('/api/bedrock/generate-discount-plans', methods=['POST'])
def generate_discount_plans():
    """Generate discount plans based on ingredient ID using Nova model"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if 'ingredient_id' not in data:
            return jsonify({'error': 'ingredient_id is required'}), 400
        
        ingredient_id = data['ingredient_id']
        recipe_ids = data.get('recipe_ids', None)  # Optional related recipe IDs
        
        # Get ingredient data from database
        try:
            ingredient = db.ingredients.find_one({'_id': ObjectId(ingredient_id)})
            if not ingredient:
                return jsonify({'error': 'Ingredient not found'}), 404
        except Exception as e:
            return jsonify({'error': f'Invalid ingredient_id format: {str(e)}'}), 400
        
        # Get related restock information
        restocks = list(db.restocks.find({
            'ingredient_id': ObjectId(ingredient_id),
            'items_left': {'$gt': 0},
            'clear': False
        }))
        
        ingredient_data = {
            'ingredient_id': ingredient_id,
            'name': ingredient['name'],
            'category': ingredient['category'],
            'current_stock': ingredient.get('current_stock', 0),
            'unit': ingredient['unit'],
            'price_per_unit': ingredient.get('price_per_unit', 0),
            'best_used_days': ingredient.get('best_used_days', 7),
            'stock_analysis': {
                'total_available': sum(restock.get('items_left', 0) for restock in restocks),
                'batches_count': len(restocks),
                'earliest_expiry': min(restock.get('expiry_date') for restock in restocks) if restocks else None,
                'urgency_level': 'high' if ingredient.get('current_stock', 0) > 10 else 'medium'
            }
        }
        
        # Call Nova model to generate recipes
        result = bedrock_service.generate_discount_plans(ingredient_data=ingredient_data)
        
        if not result['success']:
            return jsonify({
                'success': False,
                'error': result['error'],
                'raw_response': result.get('raw_response', '')
            }), 500
        
        # Return only recipes in response
        return jsonify({
            'recipes': result['recipes']
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500