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

		for tool in rule.get('Requires', {}):
			tasks.append(('have_enough', ID, tool, 1))

		for item, qty in rule.get('Consumes', {}).items():
			tasks.append(('have_enough', ID, item, qty))

		tasks.append((name, ID))

		return tasks
	return method

# RANK TOOL

def tool_rank(req):
    if not req:
        return 0
    if 'wooden_pickaxe' in req:
        return 1
    if 'stone_pickaxe' in req:
        return 2
    if 'iron_pickaxe' in req:
        return 3
    return 4

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
		rules.sort(key=lambda x: (
			tool_rank(x[1].get('Requires')),
			x[1]['Time']
		))


		methods = []
		for name, rule in rules:
			op_name = f"op_{name}"
			methods.append(make_method(op_name, rule))

		pyhop.declare_methods(f'produce_{product}', *methods)
		# debugging
		#pyhop.print_methods()

def make_operator(rule):
	def operator(state, ID):

		if state.time[ID] < rule['Time']:
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
	# prune search branch if heuristic() returns True
	# do not change parameters to heuristic(), but can add more heuristic functions with the same parameters: 
	# e.g. def heuristic2(...); pyhop.add_check(heuristic2)
	def heuristic(state, curr_task, tasks, plan, depth, calling_stack):
		
		# prune impossible time
		if state.time[ID] < 0:
			return True

		if depth > 150:
			return True
		
	 	# prevent recursive production loops, but allow limited recursion for multiple units
		if curr_task[0].startswith('produce_'):
			item = curr_task[0][8:]  # extract item name from 'produce_X'
			# Count occurrences of this produce task in calling stack
			count = sum(1 for t in calling_stack if t[0] == curr_task[0])
			# Items that need multiple copies: allow up to 10 recursions
			# Items that don't: allow up to 2 recursions
			if item in ['cobble', 'ore', 'coal', 'ingot']:
				if count >= 10:
					return True
			else:
				if count >= 2:
					return True
		
		return False

	pyhop.add_check(heuristic)

def define_ordering(data, ID):
	# if needed, use the function below to return a different ordering for the methods
	# note that this should always return the same methods, in a new order, and should not add/remove any new ones
	def reorder_methods(state, curr_task, tasks, plan, depth, calling_stack, methods):
		return methods
	
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
	rules_filename = 'crafting.json'
	if len(sys.argv) > 1:
		rules_filename = sys.argv[1]

	with open(rules_filename) as f:
		data = json.load(f)

	state = set_up_state(data, 'agent')
	goals = set_up_goals(data, 'agent')

	declare_operators(data)
	declare_methods(data)
	add_heuristic(data, 'agent')
	define_ordering(data, 'agent')

	# pyhop.print_operators()
	# pyhop.print_methods()

	# Hint: verbose output can take a long time even if the solution is correct; 
	# try verbose=1 if it is taking too long
	pyhop.pyhop(state, goals, verbose=1)
	# pyhop.pyhop(state, [('have_enough', 'agent', 'cart', 1),('have_enough', 'agent', 'rail', 20)], verbose=3)