from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
uri = os.getenv('MONGODB_URI')

client = MongoClient(uri)
db = client.kitchlah_db
stations_coll = db.stations
ingredients_coll = db.ingredients
items_coll = db.items
orders_coll = db.orders
restork_coll = db.restocks

stations_coll.delete_many({})
ingredients_coll.delete_many({})
items_coll.delete_many({})
orders_coll.delete_many({})
restork_coll.delete_many({})

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
    "best_used_days": 5,  # bread shelf life
    "price_per_unit": 0.35,
    "unit": "piece",
    "current_stock": 500,
    "last_restock_date": "2025-09-15"
}

patty_chicken = {
    "name": "Chicken Patty",
    "best_used_days": 7,  # frozen shelf life after thaw
    "price_per_unit": 2.50,
    "unit": "piece",
    "current_stock": 200,
    "last_restock_date": "2025-09-15"
}

lettuce = {
    "name": "Fresh Lettuce",
    "best_used_days": 7,
    "price_per_unit": 0.008,
    "unit": "grams",
    "current_stock": 2000,
    "last_restock_date": "2025-09-17"
}

tomato = {
    "name": "Fresh Tomato",
    "best_used_days": 10,
    "price_per_unit": 0.012,
    "unit": "grams",
    "current_stock": 3000,
    "last_restock_date": "2025-09-16"
}

onion = {
    "name": "Yellow Onion",
    "best_used_days": 30,
    "price_per_unit": 0.005,
    "unit": "grams",
    "current_stock": 2500,
    "last_restock_date": "2025-09-12"
}

mayonaise = {
    "name": "Mayonnaise",
    "best_used_days": 60,
    "price_per_unit": 0.015,
    "unit": "ml",
    "current_stock": 1000,
    "last_restock_date": "2025-09-10"
}

fries = {
    "name": "Frozen French Fries",
    "best_used_days": 90,
    "price_per_unit": 0.004,
    "unit": "grams",
    "current_stock": 5000,
    "last_restock_date": "2025-09-05"
}

oil = {
    "name": "Cooking Oil",
    "best_used_days": 180,
    "price_per_unit": 0.01,
    "unit": "ml",
    "current_stock": 5000,
    "last_restock_date": "2025-09-01"
}

# Fish n Chips ingredients
white_fish = {
    "name": "White Fish Fillet",
    "best_used_days": 5,
    "price_per_unit": 4.50,
    "unit": "piece",
    "current_stock": 100,
    "last_restock_date": "2025-09-16"
}

flour = {
    "name": "All-Purpose Flour",
    "best_used_days": 180,
    "price_per_unit": 0.002,
    "unit": "grams",
    "current_stock": 5000,
    "last_restock_date": "2025-09-01"
}

egg = {
    "name": "Eggs",
    "best_used_days": 21,
    "price_per_unit": 0.25,
    "unit": "piece",
    "current_stock": 200,
    "last_restock_date": "2025-09-18"
}

breadcrumbs = {
    "name": "Breadcrumbs",
    "best_used_days": 90,
    "price_per_unit": 0.003,
    "unit": "grams",
    "current_stock": 2000,
    "last_restock_date": "2025-09-07"
}

tartar_sauce = {
    "name": "Tartar Sauce",
    "best_used_days": 30,
    "price_per_unit": 0.02,
    "unit": "ml",
    "current_stock": 1000,
    "last_restock_date": "2025-09-10"
}

lemon = {
    "name": "Fresh Lemon",
    "best_used_days": 14,
    "price_per_unit": 0.30,
    "unit": "piece",
    "current_stock": 50,
    "last_restock_date": "2025-09-18"
}

# Spaghetti ingredients
spaghetti_pasta = {
    "name": "Spaghetti Pasta",
    "best_used_days": 365,
    "price_per_unit": 0.003,
    "unit": "grams",
    "current_stock": 10000,
    "last_restock_date": "2025-09-01"
}

olive_oil = {
    "name": "Olive Oil",
    "best_used_days": 365,
    "price_per_unit": 0.015,
    "unit": "ml",
    "current_stock": 2000,
    "last_restock_date": "2025-09-01"
}

garlic = {
    "name": "Fresh Garlic",
    "best_used_days": 20,
    "price_per_unit": 0.01,
    "unit": "grams",
    "current_stock": 500,
    "last_restock_date": "2025-09-14"
}

minced_beef = {
    "name": "Minced Beef",
    "best_used_days": 3,
    "price_per_unit": 0.015,
    "unit": "grams",
    "current_stock": 2000,
    "last_restock_date": "2025-09-19"
}

minced_chicken = {
    "name": "Minced Chicken",
    "best_used_days": 3,
    "price_per_unit": 0.012,
    "unit": "grams",
    "current_stock": 2000,
    "last_restock_date": "2025-09-19"
}

bacon = {
    "name": "Bacon Strips",
    "best_used_days": 7,
    "price_per_unit": 0.018,
    "unit": "grams",
    "current_stock": 1000,
    "last_restock_date": "2025-09-15"
}

tomato_sauce = {
    "name": "Tomato Sauce",
    "best_used_days": 60,
    "price_per_unit": 0.008,
    "unit": "ml",
    "current_stock": 3000,
    "last_restock_date": "2025-09-12"
}

cream_sauce = {
    "name": "Cream Sauce",
    "best_used_days": 14,
    "price_per_unit": 0.012,
    "unit": "ml",
    "current_stock": 2000,
    "last_restock_date": "2025-09-14"
}

parmesan_cheese = {
    "name": "Parmesan Cheese",
    "best_used_days": 30,
    "price_per_unit": 0.025,
    "unit": "grams",
    "current_stock": 1000,
    "last_restock_date": "2025-09-12"
}

# Chicken Chop ingredients
chicken_breast = {
    "name": "Chicken Breast",
    "best_used_days": 5,
    "price_per_unit": 3.50,
    "unit": "piece",
    "current_stock": 150,
    "last_restock_date": "2025-09-18"
}

chicken_thigh = {
    "name": "Chicken Thigh",
    "best_used_days": 5,
    "price_per_unit": 2.80,
    "unit": "piece",
    "current_stock": 120,
    "last_restock_date": "2025-09-18"
}

seasoning_mix = {
    "name": "Seasoning Mix",
    "best_used_days": 365,
    "price_per_unit": 0.015,
    "unit": "grams",
    "current_stock": 500,
    "last_restock_date": "2025-09-01"
}

mushroom_sauce = {
    "name": "Mushroom Sauce",
    "best_used_days": 20,
    "price_per_unit": 0.018,
    "unit": "ml",
    "current_stock": 1500,
    "last_restock_date": "2025-09-14"
}

black_pepper_sauce = {
    "name": "Black Pepper Sauce",
    "best_used_days": 20,
    "price_per_unit": 0.016,
    "unit": "ml",
    "current_stock": 1500,
    "last_restock_date": "2025-09-14"
}

mashed_potato = {
    "name": "Mashed Potato",
    "best_used_days": 3,
    "price_per_unit": 0.006,
    "unit": "grams",
    "current_stock": 3000,
    "last_restock_date": "2025-09-19"
}

mixed_salad = {
    "name": "Mixed Salad",
    "best_used_days": 5,
    "price_per_unit": 0.008,
    "unit": "grams",
    "current_stock": 2000,
    "last_restock_date": "2025-09-18"
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
	"name": "burger_fries",
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
			"depends_on": []
		},
		{
			"station_id": station_ids["grill"],
			"task_name": "Grill patty",
			"duration": 6,
			"depends_on": []
		},
		{
			"station_id": station_ids["fryer"],
			"task_name": "Fry fries",
			"duration": 4,
			"depends_on": []
		},
		{
			"station_id": station_ids["assembly"],
			"task_name": "Plate dish",
			"duration": 2,
			"depends_on": [0, 1, 2]
		}
	],
	"total_time": 14
}

fish_and_chips = {
	"name": "fish_n_chip",
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
			"depends_on": []
		},
		{
			"station_id": station_ids["fryer"],
			"task_name": "Fry fish",
			"duration": 6,
			"depends_on": [0]
		},
		{
			"station_id": station_ids["fryer"],
			"task_name": "Fry fries",
			"duration": 4,
			"depends_on": []
		},
		{
			"station_id": station_ids["assembly"],
			"task_name": "Plate with tartar sauce and lemon",
			"duration": 1,
			"depends_on": [1, 2]
		}
	],
	"total_time": 13
}

spaghetti_bolognese = {
	"name": "spaghetti",
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
			"depends_on": []
		},
		{
			"station_id": station_ids["stove"],
			"task_name": "Boil spaghetti",
			"duration": 10,
			"depends_on": []
		},
		{
			"station_id": station_ids["stove"],
			"task_name": "Cook sauce with meat",
			"duration": 6,
			"depends_on": [0]
		},
		{
			"station_id": station_ids["assembly"],
			"task_name": "Mix pasta with sauce and plate",
			"duration": 1,
			"depends_on": [1, 2]
		}
	],
	"total_time": 20
}

chicken_chop = {
	"name": "chicken_chop",
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
			"depends_on": []
		},
		{
			"station_id": station_ids["grill"],
			"task_name": "Grill chicken",
			"duration": 8,
			"depends_on": [0]
		},
		{
			"station_id": station_ids["fryer"],
			"task_name": "Fry fries",
			"duration": 4,
			"depends_on": []
		},
		{
			"station_id": station_ids["stove"],
			"task_name": "Heat sauce",
			"duration": 2,
			"depends_on": []
		},
		{
			"station_id": station_ids["assembly"],
			"task_name": "Plate chicken with sauce and sides",
			"duration": 1,
			"depends_on": [1, 2, 3]
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

orders_coll.insert_many([order1, order2, order3, order4, order5, order6, order7])

from datetime import datetime, timedelta

restocks = [
    {
        "ingredient_id": ingredient_ids["bun"],
        "quantity_added": 200,
        "date": "2025-09-01T09:00:00Z",
        "items_left": 180,
        "expiry_date": "2025-09-06T00:00:00Z",
        "clear": False
    },
    {
        "ingredient_id": ingredient_ids["patty_chicken"],
        "quantity_added": 100,
        "date": "2025-09-02T11:30:00Z",
        "items_left": 95,
        "expiry_date": "2025-09-09T00:00:00Z",
        "clear": False
    },
    {
        "ingredient_id": ingredient_ids["lettuce"],
        "quantity_added": 500,
        "date": "2025-09-03T08:15:00Z",
        "items_left": 400,
        "expiry_date": "2025-09-10T00:00:00Z",
        "clear": False
    },
    {
        "ingredient_id": ingredient_ids["tomato"],
        "quantity_added": 800,
        "date": "2025-09-03T08:20:00Z",
        "items_left": 750,
        "expiry_date": "2025-09-13T00:00:00Z",
        "clear": False
    },
    {
        "ingredient_id": ingredient_ids["onion"],
        "quantity_added": 600,
        "date": "2025-09-04T14:10:00Z",
        "items_left": 580,
        "expiry_date": "2025-10-04T00:00:00Z",
        "clear": False
    },
    {
        "ingredient_id": ingredient_ids["mayonaise"],
        "quantity_added": 300,
        "date": "2025-09-05T10:00:00Z",
        "items_left": 300,
        "expiry_date": "2025-11-04T00:00:00Z",
        "clear": False
    },
    {
        "ingredient_id": ingredient_ids["fries"],
        "quantity_added": 2000,
        "date": "2025-09-06T07:50:00Z",
        "items_left": 1800,
        "expiry_date": "2025-12-05T00:00:00Z",
        "clear": False
    },
    {
        "ingredient_id": ingredient_ids["oil"],
        "quantity_added": 3000,
        "date": "2025-09-06T08:00:00Z",
        "items_left": 3000,
        "expiry_date": "2026-03-05T00:00:00Z",
        "clear": False
    },
    {
        "ingredient_id": ingredient_ids["white_fish"],
        "quantity_added": 40,
        "date": "2025-09-07T12:00:00Z",
        "items_left": 32,
        "expiry_date": "2025-09-12T00:00:00Z",
        "clear": False
    },
    {
        "ingredient_id": ingredient_ids["egg"],
        "quantity_added": 100,
        "date": "2025-09-07T12:15:00Z",
        "items_left": 90,
        "expiry_date": "2025-09-28T00:00:00Z",
        "clear": False
    },
    {
        "ingredient_id": ingredient_ids["breadcrumbs"],
        "quantity_added": 600,
        "date": "2025-09-08T09:00:00Z",
        "items_left": 580,
        "expiry_date": "2025-12-07T00:00:00Z",
        "clear": False
    },
    {
        "ingredient_id": ingredient_ids["lemon"],
        "quantity_added": 20,
        "date": "2025-09-09T13:20:00Z",
        "items_left": 18,
        "expiry_date": "2025-09-23T00:00:00Z",
        "clear": False
    },
    {
        "ingredient_id": ingredient_ids["spaghetti_pasta"],
        "quantity_added": 3000,
        "date": "2025-09-10T09:30:00Z",
        "items_left": 3000,
        "expiry_date": "2026-09-10T00:00:00Z",
        "clear": False
    },
    {
        "ingredient_id": ingredient_ids["olive_oil"],
        "quantity_added": 1000,
        "date": "2025-09-10T09:40:00Z",
        "items_left": 950,
        "expiry_date": "2026-09-10T00:00:00Z",
        "clear": False
    },
    {
        "ingredient_id": ingredient_ids["garlic"],
        "quantity_added": 200,
        "date": "2025-09-11T10:00:00Z",
        "items_left": 160,
        "expiry_date": "2025-09-30T00:00:00Z",
        "clear": False
    },
    {
        "ingredient_id": ingredient_ids["minced_beef"],
        "quantity_added": 1000,
        "date": "2025-09-12T16:00:00Z",
        "items_left": 800,
        "expiry_date": "2025-09-15T00:00:00Z",
        "clear": False
    },
    {
        "ingredient_id": ingredient_ids["minced_chicken"],
        "quantity_added": 800,
        "date": "2025-09-12T16:10:00Z",
        "items_left": 750,
        "expiry_date": "2025-09-15T00:00:00Z",
        "clear": False
    },
    {
        "ingredient_id": ingredient_ids["bacon"],
        "quantity_added": 400,
        "date": "2025-09-13T09:00:00Z",
        "items_left": 380,
        "expiry_date": "2025-09-20T00:00:00Z",
        "clear": False
    },
    {
        "ingredient_id": ingredient_ids["chicken_breast"],
        "quantity_added": 60,
        "date": "2025-09-14T08:00:00Z",
        "items_left": 55,
        "expiry_date": "2025-09-19T00:00:00Z",
        "clear": False
    },
    {
        "ingredient_id": ingredient_ids["mixed_salad"],
        "quantity_added": 500,
        "date": "2025-09-14T08:10:00Z",
        "items_left": 420,
        "expiry_date": "2025-09-19T00:00:00Z",
        "clear": True
    }
]

restork_coll.insert_many(restocks)

client.close()