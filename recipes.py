# recipes.py

# -------------------- Recipe definitions --------------------
RECIPE = {
    "burger_fries": {"beef_patty":150, "fries":200, "bun_count":1, "lettuce":20},
    "fish_n_chip": {"fish":250, "fries":200, "batter":80},
    "spaghetti": {"pasta":120, "sauce":90, "cheese":10},
    "chicken_chop": {"chicken":250, "sauce":60, "fries":150}
}

# key = name of menu item, value = dict of ingredients and per-unit quantities
MENU = list(RECIPE.keys())

# -------------------- Orders to ingredient calculation --------------------
def orders_to_ingredients(pred_orders):
    out = {}
    for menu, count in pred_orders.items():
        for ing, per_unit in RECIPE[menu].items():
            out[ing] = out.get(ing, 0) + per_unit * count
    return out
