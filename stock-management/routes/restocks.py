from flask import Blueprint, request, jsonify
from models.restock import Restock

restocks_bp = Blueprint('restocks', __name__)

@restocks_bp.route('/api/restocks', methods=['GET'])
def get_all_restocks():
    """Get all restocks with ingredient details, for restock history"""
    try:
        restocks = Restock.get_all_with_details()
        return jsonify(restocks), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@restocks_bp.route('/api/restocks', methods=['POST'])
def create_restock():
    """Create new restock record"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['ingredient_id', 'quantity_added', 'date']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Validate quantity
        if data['quantity_added'] <= 0:
            return jsonify({'error': 'Quantity must be greater than 0'}), 400
        
        restock_id, message = Restock.create(data)
        
        if restock_id:
            return jsonify({
                'id': restock_id,
                'message': message
            }), 201
        else:
            return jsonify({'error': message}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@restocks_bp.route('/api/restocks/ingredient/<ingredient_id>', methods=['GET'])
def get_restocks_by_ingredient(ingredient_id):
    """Get restocks for specific ingredient, before expiry and expired but not cleared"""
    try:
        restocks = Restock.get_by_ingredient_id(ingredient_id)
        return jsonify(restocks), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@restocks_bp.route('/api/restocks/clear/<restocks_id>')
def clear_expired_stock(restocks_id):
    """Mark expired restock that still have items as cleared"""
    try: 
        success, message = Restock.mark_as_cleared(restocks_id)
        
        if success:
            return jsonify({'message': message}), 200
        else:
            return jsonify({'error': message}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@restocks_bp.route('/api/restocks/<ingredient_id>/consume', methods=['PUT'])
def consume_from_restock(ingredient_id):
    """Update items left after consumption, real time feature, call when real time order coming in"""
    try:
        data = request.get_json()
        
        if 'items_consumed' not in data:
            return jsonify({'error': 'Missing required field: items_consumed'}), 400
        
        if data['items_consumed'] <= 0:
            return jsonify({'error': 'Items consumed must be greater than 0'}), 400
        
        # Update the specific restock's items_left
        success = Restock.update_items_left(ingredient_id, data['items_consumed'])
        
        if success:
            # Also update ingredient's current stock
            from utils.database import db
            from bson import ObjectId
            
            restock = db.restocks.find_one({'_id': ObjectId(ingredient_id)})
            if restock:
                db.ingredients.update_one(
                    {'_id': restock['ingredient_id']},
                    {'$inc': {'current_stock': -data['items_consumed']}}
                )
            
            return jsonify({'message': 'Stock updated successfully'}), 200
        else:
            return jsonify({'error': 'Failed to update restock'}), 400
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
