
from ortools.sat.python import cp_model
from pymongo import MongoClient
from collections import defaultdict
from bson import ObjectId
from dotenv import load_dotenv
import os

load_dotenv()
uri = os.getenv('MONGO_URI')

client = MongoClient(uri)
db = client["kitchlah"]
orders_collection = db["orders"]
menu_collection = db["menu"]
stations_collection = db["stations"]

all_tasks = []
horizon = 0

# Fetch orders from database
orders = list(orders_collection.find())
tasks = []

for order in orders:
	for i, item in enumerate(order['items']):
		menu_item = menu_collection.find_one({"_id": ObjectId(item["item_id"])})
		for j, task in enumerate(menu_item["workflow"]):
			tasks.append({
				"order_id": order["_id"],
				"item_idx": i,
				"task_idx": j,
				"station_id": task["station_id"],
				"duration": task["duration"]
			})
			horizon += task["duration"]

model = cp_model.CpModel()
task_vars = []


stations_to_intervals = defaultdict(list)
# key : station id
# value : list of intervals for that station

for i, task in enumerate(tasks):
	start_var = model.NewIntVar(0, horizon, f"start_{i}")
	end_var = model.NewIntVar(0, horizon, f"end_{i}")
	interval = model.NewIntervalVar(start_var, task["duration"], end_var, f"interval_{i}")
	task_vars.append({
		"start": start_var,
		"end": end_var,
		"interval": interval,
		"station_id": task["station_id"],
		"order_id": task["order_id"],
		"item_idx": task["item_idx"],
		"task_idx": task["task_idx"]
	})
	stations_to_intervals[task["station_id"]].append(interval)

# enforce precendence inside same item

order_item_to_indices = defaultdict(list)
# purpose : to get task id associated with any item in any order
# key : (order_id, item_idx in order)
# value : (task idx)


for i, task in enumerate(task_vars):
	key = (task["order_id"], task["item_idx"])
	order_item_to_indices[key].append(i)

for k, v in order_item_to_indices.items():
	v.sort(key=lambda i: task_vars[i]["task_idx"])
	for i in range(len(v) - 1):
		model.Add(task_vars[v[i + 1]]["start"] >= task_vars[v[i]]["end"])

# add cumulative constraint for stations

for station, intervals in stations_to_intervals.items():
	station_doc = stations_collection.find_one({"station_id": station})
	capacity = station_doc["capacity"] if station_doc else 1  # default capacity if not found
	demands = [1] * len(intervals)
	model.AddCumulative(intervals, demands, capacity)

# minimize makespan

makespan = model.NewIntVar(0, horizon, "makespan")
model.AddMaxEquality(makespan, [t["end"] for t in task_vars])
model.Minimize(makespan)

solver = cp_model.CpSolver()
status = solver.Solve(model)

if status == cp_model.OPTIMAL:
	print("Optimal solution found!")
	print(f"Makespan: {solver.Value(makespan)} time units")
	
	# Print the schedule
	for i, task_var in enumerate(task_vars):
		start_time = solver.Value(task_var["start"])
		end_time = solver.Value(task_var["end"])
		print(f"Task {i}: Order {task_var['order_id']}, Item {task_var['item_idx']}, "
		      f"Task {task_var['task_idx']}, Station {task_var['station_id']}: "
		      f"Start={start_time}, End={end_time}")
		      
elif status == cp_model.FEASIBLE:
	print("Feasible solution found!")
	print(f"Makespan: {solver.Value(makespan)} time units")
	
else:
	print("No solution found!")
	if status == cp_model.INFEASIBLE:
		print("The problem is infeasible.")
	elif status == cp_model.MODEL_INVALID:
		print("The model is invalid.")
	else:
		print(f"Solver status: {status}")