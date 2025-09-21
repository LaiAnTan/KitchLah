import json
import base64
from datetime import datetime, timedelta
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from ortools.sat.python import cp_model
from collections import defaultdict
from bson import ObjectId

load_dotenv()

uri = os.getenv('MONGO_URI')
client = MongoClient(uri)
db = client["kitchlah_db"]
orders_collection = db["orders"]
items_collection = db["items"]
stations_collection = db["stations"]
schedules_collection = db["schedules"]

def orders_to_tasks(orders, current_time=None):
	if current_time is None:
		current_time = datetime.now()

	tasks = []
	horizon = 0

	for order in orders:
		for i, item in enumerate(order['items']):
			menu_item = items_collection.find_one({"_id": ObjectId(item["item_id"])})
			for j, task in enumerate(menu_item["workflow"]):
				tasks.append({
					"order_id": order["_id"],
					"item_idx": i,
					"task_idx": j,
					"station_id": task["station_id"],
					"duration": task["duration"],
					"depends_on": task["depends_on"],
					"task_name": task["task_name"]
				})
			horizon += task["duration"]
	
	return tasks, horizon, current_time

def create_model(model, locked_tasks, new_tasks, horizon, current_time=None):
	if current_time is None:
		current_time = datetime.now()

	task_vars = []

	stations_to_intervals = defaultdict(list)
	# key : station id
	# value : list of intervals for that station

	tasks = [x for x in locked_tasks]
	tasks.extend(new_tasks)

	for i, old in enumerate(locked_tasks):
		start_var = model.NewConstant(old["start_time"])
		end_var = model.NewConstant(old["end_time"])
		duration = old["end_time"] - old["start_time"]
		interval = model.NewIntervalVar(start_var, duration, end_var, f"fixed_interval_{i}")
		task_vars.append({
			"start": start_var,
			"end": end_var,
			"interval": interval,
			"station_id": old["station_id"],
			"order_id": old["order_id"],
			"item_idx": old["item_idx"],
			"task_idx": old["task_idx"],
			"task_name": old["task_name"]
		})
		stations_to_intervals[old["station_id"]].append(interval)

	for i, task in enumerate(new_tasks):
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
			"task_idx": task["task_idx"],
			"task_name": task["task_name"]
		})
		stations_to_intervals[task["station_id"]].append(interval)

	order_item_to_indices = defaultdict(list)
	# purpose : to get task id associated with any item in any order
	# key : (order_id, item_idx in order)
	# value : (task idx)

	for i, task in enumerate(task_vars):
		key = (task["order_id"], task["item_idx"])
		order_item_to_indices[key].append(i)

	# Add dependency constraints based on depends_on field
	for k, v in order_item_to_indices.items():
		# Sort by task index to maintain order
		v.sort(key=lambda i: task_vars[i]["task_idx"])
		
		# For each task in this order item, add dependency constraints
		for task_idx in v:
			current_task = tasks[task_idx]
			current_task_var = task_vars[task_idx]
			
			# old task do not have depends on, ignore
			if (current_task.get("depends_on")):
				# Add constraints for each dependency in depends_on
				for dep_task_idx in current_task["depends_on"]:
					# Find the dependency task in the same order item
					dep_global_idx = None
					for idx in v:
						if task_vars[idx]["task_idx"] == dep_task_idx:
							dep_global_idx = idx
							break
					
					if dep_global_idx is not None:
						# Dependency task must finish before current task starts
						# Assumption := new orders will never depend on old orders
						model.Add(current_task_var["start"] >= task_vars[dep_global_idx]["end"])

	# add cumulative constraint for stations
	for station, intervals in stations_to_intervals.items():
		station_doc = stations_collection.find_one({"_id": ObjectId(station)})
		capacity = station_doc["capacity"] if station_doc else 1  # default capacity if not found
		demands = [1] * len(intervals)
		model.AddCumulative(intervals, demands, capacity)

	# minimize makespan
	makespan = model.NewIntVar(0, horizon, "makespan")
	model.AddMaxEquality(makespan, [t["end"] for t in task_vars])
	model.Minimize(makespan)

	return model, task_vars, makespan

def convert_to_timestamps(task_schedule, current_time, time_unit_minutes=1):
	"""
	Convert relative time units to actual timestamps
	
	Args:
		task_schedule: List of scheduled tasks with start/end times
		current_time: Reference datetime
		time_unit_minutes: How many minutes each time unit represents
	"""
	for task in task_schedule:
		task["start_timestamp"] = current_time + timedelta(minutes=task["start_time"] * time_unit_minutes)
		task["end_timestamp"] = current_time + timedelta(minutes=task["end_time"] * time_unit_minutes)
		task["scheduled_at"] = current_time
	return task_schedule

item_ids = {
	"burger_and_fries": ObjectId("68cf78946e7d2e5ba075d171"),
	"fish_and_chips": ObjectId("68cf78946e7d2e5ba075d172"),
	"spaghetti_bolognese": ObjectId("68cf78946e7d2e5ba075d173"),
	"chicken_chop": ObjectId("68cf78946e7d2e5ba075d174")
}

def lambda_handler(event, context):
	orders = []

	for record in event['Records']:
		# Kinesis data is base64 encoded
		payload = base64.b64decode(record["kinesis"]["data"]).decode("utf-8")
		data = json.loads(payload)
		orders_collection.insert_one(data)
		orders.append(data)
	
	horizon = 0
	current_time = datetime.now()
	tasks, horizon, scheduling_time = orders_to_tasks(orders, current_time)

	# get old tasks
	old_tasks = list(schedules_collection.find())
	for old in old_tasks:
		end_time = old["end_time"]
		start_time = old["start_time"]
		horizon += end_time - start_time

	model = cp_model.CpModel()
	model, task_vars, makespan = create_model(model, old_tasks, tasks, horizon, scheduling_time)
	solver = cp_model.CpSolver()
	status = solver.Solve(model)

	# locked task are constants, not IntVar
	def safe_value(x):
		return solver.Value(x) if isinstance(x, cp_model.IntVar) else x

	if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
		
		all_tasks_chrono = []
		for i, task_var in enumerate(task_vars):
			start_time = safe_value(task_var["start"])
			end_time = safe_value(task_var["end"])

			all_tasks_chrono.append({
				"start_time": start_time,
				"end_time": end_time,
				"station_id": task_var["station_id"],
				"task_name": task_var["task_name"],
				"order_id": task_var["order_id"],
				"item_idx": task_var["item_idx"],
				"task_idx": task_var["task_idx"]
			})
		# Print the schedule
		for i, task_var in enumerate(all_tasks_chrono):
			station_name = stations_collection.find_one({ "_id" : task_var["station_id"] })["name"]
			print(f"Task {i}: Order {task_var['order_id']}, Item {task_var['item_idx']}, "
				f"Task {task_var['task_idx']}, Station {station_name}: "
				f"Start={task_var['start_time']}, End={task_var['end_time']}")
  
		all_tasks_chrono.sort(key=lambda x: x["start_time"])
		all_tasks_with_timestamps = convert_to_timestamps(all_tasks_chrono, scheduling_time, time_unit_minutes=1)	
		# very bad, remove later, temporary solution
		# ideally you would only delete the old schedules, and only add the new schedules
		# however, that takes 10 lines, this takes one
		schedules_collection.delete_many({})
		schedules_collection.insert_many(all_tasks_with_timestamps)

	else:
		print("No solution found!")
		if status == cp_model.INFEASIBLE:
			print("The problem is infeasible.")
		elif status == cp_model.MODEL_INVALID:
			print("The model is invalid.")
		else:
			print(f"Solver status: {status}")


	return {"statusCode": 200}

if __name__ == "__main__":
    lambda_handler(None, None)