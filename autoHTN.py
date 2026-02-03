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

def make_method(name, rule, product=None):
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

	# Check if we should optimize for wooden_axe
	goal_items = data.get('Problem', {}).get('Goal', {})
	wood_needed = goal_items.get('wood', 0) + goal_items.get('plank', 0) / 4 + goal_items.get('stick', 0) / 4
	if 'iron_pickaxe' in goal_items or 'stone_pickaxe' in goal_items:
		wood_needed += 4
	
	use_wooden_axe_optimization = wood_needed >= 4

	for product, rules in recipes_by_product.items():
		if product == 'wood':
			# For wood gathering, prioritize wooden_axe over punch when it's beneficial
			# Strategy: Put wooden_axe FIRST, punch SECOND
			# The heuristic will prune wooden_axe if not beneficial
			def wood_priority(x):
				name = x[0]
				if 'wooden_axe' in name:
					return 0  # Try wooden_axe FIRST
				elif 'punch' in name:
					return 1  # Punch as fallback
				elif 'stone_axe' in name:
					return 2
				elif 'iron_axe' in name:
					return 3
				else:
					return 4
			
			rules.sort(key=lambda x: (
				wood_priority(x),
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
			method = make_method(op_name, rule, product=product)
			method._requires = rule.get('Requires', {})
			method._requires_tools = set(rule.get('Requires', {}).keys())
			method._consumes = set(rule.get('Consumes', {}).keys())
			method._recipe_name = name
			method._product = product
			method._is_punch = 'punch' in name
			methods.append(method)

		# Force wooden_axe usage once it's craftable (only for wood and only when optimization applies)
		if product == 'wood' and use_wooden_axe_optimization:
			def force_wooden_axe(state, ID):
				if getattr(state, 'bench', {}).get(ID, 0) < 1:
					return False
				if getattr(state, 'wooden_axe', {}).get(ID, 0) >= 1:
					return False
				return [
					('have_enough', ID, 'plank', 3),
					('have_enough', ID, 'stick', 2),
					('have_enough', ID, 'wooden_axe', 1),
					('op_wooden_axe for wood', ID)
				]
			force_wooden_axe._recipe_name = 'force_wooden_axe'
			force_wooden_axe._requires = {'bench': 1}
			force_wooden_axe._requires_tools = {'bench'}
			force_wooden_axe._consumes = set()
			force_wooden_axe._product = 'wood'
			force_wooden_axe._is_punch = False
			force_wooden_axe._is_force_wooden_axe = True
			methods.insert(0, force_wooden_axe)

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
	goal_iron_pickaxe = goal_items.get('iron_pickaxe', 0)
	initial_time = data['Problem']['Time']
	# scale depth limit based on time budget
	max_depth = 200 if initial_time <= 100 else 280

	def heuristic(state, curr_task, tasks, plan, depth, calling_stack):
		# prevent deep recursion
		if state.time[ID] < 0:
			return True
		
		if depth > max_depth:
			return True

		# PRUNE PUNCH FOR WOOD
		if curr_task[0] == 'produce_wood':
			wood_count = getattr(state, 'wood', {}).get(ID, 0)
			plank_count = getattr(state, 'plank', {}).get(ID, 0)
			stick_count = getattr(state, 'stick', {}).get(ID, 0)
			has_bench = getattr(state, 'bench', {}).get(ID, 0) >= 1
			has_wooden_axe = getattr(state, 'wooden_axe', {}).get(ID, 0) >= 1
			
			# TOTAL WOOD NEED CALCULATION
			wood_needed_for_goals = goal_items.get('wood', 0)
			plank_needed = goal_items.get('plank', 0)
			stick_needed = goal_items.get('stick', 0)
			tool_wood_needed = 2 if ('iron_pickaxe' in goal_items or 'stone_pickaxe' in goal_items) else 0
			
			total_wood_needed = wood_needed_for_goals + (plank_needed / 4) + (stick_needed / 4) + tool_wood_needed
			wood_equivalent_current = wood_count + (plank_count / 4) + (stick_count / 4)
			remaining_wood = max(0, total_wood_needed - wood_equivalent_current)
			
			# PRUNCE PUNCH 
			if has_bench and not has_wooden_axe and remaining_wood >= 3:
				if len(calling_stack) > 0:
					pass

		# allow iron tool production when in goal
		if curr_task[0].startswith('produce_'):
			item = curr_task[0][8:]
			# check wood needs for axe production decisions
			goal_wood = goal_items.get('wood', 0)
			goal_plank = goal_items.get('plank', 0)
			goal_stick = goal_items.get('stick', 0)
			
			intermediate_wood_estimate = 0
			
			# bench needs 4 planks
			if not getattr(state, 'bench', {}).get(ID, 0):
				intermediate_wood_estimate += 1
			
			# wooden pickaxe needs 3 planks + 2 sticks
			# stone pickaxe needs 2 sticks
			# iron pickaxe needs 2 sticks
			if 'iron_pickaxe' in goal_items:
				intermediate_wood_estimate += 3  # wooden pickaxe + stone pickaxe + iron pickaxe
			elif 'stone_pickaxe' in goal_items:
				intermediate_wood_estimate += 2  # wooden pickaxe + stone pickaxe
			elif 'wooden_pickaxe' in goal_items:
				intermediate_wood_estimate += 1.5
			
			# furnace needs sticks for coal/ore smelting
			if goal_items.get('ingot', 0) > 0 or goal_iron_pickaxe > 0:
				intermediate_wood_estimate += 1
			
			total_wood_need = goal_wood + (goal_plank / 4) + (goal_stick / 4) + intermediate_wood_estimate
			

			if item == 'wooden_axe':
				return False
			
			# prune other axes unless in goal
			if item in axe_tools and item != 'wooden_axe' and item not in goal_tools:
				return True
			
			# allow iron tools only if explicitly in goal
			if item in iron_tools and item not in goal_tools:
				return True
			# allow furnace only if ingots or iron pickaxe in goal
			if item == 'furnace' and item not in goal_tools:
				if goal_ingot == 0 and goal_iron_pickaxe == 0:
					return True

		# if goal doesn't require iron tools, avoid building them before ingots exist
		if curr_task[0].startswith('produce_'):
			item = curr_task[0][8:]
			if item in iron_tools and not (goal_tools & iron_tools):
				if getattr(state, 'ingot', {}).get(ID, 0) < 3:
					return True
			
		# track repetitive production tasks in calling stack to prevent cycles
		if curr_task[0].startswith('produce_'):
			item = curr_task[0][8:]
			count_in_stack = sum(1 for t in calling_stack if t[0] == curr_task[0])
			
			# allow more repetitions for bulk materials (e.g., furnace needs 8 cobble)
			# scale based on what's in the goal: sticks/planks/wood need more wood production
			goal_stick = goal_items.get('stick', 0)
			goal_plank = goal_items.get('plank', 0)
			goal_wood = goal_items.get('wood', 0)
			extra_wood_for_sticks = 2 if goal_stick > 0 else 0
			extra_wood_for_planks = 2 if goal_plank > 0 else 0
			
			if goal_ingot > 0 or goal_stick > 0 or goal_plank > 0 or goal_iron_pickaxe > 0:
				goal_cart = goal_items.get('cart', 0)
				goal_rail = goal_items.get('rail', 0)
				
				if initial_time <= 100:
					max_repeats = {
						'ore': 6,
						'coal': 6,
						'cobble': 12,
						'wood': 8,
						'plank': 12,
						'stick': 8
					}.get(item, 5)
				elif goal_cart > 0 or goal_rail > 0:
					if goal_rail > 0:
						ore_cap = 25
					else:
						ore_cap = 5
					
					max_repeats = {
						'ore': ore_cap,
						'coal': ore_cap,
						'cobble': 8,
						'wood': 4,
						'plank': 10,
						'stick': 4,
						'ingot': 5
					}.get(item, 3)
				else:
					# normal caps for other goals
					max_repeats = {
						'ore': max(goal_ingot, 3) + 2,
						'coal': max(goal_ingot, 3) + 2,
						'cobble': 15,
						'wood': 10 + extra_wood_for_sticks,
						'plank': 15,
						'stick': 10 if (goal_stick > 0 or goal_iron_pickaxe > 0) else 4
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
	# filter methods to reduce cyclic tool dependencies
	tool_set = set(data.get('Tools', []))
	raw_materials = {'wood', 'cobble', 'coal', 'ore'}
	goal_items = set(data['Problem']['Goal'].keys())
	goal_quantities = data['Problem']['Goal']
	goal_tools = {k for k in goal_items if k in tool_set}
	iron_tools = {'iron_axe', 'iron_pickaxe'}
	goal_ingot = goal_quantities.get('ingot', 0)
	
	# calculate wood requirements based on goals
	# wood is needed directly or indirectly through planks (4 planks per wood) and sticks (8 sticks per wood)
	wood_needed_for_goals = 0
	if "wood" in goal_quantities:
		wood_needed_for_goals += goal_quantities["wood"]
	if "plank" in goal_quantities:
		wood_needed_for_goals += goal_quantities["plank"] / 4
	if "stick" in goal_quantities:
		wood_needed_for_goals += goal_quantities["stick"] / 8
	
	# pre-calculate total wood needed for this problem
	total_wood_needed_for_problem = wood_needed_for_goals
	if 'iron_pickaxe' in goal_items:
		total_wood_needed_for_problem += 2.25
	elif 'stone_pickaxe' in goal_items:
		total_wood_needed_for_problem += 1.25
	elif 'wooden_pickaxe' in goal_items:
		total_wood_needed_for_problem += 1.25
	total_wood_needed_for_problem += 1  # bench materials


	def reorder_methods(state, curr_task, tasks, plan, depth, calling_stack, methods):
		if not curr_task[0].startswith('produce_'):
			return methods

		item = curr_task[0][8:]
		if item == 'wood':
			has_bench = getattr(state, 'bench', {}).get(ID, 0) >= 1
			has_wooden_axe = getattr(state, 'wooden_axe', {}).get(ID, 0) >= 1
			in_wooden_axe_production = any(t[0] == 'produce_wooden_axe' for t in calling_stack)
			if has_bench and not has_wooden_axe and total_wood_needed_for_problem >= 3 and not in_wooden_axe_production:
				force_methods = [m for m in methods if getattr(m, '_is_force_wooden_axe', False)]
				if force_methods:
					return force_methods
		
		# tools currently being produced in this branch
		tools_in_production = {
			t[0][8:] for t in calling_stack
			if t[0].startswith('produce_') and t[0][8:] in tool_set
		}

		filtered = []
		for m in methods:
			req_tools = getattr(m, '_requires_tools', set())
			# skip methods that depend on a tool we're currently trying to build
			if req_tools & tools_in_production:
				continue
			# if goal doesn't require iron tools --> avoid iron tool dependencies before ingots exist
			if (req_tools & iron_tools) and not (goal_tools & iron_tools):
				if getattr(state, 'ingot', {}).get(ID, 0) < 3:
					continue
			filtered.append(m)

		candidate_methods = filtered or methods

		# for items with specific goal -->  strongly filter to simplest methods
		goal_items = data.get('Problem', {}).get('Goal', {})
		goal_stick = goal_items.get('stick', 0)
		goal_ingot = goal_items.get('ingot', 0)
		goal_iron_pickaxe = goal_items.get('iron_pickaxe', 0)
		goal_cart = goal_items.get('cart', 0)
		
		if goal_stick > 0 or goal_ingot > 0 or goal_iron_pickaxe > 0 or goal_cart > 0:
			if item in raw_materials:
				# keep top 2 methods by tool rank
				ranked = sorted(candidate_methods, key=lambda m: tool_rank(getattr(m, '_requires', {})))
				if ranked:
					min_rank = tool_rank(getattr(ranked[0], '_requires', {}))
					second_rank = min_rank + 1
					candidate_methods = [m for m in ranked if tool_rank(getattr(m, '_requires', {})) <= second_rank][:2]

		if item in raw_materials:
			available = []
			unavailable = []
			for m in candidate_methods:
				req_tools = getattr(m, '_requires_tools', set())
				if all(getattr(state, t)[ID] >= 1 for t in req_tools):
					available.append(m)
				else:
					unavailable.append(m)
			
			# special handling for wood production -> prefer wooden_axe optimization
			if item == 'wood':
				has_bench = getattr(state, 'bench', {}).get(ID, 0) >= 1
				has_wooden_axe = getattr(state, 'wooden_axe', {}).get(ID, 0) >= 1
				in_wooden_axe_production = any(t[0] == 'produce_wooden_axe' for t in calling_stack)
				
				# if we have wooden_axe -> use it exclusively
				if has_wooden_axe:
					axe_available = [m for m in available if 'wooden_axe' in getattr(m, '_requires_tools', set())]
					if axe_available:
						return axe_available  # use wooden_axe exclusively

				# if need lots of wood -> force the wooden_axe plan
				if has_bench and not has_wooden_axe and total_wood_needed_for_problem >= 3 and not in_wooden_axe_production:
					force_methods = [m for m in candidate_methods if getattr(m, '_is_force_wooden_axe', False)]
					if force_methods:
						return force_methods

				# if bench exists and we need lots of wood --> force the wooden_axe path
				in_wooden_axe_production = any(t[0] == 'produce_wooden_axe' for t in calling_stack)
				if has_bench and not has_wooden_axe and total_wood_needed_for_problem >= 3 and not in_wooden_axe_production:
					wooden_axe_methods = [m for m in candidate_methods if 'wooden_axe' in getattr(m, '_requires_tools', set())]
					if wooden_axe_methods:
						return wooden_axe_methods
			
			if available:
				# prefer methods with better tools first
				available.sort(key=lambda m: tool_rank(getattr(m, '_requires', {})), reverse=True)
				return available
			else:
				return candidate_methods

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
	goal_items = data['Problem']['Goal']
	
	for item, num in goal_items.items():
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

	# DEBUGGING OUTPUT
	print("Starting planner...", flush=True)
	initial_time = data['Problem']['Time']
	try:
		result = pyhop.pyhop(state, goals, verbose=0)
		print("\n=== PLANNING RESULT ===")
		if result is not False:
			time_used = 0
			for step in result:
				op_name = step[0]
				if op_name.startswith('op_'):
					recipe_name = op_name[3:]
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