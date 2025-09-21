
from ortools.sat.python import cp_model
from pymongo import MongoClient
from collections import defaultdict
from bson import ObjectId
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

load_dotenv()
uri = os.getenv('MONGO_URI')

client = MongoClient(uri)
db = client["kitchlah_db"]
orders_collection = db["orders"]
items_collection = db["items"]
stations_collection = db["stations"]
schedules_collection = db["schedules"]

all_tasks = []
horizon = 0

# Fetch orders from database
orders = list(orders_collection.find())

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

def print_schedule(tasks):
    print("\n=== Schedule ===")
    print(f"{'Order':<8} {'Item':<6} {'Task':<20} {'Station':<10} {'Start':<6} {'End':<6}")
    print("-" * 70)
    for t in tasks:
        print(
            f"{str(t['order_id'])[:6]:<8} "
            f"{t['item_idx']:<6} "
            f"{t['task_name']:<20} "
            f"{str(t['station_id']):<10} "
            f"{t['start_time']:<6} "
            f"{t['end_time']:<6}"
        )
    print("=" * 70)

def create_model(model, tasks, current_time=None):

	if current_time is None:
		current_time = datetime.now()

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

if __name__ == "__main__":

	current_time = datetime.now()
	tasks, horizon, scheduling_time = orders_to_tasks(orders, current_time)
	model = cp_model.CpModel()
	model, task_vars, makespan = create_model(model, tasks, scheduling_time)
	solver = cp_model.CpSolver()
	status = solver.Solve(model)

	if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
		print("Optimal solution found!")
		print(f"Makespan: {solver.Value(makespan)} time units")


		all_tasks_chrono = []
		for i, task_var in enumerate(task_vars):
			start_time = solver.Value(task_var["start"])
			end_time = solver.Value(task_var["end"])

			all_tasks_chrono.append({
				"start_time": start_time,
				"end_time": end_time,
				"station_id": task_var["station_id"],
				"task_name": task_var["task_name"],
				"order_id": task_var["order_id"],
				"item_idx": task_var["item_idx"],
				"task_idx": task_var["task_idx"]
			})
		
		all_tasks_chrono.sort(key=lambda x: (x["start_time"], str(x["station_id"])))

		# Print the schedule
		# for i, task_var in enumerate(all_tasks_chrono):
		# 	station_name = stations_collection.find_one({ "_id" : task_var["station_id"] })["name"]
		# 	print(f"Task {i}: Order {task_var['order_id']}, Item {task_var['item_idx']}, "
		# 		f"Task {task_var['task_idx']}, Station {station_name}: "
		# 		f"Start={task_var['start_time']}, End={task_var['end_time']}")

		all_tasks_with_timestamps = convert_to_timestamps(all_tasks_chrono, scheduling_time, time_unit_minutes=1)	
		# schedules_collection.insert_many(all_tasks_with_timestamps)
		# print_schedule(all_tasks_with_timestamps)
	else:
		print("No solution found!")
		if status == cp_model.INFEASIBLE:
			print("The problem is infeasible.")
		elif status == cp_model.MODEL_INVALID:
			print("The model is invalid.")
		else:
			print(f"Solver status: {status}")
   
