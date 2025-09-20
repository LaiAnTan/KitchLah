from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
uri = os.getenv('MONGO_URI')

client = MongoClient(uri)
db = client.Kitchlah_db
stations_coll = db.stations
ingredients_coll = db.ingredients
items_coll = db.items

prep = {
	"name": "Prep Station",
	"capacity": 3
}
grill = {
	"name": "Grill Station",
	"capacity": 2
}
fryer = {
	"name": "Fryer Station",
	"capacity": 1
}
stove = {
	"name": "Stove Station",
	"capacity": 4
}
assembly = {
	"name": "Assembly Station",
	"capacity": 3
}

# Ingredient definitions
bun = {
	"name": "Burger Bun",
	"unit": "piece",
	"stock_quantity": 500,
	"reorder_level": 50,
	"cost_per_unit": 0.35
}

patty_chicken = {
	"name": "Chicken Patty",
	"unit": "piece",
	"stock_quantity": 200,
	"reorder_level": 30,
	"cost_per_unit": 2.50
}

lettuce = {
	"name": "Fresh Lettuce",
	"unit": "grams",
	"stock_quantity": 2000,
	"reorder_level": 300,
	"cost_per_unit": 0.008
}

tomato = {
	"name": "Fresh Tomato",
	"unit": "grams",
	"stock_quantity": 3000,
	"reorder_level": 500,
	"cost_per_unit": 0.012
}

onion = {
	"name": "Yellow Onion",
	"unit": "grams",
	"stock_quantity": 2500,
	"reorder_level": 400,
	"cost_per_unit": 0.005
}

mayonaise = {
	"name": "Mayonnaise",
	"unit": "ml",
	"stock_quantity": 1000,
	"reorder_level": 150,
	"cost_per_unit": 0.015
}

fries = {
	"name": "Frozen French Fries",
	"unit": "grams",
	"stock_quantity": 5000,
	"reorder_level": 800,
	"cost_per_unit": 0.004
}

oil = {
	"name": "Cooking Oil",
	"unit": "ml",
	"stock_quantity": 5000,
	"reorder_level": 1000,
	"cost_per_unit": 0.01
}

# Fish n Chips ingredients
white_fish = {
	"name": "White Fish Fillet",
	"unit": "piece",
	"stock_quantity": 100,
	"reorder_level": 20,
	"cost_per_unit": 4.50
}

flour = {
	"name": "All-Purpose Flour",
	"unit": "grams",
	"stock_quantity": 5000,
	"reorder_level": 800,
	"cost_per_unit": 0.002
}

egg = {
	"name": "Eggs",
	"unit": "piece",
	"stock_quantity": 200,
	"reorder_level": 30,
	"cost_per_unit": 0.25
}

breadcrumbs = {
	"name": "Breadcrumbs",
	"unit": "grams",
	"stock_quantity": 2000,
	"reorder_level": 300,
	"cost_per_unit": 0.003
}

tartar_sauce = {
	"name": "Tartar Sauce",
	"unit": "ml",
	"stock_quantity": 1000,
	"reorder_level": 150,
	"cost_per_unit": 0.02
}

lemon = {
	"name": "Fresh Lemon",
	"unit": "piece",
	"stock_quantity": 50,
	"reorder_level": 10,
	"cost_per_unit": 0.30
}

# Spaghetti ingredients
spaghetti_pasta = {
	"name": "Spaghetti Pasta",
	"unit": "grams",
	"stock_quantity": 10000,
	"reorder_level": 1500,
	"cost_per_unit": 0.003
}

olive_oil = {
	"name": "Olive Oil",
	"unit": "ml",
	"stock_quantity": 2000,
	"reorder_level": 300,
	"cost_per_unit": 0.015
}

garlic = {
	"name": "Fresh Garlic",
	"unit": "grams",
	"stock_quantity": 500,
	"reorder_level": 100,
	"cost_per_unit": 0.01
}

minced_beef = {
	"name": "Minced Beef",
	"unit": "grams",
	"stock_quantity": 2000,
	"reorder_level": 400,
	"cost_per_unit": 0.015
}

minced_chicken = {
	"name": "Minced Chicken",
	"unit": "grams",
	"stock_quantity": 2000,
	"reorder_level": 400,
	"cost_per_unit": 0.012
}

bacon = {
	"name": "Bacon Strips",
	"unit": "grams",
	"stock_quantity": 1000,
	"reorder_level": 200,
	"cost_per_unit": 0.018
}

tomato_sauce = {
	"name": "Tomato Sauce",
	"unit": "ml",
	"stock_quantity": 3000,
	"reorder_level": 500,
	"cost_per_unit": 0.008
}

cream_sauce = {
	"name": "Cream Sauce",
	"unit": "ml",
	"stock_quantity": 2000,
	"reorder_level": 300,
	"cost_per_unit": 0.012
}

parmesan_cheese = {
	"name": "Parmesan Cheese",
	"unit": "grams",
	"stock_quantity": 1000,
	"reorder_level": 150,
	"cost_per_unit": 0.025
}

# Chicken Chop ingredients
chicken_breast = {
	"name": "Chicken Breast",
	"unit": "piece",
	"stock_quantity": 150,
	"reorder_level": 30,
	"cost_per_unit": 3.50
}

chicken_thigh = {
	"name": "Chicken Thigh",
	"unit": "piece",
	"stock_quantity": 120,
	"reorder_level": 25,
	"cost_per_unit": 2.80
}

seasoning_mix = {
	"name": "Seasoning Mix",
	"unit": "grams",
	"stock_quantity": 500,
	"reorder_level": 100,
	"cost_per_unit": 0.015
}

mushroom_sauce = {
	"name": "Mushroom Sauce",
	"unit": "ml",
	"stock_quantity": 1500,
	"reorder_level": 250,
	"cost_per_unit": 0.018
}

black_pepper_sauce = {
	"name": "Black Pepper Sauce",
	"unit": "ml",
	"stock_quantity": 1500,
	"reorder_level": 250,
	"cost_per_unit": 0.016
}

mashed_potato = {
	"name": "Mashed Potato",
	"unit": "grams",
	"stock_quantity": 3000,
	"reorder_level": 500,
	"cost_per_unit": 0.006
}

mixed_salad = {
	"name": "Mixed Salad",
	"unit": "grams",
	"stock_quantity": 2000,
	"reorder_level": 300,
	"cost_per_unit": 0.008
}



# Insert stations and capture their ObjectIds
stations_result = stations_coll.insert_many([
	prep, grill, fryer, stove, assembly
])

# Create mapping from station names to their ObjectIds
station_ids = {
	"prep": stations_result.inserted_ids[0],
	"grill": stations_result.inserted_ids[1],
	"fryer": stations_result.inserted_ids[2],
	"stove": stations_result.inserted_ids[3],
	"assembly": stations_result.inserted_ids[4]
}

# Insert ingredients and capture their ObjectIds
ingredient_result = ingredients_coll.insert_many([
	bun, patty_chicken, lettuce, tomato, onion, mayonaise, fries, oil,
	# Fish n Chips ingredients
	white_fish, flour, egg, breadcrumbs, tartar_sauce, lemon,
	# Spaghetti ingredients
	spaghetti_pasta, olive_oil, garlic, minced_beef, minced_chicken, bacon, 
	tomato_sauce, cream_sauce, parmesan_cheese,
	# Chicken Chop ingredients
	chicken_breast, chicken_thigh, seasoning_mix, mushroom_sauce, 
	black_pepper_sauce, mashed_potato, mixed_salad
])

# Create mapping from ingredient names to their ObjectIds
ingredient_ids = {
	"bun": ingredient_result.inserted_ids[0],
	"patty_chicken": ingredient_result.inserted_ids[1],
	"lettuce": ingredient_result.inserted_ids[2],
	"tomato": ingredient_result.inserted_ids[3],
	"onion": ingredient_result.inserted_ids[4],
	"mayonaise": ingredient_result.inserted_ids[5],
	"fries": ingredient_result.inserted_ids[6],
	"oil": ingredient_result.inserted_ids[7],
	# Fish n Chips ingredients
	"white_fish": ingredient_result.inserted_ids[8],
	"flour": ingredient_result.inserted_ids[9],
	"egg": ingredient_result.inserted_ids[10],
	"breadcrumbs": ingredient_result.inserted_ids[11],
	"tartar_sauce": ingredient_result.inserted_ids[12],
	"lemon": ingredient_result.inserted_ids[13],
	# Spaghetti ingredients
	"spaghetti_pasta": ingredient_result.inserted_ids[14],
	"olive_oil": ingredient_result.inserted_ids[15],
	"garlic": ingredient_result.inserted_ids[16],
	"minced_beef": ingredient_result.inserted_ids[17],
	"minced_chicken": ingredient_result.inserted_ids[18],
	"bacon": ingredient_result.inserted_ids[19],
	"tomato_sauce": ingredient_result.inserted_ids[20],
	"cream_sauce": ingredient_result.inserted_ids[21],
	"parmesan_cheese": ingredient_result.inserted_ids[22],
	# Chicken Chop ingredients
	"chicken_breast": ingredient_result.inserted_ids[23],
	"chicken_thigh": ingredient_result.inserted_ids[24],
	"seasoning_mix": ingredient_result.inserted_ids[25],
	"mushroom_sauce": ingredient_result.inserted_ids[26],
	"black_pepper_sauce": ingredient_result.inserted_ids[27],
	"mashed_potato": ingredient_result.inserted_ids[28],
	"mixed_salad": ingredient_result.inserted_ids[29]
}

# Define menu items using the actual MongoDB ObjectIds
burger_and_fries = {
	"name": "Burger and Fries",
	"ingredients": [
		{ "ingredient_id": ingredient_ids["bun"], "quantity": 1, "unit": "piece" },
		{ "ingredient_id": ingredient_ids["patty_chicken"], "quantity": 1, "unit": "piece" },
		{ "ingredient_id": ingredient_ids["lettuce"], "quantity": 30, "unit": "grams" },
		{ "ingredient_id": ingredient_ids["tomato"], "quantity": 20, "unit": "grams" },
		{ "ingredient_id": ingredient_ids["onion"], "quantity": 15, "unit": "grams" },
		{ "ingredient_id": ingredient_ids["mayonaise"], "quantity": 10, "unit": "ml" },
		{ "ingredient_id": ingredient_ids["fries"], "quantity": 150, "unit": "grams" },
		{ "ingredient_id": ingredient_ids["oil"], "quantity": 50, "unit": "ml" }
	],
	"workflow": [
		{
			"station_id": station_ids["prep"],
			"task_name": "Prepare bun and veggies",
			"duration": 2,
		},
		{
			"station_id": station_ids["grill"],
			"task_name": "Grill patty",
			"duration": 6
		},
		{
			"station_id": station_ids["fryer"],
			"task_name": "Fry fries",
			"duration": 4
		},
		{
			"station_id": station_ids["assembly"],
			"task_name": "Plate dish",
			"duration": 2
		}
	],
	"total_time": 14
}

fish_and_chips = {
	"name": "Fish and Chips",
	"ingredients": [
		{ "ingredient_id": ingredient_ids["white_fish"], "quantity": 1, "unit": "piece" },
		{ "ingredient_id": ingredient_ids["flour"], "quantity": 100, "unit": "grams" },
		{ "ingredient_id": ingredient_ids["egg"], "quantity": 1, "unit": "piece" },
		{ "ingredient_id": ingredient_ids["breadcrumbs"], "quantity": 50, "unit": "grams" },
		{ "ingredient_id": ingredient_ids["fries"], "quantity": 200, "unit": "grams" },
		{ "ingredient_id": ingredient_ids["tartar_sauce"], "quantity": 30, "unit": "ml" },
		{ "ingredient_id": ingredient_ids["lemon"], "quantity": 0.25, "unit": "piece" },
		{ "ingredient_id": ingredient_ids["oil"], "quantity": 100, "unit": "ml" }
	],
	"workflow": [
		{
			"station_id": station_ids["prep"],
			"task_name": "Coat fish in batter",
			"duration": 2,
		},
		{
			"station_id": station_ids["fryer"],
			"task_name": "Fry fish",
			"duration": 6
		},
		{
			"station_id": station_ids["fryer"],
			"task_name": "Fry fries",
			"duration": 4
		},
		{
			"station_id": station_ids["assembly"],
			"task_name": "Plate with tartar sauce and lemon",
			"duration": 1
		}
	],
	"total_time": 13
}

spaghetti_bolognese = {
	"name": "Spaghetti Bolognese",
	"ingredients": [
		{ "ingredient_id": ingredient_ids["spaghetti_pasta"], "quantity": 120, "unit": "grams" },
		{ "ingredient_id": ingredient_ids["olive_oil"], "quantity": 15, "unit": "ml" },
		{ "ingredient_id": ingredient_ids["garlic"], "quantity": 10, "unit": "grams" },
		{ "ingredient_id": ingredient_ids["onion"], "quantity": 30, "unit": "grams" },
		{ "ingredient_id": ingredient_ids["minced_beef"], "quantity": 100, "unit": "grams" },
		{ "ingredient_id": ingredient_ids["tomato_sauce"], "quantity": 80, "unit": "ml" },
		{ "ingredient_id": ingredient_ids["parmesan_cheese"], "quantity": 20, "unit": "grams" }
	],
	"workflow": [
		{
			"station_id": station_ids["prep"],
			"task_name": "Chop onions and garlic",
			"duration": 3,
		},
		{
			"station_id": station_ids["stove"],
			"task_name": "Boil spaghetti",
			"duration": 10
		},
		{
			"station_id": station_ids["stove"],
			"task_name": "Cook sauce with meat",
			"duration": 6
		},
		{
			"station_id": station_ids["assembly"],
			"task_name": "Mix pasta with sauce and plate",
			"duration": 1
		}
	],
	"total_time": 20
}

chicken_chop = {
	"name": "Chicken Chop with Black Pepper Sauce",
	"ingredients": [
		{ "ingredient_id": ingredient_ids["chicken_thigh"], "quantity": 1, "unit": "piece" },
		{ "ingredient_id": ingredient_ids["seasoning_mix"], "quantity": 10, "unit": "grams" },
		{ "ingredient_id": ingredient_ids["black_pepper_sauce"], "quantity": 50, "unit": "ml" },
		{ "ingredient_id": ingredient_ids["fries"], "quantity": 150, "unit": "grams" },
		{ "ingredient_id": ingredient_ids["mixed_salad"], "quantity": 80, "unit": "grams" },
		{ "ingredient_id": ingredient_ids["oil"], "quantity": 30, "unit": "ml" }
	],
	"workflow": [
		{
			"station_id": station_ids["prep"],
			"task_name": "Season chicken",
			"duration": 1,
		},
		{
			"station_id": station_ids["grill"],
			"task_name": "Grill chicken",
			"duration": 8
		},
		{
			"station_id": station_ids["fryer"],
			"task_name": "Fry fries",
			"duration": 4
		},
		{
			"station_id": station_ids["stove"],
			"task_name": "Heat sauce",
			"duration": 2
		},
		{
			"station_id": station_ids["assembly"],
			"task_name": "Plate chicken with sauce and sides",
			"duration": 1
		}
	],
	"total_time": 16
}

# Insert menu items and capture their ObjectIds
items_result = items_coll.insert_many([burger_and_fries, fish_and_chips, spaghetti_bolognese, chicken_chop])

# Create mapping from menu item names to their ObjectIds
item_ids = {
	"burger_and_fries": items_result.inserted_ids[0],
	"fish_and_chips": items_result.inserted_ids[1],
	"spaghetti_bolognese": items_result.inserted_ids[2],
	"chicken_chop": items_result.inserted_ids[3]
}

# Define multiple realistic orders using the actual MongoDB ObjectIds
order1 = {
	"datetime": str(datetime(2025, 9, 20, 12, 15, 30)),  # Lunch time
	"items": [
		{
			"item_id": item_ids["burger_and_fries"],
			"quantity": 1,
			"remarks": None
		},
		{
			"item_id": item_ids["fish_and_chips"],
			"quantity": 2,
			"remarks": None
		}
	]
}

order2 = {
	"datetime": str(datetime(2025, 9, 20, 18, 45, 12)),  # Dinner time
	"items": [
		{
			"item_id": item_ids["spaghetti_bolognese"],
			"quantity": 1,
			"remarks": "Extra cheese please"
		},
		{
			"item_id": item_ids["chicken_chop"],
			"quantity": 1,
			"remarks": "Medium well done"
		}
	]
}

order3 = {
	"datetime": str(datetime(2025, 9, 20, 14, 20, 45)),  # Afternoon snack
	"items": [
		{
			"item_id": item_ids["fish_and_chips"],
			"quantity": 3,
			"remarks": "Extra tartar sauce"
		}
	]
}

order4 = {
	"datetime": str(datetime(2025, 9, 20, 19, 30, 8)),   # Peak dinner rush
	"items": [
		{
			"item_id": item_ids["burger_and_fries"],
			"quantity": 2,
			"remarks": "No onions"
		},
		{
			"item_id": item_ids["spaghetti_bolognese"],
			"quantity": 1,
			"remarks": None
		},
		{
			"item_id": item_ids["chicken_chop"],
			"quantity": 1,
			"remarks": "Mushroom sauce instead of black pepper"
		}
	]
}

order5 = {
	"datetime": str(datetime(2025, 9, 20, 13, 5, 22)),   # Late lunch
	"items": [
		{
			"item_id": item_ids["chicken_chop"],
			"quantity": 2,
			"remarks": "Well done, extra salad"
		},
		{
			"item_id": item_ids["fish_and_chips"],
			"quantity": 1,
			"remarks": "Crispy fries"
		}
	]
}

order6 = {
	"datetime": str(datetime(2025, 9, 20, 17, 15, 55)),  # Early dinner family order
	"items": [
		{
			"item_id": item_ids["spaghetti_bolognese"],
			"quantity": 4,
			"remarks": "Family portion, light sauce"
		}
	]
}

order7 = {
	"datetime": str(datetime(2025, 9, 20, 20, 10, 33)),  # Late dinner group order
	"items": [
		{
			"item_id": item_ids["burger_and_fries"],
			"quantity": 1,
			"remarks": "Extra mayo"
		},
		{
			"item_id": item_ids["fish_and_chips"],
			"quantity": 1,
			"remarks": None
		},
		{
			"item_id": item_ids["spaghetti_bolognese"],
			"quantity": 1,
			"remarks": "Al dente pasta"
		},
		{
			"item_id": item_ids["chicken_chop"],
			"quantity": 1,
			"remarks": "Mashed potato side"
		}
	]
}

# Create orders collection reference
orders_coll = db.orders

# Insert all orders into the database
orders_coll.insert_many([order1, order2, order3, order4, order5, order6, order7])

client.close()