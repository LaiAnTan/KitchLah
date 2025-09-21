# recipes.py

from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
uri = os.getenv("MONGODB_URI")

client = MongoClient(uri)
db = client.kitchlah_db
items_coll = db.items
ingredients_coll = db.ingredients

# -------------------- Recipe definitions --------------------
# RECIPE = {
#     "Burger and Fries": {"chicken_patty_count":1, "fries":200, "bun_count":1, "lettuce":20},
#     "Fish and Chips": {"fish_count":2, "fries":200, "batter":80},
#     "Spaghetti Bolognese": {"pasta":120, "sauce":90, "cheese":10},
#     "Chicken Chop with Black Pepper Sauce": {"chicken_count":1, "sauce":60, "fries":150}
# }

def load_recipes():
    recipes = {}
    menu = []

    # Load all menu items from items collection
    items = items_coll.find()
    for item in items:
        menu_name = item["name"]
        menu.append(menu_name)

        recipe = {}
        for ing in item["ingredients"]:
            recipe[ing["ingredient_id"]] = ing["quantity"]

        recipes[menu_name] = recipe
    return recipes, menu

RECIPE, MENU = load_recipes()
print(RECIPE, MENU)

# key = name of menu item, value = dict of ingredients and per-unit quantities
# MENU = list(RECIPE.keys())

# -------------------- Orders to ingredient calculation --------------------
def orders_to_ingredients(pred_orders):
    out = {}
    for menu, count in pred_orders.items():
        for ing, per_unit in RECIPE[menu].items():
            out[ing] = out.get(ing, 0) + per_unit * count
    return out
