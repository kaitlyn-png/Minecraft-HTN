import pyhop
import json

print("Loading JSON...")
with open('crafting.json') as f:
	data = json.load(f)

print(f"Loaded {len(data['Recipes'])} recipes")
print(f"Recipes: {list(data['Recipes'].keys())[:5]}...")

print("\nCreating state...")
state = pyhop.State('test')
state.time = {'agent': 100}
state.wood = {'agent': 0}
state.cobble = {'agent': 0}

print("Declaring method...")

def check_wood(state, ID):
	if state.wood[ID] > 0:
		return []
	return False

def produce_wood(state, ID):
	return [('punch_wood', ID)]

pyhop.declare_methods('get_wood', check_wood, produce_wood)

print("Declaring operator...")

def punch_wood(state, ID):
	state.wood[ID] += 1
	state.time[ID] -= 1
	return state

pyhop.declare_operators(punch_wood)

print("Testing pyhop...")
result = pyhop.pyhop(state, [('get_wood', 'agent')], verbose=0)

print(f"Result: {result}")
print(f"Final wood: {state.wood}")
