import os
import json
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from flask import Blueprint, request, jsonify

# Set AWS credentials (replace with your actual IAM credentials)
os.environ["AWS_ACCESS_KEY_ID"] = "AKIAVFRRC6O4ROVMS3EM"
os.environ["AWS_SECRET_ACCESS_KEY"] = "m5T83NpDPzbhUVQuDZDbn2FSEcJaQXIcOdsj5AfP"
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

class BedrockService:
    def __init__(self):
        """Initialize Bedrock client with credentials from config"""
        try:
            self.client = boto3.client(
                'bedrock-runtime',
                region_name='us-east1'
            )
            self.model_id = 'us.amazon.nova-pro-v1:0'
        except Exception as e:
            print(f"Error initializing Bedrock client: {e}")
            self.client = None

    def call_nova(self, system_prompt, user_prompt, max_tokens=4000, temperature=0.7):
        """
        Call Amazon Nova model via Bedrock
        
        Args:
            system_prompt (str): System instructions for the model
            user_prompt (str): The user prompt/request
            max_tokens (int): Maximum tokens to generate
            temperature (float): Temperature for generation (0.0-1.0)
        
        Returns:
            dict: Response with success status and content or error
        """
        if not self.client:
            return {
                'success': False,
                'error': 'Bedrock client not initialized. Check AWS credentials.'
            }

        try:
            # Prepare the request body for Nova
            body = {
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "text": f"<system_instruction>\n{system_prompt}\n</system_instruction>\n\n{user_prompt}"
                            }
                        ]
                    }
                ],
                "inferenceConfig": {
                    "max_new_tokens": max_tokens,
                    "temperature": temperature
                }
            }

            # Call Bedrock
            response = self.client.invoke_model(
                modelId=self.model_id,
                contentType='application/json',
                accept='application/json',
                body=json.dumps(body)
            )

            # Parse response
            response_body = json.loads(response['body'].read())
            
            if response_body.get('output') and response_body['output'].get('message'):
                content = response_body['output']['message']['content'][0]['text']
                return {
                    'success': True,
                    'content': content,
                    'usage': response_body.get('usage', {}),
                    'model_id': self.model_id
                }
            else:
                return {
                    'success': False,
                    'error': 'Empty response from model'
                }
        except Exception as e:
            return {
                'success': False,
                'error': f'Unexpected error: {str(e)}'
            }

    def generate_recipes(self, ingredient_data):
        """
        Generate recipes based on ingredient data
        
        Args:
            ingredient_data (dict): Ingredient information including ID, name, stock, etc.
        
        Returns:
            dict: Generated recipes or error
        """
        
        # System instruction for recipe generation
        system_instruction = """
You are an expert chef and culinary AI assistant. Your task is to create delicious, practical recipes that highlight specific ingredients provided by the user

CORE RESPONSIBILITIES:
1. Ensure recipes are practical for commercial kitchen implementation
2. Provide detailed, step-by-step cooking instructions
3. Consider ingredient quantities, cooking techniques, and presentation

OUTPUT REQUIREMENTS:
- Always respond in valid JSON format only
- No additional text, explanations, or markdown formatting outside the JSON
- Include detailed, step-by-step recipes with precise measurements
- Focus on recipes that maximize the use of the specified ingredient
- Ensure all recipes are commercially viable

QUALITY STANDARDS:
- Recipes must be authentic and delicious
- Portions should be restaurant-appropriate (serving 2-4 people)
- Include proper cooking times, temperatures, and techniques
- All suggestions must be practical for professional kitchen implementation
"""

        user_prompt = f"""
Based on the following ingredient information, generate creative recipes that highlight this ingredient:

Ingredient Information:
{json.dumps(ingredient_data, indent=2)}

Generate a response in this EXACT JSON format:

{{
    "recipes": [
        {{
            "name": "Recipe Name",
            "cuisine_type": "Italian/Asian/American/etc",
            "difficulty": "Easy/Medium/Hard",
            "cook_time_minutes": 30,
            "servings": 2,
            "primary_ingredient": "ingredient_id_from_input",
            "ingredients": [
                {{
                    "ingredient_id": "id_if_available",
                    "name": "ingredient name",
                    "quantity": 200,
                    "unit": "grams/pieces/ml",
                    "notes": "preparation notes if any"
                }}
            ],
            "instructions": [
                "Step 1: Detailed instruction...",
                "Step 2: Detailed instruction...",
                "Step 3: Detailed instruction..."
            ],
            "estimated_cost": 12.50,
            "suggested_selling_price": 18.00,
            "profit_margin_percent": 30.6,
        }}
    ]
}}

IMPORTANT: Return ONLY the JSON response. No other text, explanations, or formatting.
"""

        response = self.call_nova(
            system_prompt=system_instruction,
            user_prompt=user_prompt,
            max_tokens=2500,
            temperature=0.4
        )
        
        if not response['success']:
            return response
        
        # Try to parse the JSON response
        try:
            content = response['content'].strip()
            # Remove any potential markdown code blocks
            if content.startswith('```json'):
                content = content[7:]
            if content.endswith('```'):
                content = content[:-3]
            
            parsed_data = json.loads(content)
            
            return {
                'success': True,
                'recipes': parsed_data.get('recipes', []),
                'raw_response': response['content'],
                'model_usage': response.get('usage', {})
            }
            
        except json.JSONDecodeError as e:
            return {
                'success': False,
                'error': f'Failed to parse model response as JSON: {str(e)}',
                'raw_response': response['content']
            }

    def generate_discount_plans(self, ingredient_data, recipe_ids=None):
        """
        Generate discount plans based on ingredient data and optional recipe IDs
        
        Args:
            ingredient_data (dict): Ingredient information including ID, name, stock, etc.
            recipe_ids (list): Optional list of recipe IDs to create discount plans for
        
        Returns:
            dict: Generated discount plans or error
        """
        
        # System instruction for discount plan generation
        system_instruction = """
You are an expert restaurant marketing strategist and pricing analyst. Your task is to create compelling discount and promotional campaigns that help restaurants move inventory while maintaining profitability.

CORE RESPONSIBILITIES:
1. Create strategic discount plans that balance customer appeal with business profitability
2. Design promotions that increase ingredient usage and reduce waste
3. Ensure all discount strategies are financially viable for restaurants
4. Provide comprehensive marketing strategies with clear implementation guidelines

OUTPUT REQUIREMENTS:
- Always respond in valid JSON format only
- No additional text, explanations, or markdown formatting outside the JSON
- Include specific discount percentages, timeframes, and conditions
- Focus on promotions that will increase usage of the specified ingredient
- Ensure all plans are practical for restaurant implementation

QUALITY STANDARDS:
- Discount plans should maintain 15-35% profit margins
- Promotions should be attractive to customers but sustainable for business
- Include clear marketing messages and implementation strategies
- Consider timing, target audience, and competitive factors
"""

        recipe_context = ""
        if recipe_ids:
            recipe_context = f"\nRelated Recipe IDs to promote: {recipe_ids}"

        user_prompt = f"""
Based on the following ingredient information, create strategic discount and promotional plans:

Ingredient Information:
{json.dumps(ingredient_data, indent=2)}
{recipe_context}

Generate a response in this EXACT JSON format:

{{
    "discount_plans": [
        {{
            "name": "Promotion Name",
            "target_ingredient": "ingredient_id",
            "applicable_dishes": ["dish_name_1", "dish_name_2"],
            "discount_details": {{
                "percentage": 20,
                "fixed_amount": 0,
                "minimum_order": 25.00,
                "maximum_discount": 10.00
            }},
            "duration": {{
                "start_date": "2025-09-22",
                "end_date": "2025-09-29",
                "days_of_week": ["Monday", "Tuesday", "Wednesday"],
                "time_slots": ["lunch", "dinner"]
            }},
        }}
    ]
}}

IMPORTANT: Return ONLY the JSON response. No other text, explanations, or formatting.
"""

        response = self.call_nova(
            system_prompt=system_instruction,
            user_prompt=user_prompt,
            max_tokens=2000,
            temperature=0.4
        )
        
        if not response['success']:
            return response
        
        # Try to parse the JSON response
        try:
            content = response['content'].strip()
            # Remove any potential markdown code blocks
            if content.startswith('```json'):
                content = content[7:]
            if content.endswith('```'):
                content = content[:-3]
            
            parsed_data = json.loads(content)
            
            return {
                'success': True,
                'discount_plans': parsed_data.get('discount_plans', []),
                'raw_response': response['content'],
                'model_usage': response.get('usage', {})
            }
            
        except json.JSONDecodeError as e:
            return {
                'success': False,
                'error': f'Failed to parse model response as JSON: {str(e)}',
                'raw_response': response['content']
            }

bedrock_service = BedrockService()