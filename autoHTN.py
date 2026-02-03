import pyhop
import json

def check_enough(state, ID, item, num):
	if getattr(state,item)[ID] >= num: return []
	return False

def produce_enough(state, ID, item, num):
	return [('produce', ID, item), ('have_enough', ID, item, num)]

pyhop.declare_methods('have_enough', check_enough, produce_enough)

def produce(state, ID, item):
	return [('produce_{}'.format(item), ID)]

pyhop.declare_methods('produce', produce)

def make_method(name, rule):
	def method(state, ID):
		tasks = []

		# tools ?
		for tool in rule.get('Requires', {}):
			tasks.append(('have_enough', ID, tool, 1))

		# simple items first (wood, cobble, coal, ore) --> (plank, stick) --> (ingot, etc.)
		item_priority = {
			'wood': 1, 'cobble': 1, 'coal': 1, 'ore': 1,
			'plank': 2, 'stick': 2, 'ingot': 2
			#'ingot': 3
		}
		consumables = [(item, qty) for item, qty in rule.get('Consumes', {}).items()]
		consumables.sort(key=lambda x: item_priority.get(x[0], 4))
		
		for item, qty in consumables:
			tasks.append(('have_enough', ID, item, qty))

		tasks.append((name, ID))

		return tasks
	return method

# RANK TOOL - Lower rank = better (prefer simpler tools)

def tool_rank(req):
    if not req:
        return 0  # No tool required
    if 'bench' in req and len(req) == 1:
        return 1  # Bench only recipes are simple
    if 'wooden_axe' in req or 'wooden_pickaxe' in req:
        return 2  # Wooden tools are quick to make
    if 'stone_axe' in req or 'stone_pickaxe' in req:
        return 3  # Stone tools need cobble
    if 'furnace' in req:
        return 4  # Furnace is slow
    if 'iron_axe' in req or 'iron_pickaxe' in req:
        return 5  # Iron tools are expensive
    return 10

def declare_methods(data):
	# some recipes are faster than others for the same product even though they might require extra tools
	# sort the recipes so that faster recipes go first

	# your code here
	# hint: call make_method, then declare the method to pyhop using pyhop.declare_methods('foo', m1, m2, ..., mk)

	recipes_by_product = {}

	for name, rule in data['Recipes'].items():
		for product in rule['Produces']:
			recipes_by_product.setdefault(product, []).append((name, rule))

	for product, rules in recipes_by_product.items():
		if product == 'wood':
			rules.sort(key=lambda x: (
				0 if 'punch' in x[0] else 1,  # Punch first
				tool_rank(x[1].get('Requires')),
				x[1]['Time'],
				len(x[1].get('Consumes', {}))
			))
		else:
			rules.sort(key=lambda x: (
				tool_rank(x[1].get('Requires')),
				x[1]['Time'],
				len(x[1].get('Consumes', {}))
			))

		methods = []
		for name, rule in rules:
			op_name = f"op_{name}"
			method = make_method(op_name, rule)
			method._requires = rule.get('Requires', {})
			method._requires_tools = set(rule.get('Requires', {}).keys())
			method._consumes = set(rule.get('Consumes', {}).keys())
			method._recipe_name = name
			methods.append(method)

		pyhop.declare_methods(f'produce_{product}', *methods)
		#pyhop.print_methods()

def make_operator(rule):
	def operator(state, ID):

		if state.time[ID] < rule['Time']:
			return False

		for tool, qty in rule.get('Requires', {}).items():
			if getattr(state, tool)[ID] < qty:
				return False

		for item, qty in rule.get('Consumes', {}).items():
			if getattr(state, item)[ID] < qty:
				return False

		for item, qty in rule.get('Consumes', {}).items():
			getattr(state, item)[ID] -= qty

		for item, qty in rule.get('Produces', {}).items():
			getattr(state, item)[ID] += qty

		state.time[ID] -= rule['Time']
		return state

	operator.__doc__ = f"Produces {rule.get('Produces', {})} consuming {rule.get('Consumes', {})} requiring {rule.get('Requires', {})}"
	return operator


def declare_operators(data):
	# your code here
	# hint: call make_operator, then declare the operator to pyhop using pyhop.declare_operators(o1, o2, ..., ok)
	ops = []

	for name, rule in data['Recipes'].items():
		op = make_operator(rule)
		op.__name__ = f"op_{name}"
		ops.append(op)

	pyhop.declare_operators(*ops)

def add_heuristic(data, ID):
	goal_tools = {k for k in data.get('Problem', {}).get('Goal', {}) if k in data.get('Tools', [])}
	iron_tools = {'iron_axe', 'iron_pickaxe'}
	axe_tools = {'wooden_axe', 'stone_axe', 'iron_axe'}
	goal_items = data.get('Problem', {}).get('Goal', {})
	goal_ingot = goal_items.get('ingot', 0)

	def heuristic(state, curr_task, tasks, plan, depth, calling_stack):
		# Critical: prevent deep recursion
		if state.time[ID] < 0:
			return True
		if depth > 300:  # Increased depth limit significantly for iron_pickaxe
			return True

		# Prune tool production that isn't part of the goal (axes and iron tools)
		if curr_task[0].startswith('produce_'):
			item = curr_task[0][8:]
			if item in axe_tools and item not in goal_tools:
				return True
			if item in iron_tools and item not in goal_tools:
				return True

		# If goal doesn't require iron tools, avoid building them before ingots exist
		if curr_task[0].startswith('produce_'):
			item = curr_task[0][8:]
			if item in iron_tools and not (goal_tools & iron_tools):
				if getattr(state, 'ingot', {}).get(ID, 0) < 3:
					return True
			
		# Track repetitive production tasks in calling stack to prevent cycles
		if curr_task[0].startswith('produce_'):
			item = curr_task[0][8:]
			count_in_stack = sum(1 for t in calling_stack if t[0] == curr_task[0])
			
			# Allow more repetitions for bulk materials (e.g., furnace needs 8 cobble)
			if goal_ingot > 0:
				max_repeats = {
					'ore': goal_ingot + 1,
					'coal': goal_ingot + 1,
					'cobble': 12,  # 8 furnace + 3 stone pick + buffer
					'wood': 4,
					'plank': 12,
					'stick': 6
				}.get(item, 5)
			else:
				max_repeats = {
					'cobble': 12,
					'ore': 12,
					'coal': 12,
					'ingot': 12,
					'wood': 12,
					'plank': 12,
					'stick': 12
				}.get(item, 5)
			
			if count_in_stack >= max_repeats:
				return True
		
		return False

	pyhop.add_check(heuristic)


def define_ordering(data, ID):
	# Filter methods to reduce cyclic tool dependencies (major source of slowdown)
	tool_set = set(data.get('Tools', []))
	raw_materials = {'wood', 'cobble', 'coal', 'ore'}
	goal_tools = {k for k in data.get('Problem', {}).get('Goal', {}) if k in tool_set}
	iron_tools = {'iron_axe', 'iron_pickaxe'}
	goal_items = data.get('Problem', {}).get('Goal', {})
	goal_ingot = goal_items.get('ingot', 0)

	def reorder_methods(state, curr_task, tasks, plan, depth, calling_stack, methods):
		if not curr_task[0].startswith('produce_'):
			return methods

		# Tools currently being produced in this branch
		tools_in_production = {
			t[0][8:] for t in calling_stack
			if t[0].startswith('produce_') and t[0][8:] in tool_set
		}

		if not tools_in_production:
			return methods

		filtered = []
		for m in methods:
			req_tools = getattr(m, '_requires_tools', set())
			# Skip methods that depend on a tool we're currently trying to build
			if req_tools & tools_in_production:
				continue
			# If goal doesn't require iron tools, avoid iron tool dependencies before ingots exist
			if (req_tools & iron_tools) and not (goal_tools & iron_tools):
				if getattr(state, 'ingot', {}).get(ID, 0) < 3:
					continue
			filtered.append(m)

		candidate_methods = filtered or methods

		# For raw materials, prefer the cheapest available tool path to avoid search blowup
		item = curr_task[0][8:]
		if goal_ingot > 0:
			if item == 'wood':
				candidate_methods = [m for m in candidate_methods if 'punch for wood' in getattr(m, '_recipe_name', '')] or candidate_methods
			elif item == 'cobble':
				candidate_methods = [m for m in candidate_methods if 'wooden_pickaxe' in getattr(m, '_requires_tools', set())] or candidate_methods
			elif item in {'ore', 'coal'}:
				candidate_methods = [m for m in candidate_methods if 'stone_pickaxe' in getattr(m, '_requires_tools', set())] or candidate_methods

		if item in raw_materials:
			available = []
			for m in candidate_methods:
				req_tools = getattr(m, '_requires_tools', set())
				if all(getattr(state, t)[ID] >= 1 for t in req_tools):
					available.append(m)
			if available:
				min_rank = min(tool_rank(getattr(m, '_requires', {})) for m in available)
				available = [m for m in available if tool_rank(getattr(m, '_requires', {})) == min_rank]
				return available
			else:
				min_rank = min(tool_rank(getattr(m, '_requires', {})) for m in candidate_methods)
				candidate_methods = [m for m in candidate_methods if tool_rank(getattr(m, '_requires', {})) == min_rank]

		return candidate_methods
	
	pyhop.define_ordering(reorder_methods)

def set_up_state(data, ID):
	state = pyhop.State('state')
	setattr(state, 'time', {ID: data['Problem']['Time']})

	for item in data['Items']:
		setattr(state, item, {ID: 0})

	for item in data['Tools']:
		setattr(state, item, {ID: 0})

	for item, num in data['Problem']['Initial'].items():
		setattr(state, item, {ID: num})

	return state

def set_up_goals(data, ID):
	goals = []
	for item, num in data['Problem']['Goal'].items():
		goals.append(('have_enough', ID, item, num))
	
	# # rails first, then carts
	# goals.sort(key=lambda g: g[2] == 'cart')

	return goals

if __name__ == '__main__':
	import sys
	sys.setrecursionlimit(10000)  # Increase recursion limit for deep searches
	
	rules_filename = 'crafting.json'
	if len(sys.argv) > 1:
		rules_filename = sys.argv[1]

	print(f"Loading {rules_filename}...", flush=True)
	with open(rules_filename) as f:
		data = json.load(f)

	print("Setting up state...", flush=True)
	state = set_up_state(data, 'agent')
	goals = set_up_goals(data, 'agent')

	print("Declaring operators...", flush=True)
	declare_operators(data)
	print("Declaring methods...", flush=True)
	declare_methods(data)
	print("Adding heuristic...", flush=True)
	add_heuristic(data, 'agent')
	print("Defining ordering...", flush=True)
	define_ordering(data, 'agent')

	# pyhop.print_operators()
	# pyhop.print_methods()

	# Hint: verbose output can take a long time even if the solution is correct; 
	# try verbose=1 if it is taking too long
	print("Starting planner...", flush=True)
	initial_time = data['Problem']['Time']
	try:
		result = pyhop.pyhop(state, goals, verbose=0)
		print("\n=== PLANNING RESULT ===")
		if result:
			# Calculate time used from the plan
			time_used = 0
			for step in result:
				# Extract recipe name from operator name (e.g., 'op_punch for wood' -> 'punch for wood')
				op_name = step[0]
				if op_name.startswith('op_'):
					recipe_name = op_name[3:]  # Remove 'op_' prefix
					if recipe_name in data['Recipes']:
						time_used += data['Recipes'][recipe_name]['Time']
			
			print("SUCCESS: Found a valid plan")
			print(f"Time used: {time_used} / {initial_time} Minecraft time units")
			print(f"\nPlan ({len(result)} steps):")
			for i, step in enumerate(result, 1):
				print(f"{i}. {step}")
		else:
			print("FAILED: No plan found")
	except RecursionError:
		print("ERROR: Recursion limit exceeded - search space too large")
	except KeyboardInterrupt:
		print("\nInterrupted by user")