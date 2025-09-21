from flask import Blueprint, request, jsonify
from models.ingredient import Ingredient
from models.restock import Restock
from utils.database import db
from datetime import datetime, timedelta
from ai_prediction.main import run

alert_bp = Blueprint('alert', __name__)

@alert_bp.route('/api/expiry_alert', methods=['GET'])
def get_expirty_alert():
    """Get expiry alerts by calling ML model and identifying ingredients that will expire with remaining stock"""
    try:
        # Step 1: Call ML model to get 7-day ingredient predictions
        # try:
            # call ingredients api
        _, _, df_ingredients, _, _ = run()
            # ml_response = requests.post(ml_model_url, timeout=30)
            
            # if ml_response.status_code != 200:
            #     return jsonify({
            #         'error': f'ML model API returned status {ml_response.status_code}',
            #         'details': ml_response.text
            #     }), 500
            
            # ml_data = ml_response.json()
            
            # if 'ingredient_consumption' not in ml_data:
            #     return jsonify({'error': 'ML model response missing ingredient_consumption field'}), 500
            
            # {'fish_patty': [100,200,200,100,200]}
        # predicted_consumption = ml_data['ingredient_consumption']
        predicted_consumption = df_ingredients

        # except requests.RequestException as e:
        #     return jsonify({'error': f'Failed to call ML model: {str(e)}'}), 500

        # Step 2: Calculate expiry alerts
        expiry_alerts = []

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
                            'cond': {
                                '$and': [
                                    {'$gt': ['$this.items_left', 0]},
                                    {'$gte': ['$this.expiry_date', datetime.now()]},
                                    {'$eq': ['$this.clear', False]}
                                ]
                            }
                        }
                    }
                }
            }
        ]
        
        ingredients = list(db.ingredients.aggregate(pipeline))
        
        # Step 3: For each ingredient, simulate consumption and check for expiry waste
        for ingredient in ingredients:
            ingredient_id = ingredient['_id']
            # Skip if no prediction for this ingredient
            if ingredient_id not in predicted_consumption:
                continue
            
            daily_consumption = predicted_consumption[ingredient_id]
            daily_consumption = list(daily_consumption)

            if not isinstance(daily_consumption, list) or len(daily_consumption) != 7:
                continue
            
            # Calculate expiry waste for this ingredient
            print(ingredient['active_restocks'])
            expiry_analysis = _calculate_expiry_waste(
                ingredient['active_restocks'],
                daily_consumption
            )
            
            # Create alert if there will be expired waste
            if expiry_analysis['has_expiry_waste']:
                alert = {
                    'ingredient_id': ingredient_id,
                    'name': ingredient['name'],
                    'unit': ingredient['unit'],
                    'price_per_unit': ingredient.get('price_per_unit', 0),
                    'total_waste_amount': expiry_analysis['total_waste_amount'],
                    'waste_value': expiry_analysis['waste_value'],
                    'expiry_timeline': expiry_analysis['expiry_timeline'],
                    'consumption_vs_expiry': expiry_analysis['consumption_vs_expiry'],
                    'waste_percentage': expiry_analysis['waste_percentage'],
                    'alert_severity': _get_expiry_alert_severity(
                        expiry_analysis['waste_percentage'],
                        expiry_analysis['waste_value']
                    ),
                    'recommendations': expiry_analysis['recommendations']
                }
                expiry_alerts.append(alert)
        
        # Sort alerts by waste value (highest waste first)
        expiry_alerts.sort(key=lambda x: x['waste_value'], reverse=True)
        
        # Calculate summary statistics
        total_waste_value = sum(alert['waste_value'] for alert in expiry_alerts)
        total_waste_items = sum(alert['total_waste_amount'] for alert in expiry_alerts)
        
        return jsonify({
            'success': True,
            'expiry_alerts': expiry_alerts,
            'summary': {
                'total_alerts': len(expiry_alerts),
                'high_waste_alerts': len([a for a in expiry_alerts if a['alert_severity'] == 'high']),
                'medium_waste_alerts': len([a for a in expiry_alerts if a['alert_severity'] == 'medium']),
                'low_waste_alerts': len([a for a in expiry_alerts if a['alert_severity'] == 'low']),
                'total_waste_value': round(total_waste_value, 2),
                'total_waste_amount': round(total_waste_items, 2)
            },
            'ml_model_called': True,
            'prediction_period_days': 7
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def _calculate_expiry_waste(active_restocks, daily_consumption):
    """Calculate how much stock will expire unused over 7 days"""
    
    # Sort restocks by expiry date to process FIFO
    sorted_restocks = sorted(active_restocks, key=lambda x: x['date'])
    
    # Create a copy of restocks to track consumption
    restocks_tracker = []
    for restock in sorted_restocks:
        expiry_date = restock['expiry_date']
        if isinstance(expiry_date, str):
            expiry_date = datetime.fromisoformat(expiry_date.replace('Z', '+00:00'))
        
        restocks_tracker.append({
            'items_left': restock['items_left'],
            'expiry_date': expiry_date,
            'restock_date': restock['date'],
            'original_amount': restock['items_left']
        })
    
    expiry_timeline = []
    total_waste_amount = 0
    consumption_vs_expiry = []
    
    # Simulate day by day for 7 days
    for day in range(7):
        current_date = datetime.now() + timedelta(days=day)
        daily_need = daily_consumption[day]
        daily_consumed = 0
        
        # Consume from available stock using FIFO (oldest first)
        for restock in restocks_tracker:
            if daily_consumed >= daily_need:
                break
            
            if restock['items_left'] > 0 and restock['expiry_date'] > current_date:
                # Can consume from this restock
                consume_amount = min(daily_need - daily_consumed, restock['items_left'])
                restock['items_left'] -= consume_amount
                daily_consumed += consume_amount
        
        # Check for expired stock at end of day
        expired_today = []
        for restock in restocks_tracker:
            if restock['expiry_date'].date() == current_date.date() and restock['items_left'] > 0:
                expired_today.append({
                    'amount': restock['items_left'],
                    'expiry_date': restock['expiry_date'].strftime('%Y-%m-%d'),
                    'days_from_now': day
                })
                total_waste_amount += restock['items_left']
                restock['items_left'] = 0  # Mark as expired/wasted
        
        if expired_today:
            expiry_timeline.extend(expired_today)
        
        consumption_vs_expiry.append({
            'day': day + 1,
            'date': current_date.strftime('%Y-%m-%d'),
            'consumption': daily_need,
            'actually_consumed': daily_consumed,
            'expired_today': sum(item['amount'] for item in expired_today)
        })
    
    # Check for any remaining stock that will expire after 7 days
    remaining_stock_total = sum(restock['items_left'] for restock in restocks_tracker)
    
    # Calculate waste percentage
    original_total = sum(restock['original_amount'] for restock in restocks_tracker)
    waste_percentage = (total_waste_amount / original_total * 100) if original_total > 0 else 0
    
    # Generate recommendations
    recommendations = _generate_expiry_recommendations(
        total_waste_amount, 
        waste_percentage,
        consumption_vs_expiry
    )
    
    return {
        'has_expiry_waste': total_waste_amount > 0,
        'total_waste_amount': round(total_waste_amount, 2),
        'waste_value': 0,  # Will be calculated in main function with price
        'waste_percentage': round(waste_percentage, 2),
        'expiry_timeline': expiry_timeline,
        'consumption_vs_expiry': consumption_vs_expiry,
        'remaining_stock_after_7_days': round(remaining_stock_total, 2),
        'recommendations': recommendations
    }

def _get_expiry_alert_severity(waste_percentage, waste_value):
    """Determine expiry alert severity based on waste percentage and value"""
    if waste_percentage >= 50 or waste_value >= 50:
        return 'high'      # High waste (50%+ or $50+ waste)
    elif waste_percentage >= 25 or waste_value >= 20:
        return 'medium'    # Medium waste (25-49% or $20-49 waste)
    else:
        return 'low'       # Low waste (under 25% or under $20 waste)

def _generate_expiry_recommendations(waste_amount, waste_percentage, consumption_timeline):
    """Generate recommendations to reduce expiry waste"""
    recommendations = []
    
    if waste_percentage > 30:
        recommendations.append("Consider reducing order quantities for this ingredient")
    
    if waste_amount > 5:
        recommendations.append(f"Plan promotions or menu changes to use {waste_amount:.1f} units before expiry")
    
    # Check if consumption is consistently low
    avg_consumption = sum(day['consumption'] for day in consumption_timeline) / len(consumption_timeline)
    if avg_consumption < 2:
        recommendations.append("Low daily usage - consider ordering smaller quantities more frequently")
    
    # Check if there are days with high waste
    high_waste_days = [day for day in consumption_timeline if day['expired_today'] > 2]
    if high_waste_days:
        recommendations.append("Focus on FIFO inventory rotation - older stock not being used first")
    
    if not recommendations:
        recommendations.append("Monitor consumption patterns to optimize ordering")
    
    return recommendations


@alert_bp.route('/api/stock_alert', methods=['GET'])
def get_stock_alert():
    """Get alert about the stock of the ingredients"""
    try:
        # endpoint = zhuheng endpoint
        # try: 
        #     ml_response = request.post(ml_model_url, json={
        #         'prediction_days': 7,
        #     }, timeout=30)
            
        #     if ml_response.status_code != 200:
        #         return jsonify({
        #             'error': f'ML model API returned status {ml_response.status_code}',
        #             'details': ml_response.text
        #         }), 500
            
        #     ml_data = ml_response.json()
            
        #     if 'ingredient_consumption' not in ml_data:
        #         return jsonify({'error': 'ML model response missing ingredient_consumption field'}), 500
        
        #     predicted_consumption = ml_data['ingredient_consumption'] 
        # except Exception as e:
        #     return jsonify({'error': f'Failed to call ML model: {str(e)}'}), 500

        _, _, df_ingredients, _, _ = run()
        predicted_consumption = df_ingredients

        alerts = []
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
                            'cond': {
                                '$and': [
                                    {'$gt': ['$this.items_left', 0]},
                                    {'$gte': ['$this.expiry_date', datetime.now()]},
                                    {'$eq': ['$this.clear', False]}
                                ]
                            }
                        }
                    }
                }
            }
        ]
        
        ingredients = list(db.ingredients.aggregate(pipeline))
         # Step 3: For each ingredient, check if stock is sufficient for 7 days
        for ingredient in ingredients:
            ingredient_id = str(ingredient['_id'])
            
            if ingredient_id not in predicted_consumption:
                continue
            
            daily_consumption = predicted_consumption[ingredient_id]
            
            # Validate daily consumption format
            if not isinstance(daily_consumption, list) or len(daily_consumption) != 7:
                continue
            
            total_needed = sum(daily_consumption)
            current_stock = ingredient.get('current_stock', 0)
            
            # Calculate available stock considering FIFO and expiry
            available_stock_by_day = _calculate_daily_available_stock(ingredient['active_restocks'])
            
            # Simulate consumption day by day
            depletion_info = _simulate_daily_consumption(
                current_stock,
                available_stock_by_day,
                daily_consumption
            )
            
            # Create alert if stock will be insufficient
            if depletion_info['insufficient']:
                alert = {
                    'ingredient_id': ingredient_id,
                    'name': ingredient['name'],
                    'unit': ingredient['unit'],
                    'current_stock': current_stock,
                    'total_consumption_7_days': total_needed,
                    'depletion_date': depletion_info['depletion_date'],
                    'days_until_depletion': depletion_info['days_until_depletion'],
                    'shortage_amount': depletion_info['shortage_amount'],
                    'daily_forecast': daily_consumption,
                    'alert_severity': _get_alert_severity(depletion_info['days_until_depletion']),
                    'recommended_restock_amount': max(total_needed - current_stock, 0)
                }
                alerts.append(alert)
        
        # Sort alerts by urgency (soonest depletion first)
        alerts.sort(key=lambda x: x['days_until_depletion'])
        
        return jsonify({
            'success': True,
            'alerts': alerts,
            'summary': {
                'total_alerts': len(alerts),
                'critical_alerts': len([a for a in alerts if a['alert_severity'] == 'critical']),
                'high_priority_alerts': len([a for a in alerts if a['alert_severity'] == 'high']),
                'medium_priority_alerts': len([a for a in alerts if a['alert_severity'] == 'medium'])
            },
            'ml_model_called': True,
            'prediction_period_days': 7
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def _calculate_daily_available_stock(active_restocks):
    """Calculate how much stock becomes unavailable each day due to expiry"""
    daily_expiry = {}
    
    for restock in active_restocks:
        expiry_date = restock['expiry_date']
        if isinstance(expiry_date, str):
            expiry_date = datetime.fromisoformat(expiry_date.replace('Z', '+00:00'))
        
        # Calculate which day (0-6) this stock expires
        days_until_expiry = (expiry_date.date() - datetime.now().date()).days
        
        if 0 <= days_until_expiry <= 7:
            if days_until_expiry not in daily_expiry:
                daily_expiry[days_until_expiry] = 0
            daily_expiry[days_until_expiry] += restock['items_left']
    
    return daily_expiry

def _simulate_daily_consumption(current_stock, daily_expiry, daily_consumption):
    """Simulate consumption day by day and find depletion point"""
    remaining_stock = current_stock
    
    for day in range(7):  # Days 0-6
        # Remove expired stock at start of day
        if day in daily_expiry:
            remaining_stock -= daily_expiry[day]
        
        # Consume daily requirement
        daily_need = daily_consumption[day]
        remaining_stock -= daily_need
        
        # Check if depleted
        if remaining_stock < 0:
            # Calculate the exact date of depletion
            depletion_date = (datetime.now() + timedelta(days=day + 1)).strftime('%Y-%m-%d')
            
            return {
                'insufficient': True,
                'depletion_date': depletion_date,
                'days_until_depletion': day + 1,
                'shortage_amount': abs(remaining_stock),
                'final_stock': remaining_stock
            }
    
    # Stock is sufficient for 7 days
    return {
        'insufficient': remaining_stock < 0,
        'depletion_date': None,
        'days_until_depletion': None,
        'shortage_amount': 0,
        'final_stock': remaining_stock
    }

def _get_alert_severity(days_until_depletion):
    """Determine alert severity based on days until depletion"""
    if days_until_depletion is None:
        return 'none'
    elif days_until_depletion <= 1:
        return 'critical'  # Depletes today or tomorrow
    elif days_until_depletion <= 3:
        return 'high'      # Depletes in 2-3 days
    elif days_until_depletion <= 5:
        return 'medium'    # Depletes in 4-5 days
    else:
        return 'low'       # Depletes in 6-7 days
    
    
    