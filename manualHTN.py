import pyhop

# iron_axe for wood
def op_iron_axe_for_wood(state, ID):
	if state.time[ID] >= 1 and state.iron_axe[ID] >= 1:
		state.wood[ID] += 1
		state.time[ID] -= 1
		return state
	return False

# punch for wood
def op_punch_for_wood(state, ID):
	if state.time[ID] >= 4:
		state.wood[ID] += 1
		state.time[ID] -= 4
		return state
	return False

# craft wooden_pickaxe at bench
def op_craft_wooden_pickaxe_at_bench(state, ID):
	if state.time[ID] >= 1 and state.bench[ID] >= 1 and state.plank[ID] >= 3 and state.stick[ID] >= 2:
		state.plank[ID] -= 3
		state.stick[ID] -= 2
		state.wooden_pickaxe[ID] += 1
		state.time[ID] -= 1
		return state
	return False

# craft stone_pickaxe at bench
def op_craft_stone_pickaxe_at_bench(state, ID):
	if state.time[ID] >= 1 and state.bench[ID] >= 1 and state.cobble[ID] >= 3 and state.stick[ID] >= 2:
		state.cobble[ID] -= 3
		state.stick[ID] -= 2
		state.stone_pickaxe[ID] += 1
		state.time[ID] -= 1
		return state
	return False

# wooden_pickaxe for coal
def op_wooden_pickaxe_for_coal(state, ID):
	if state.time[ID] >= 4 and state.wooden_pickaxe[ID] >= 1:
		state.coal[ID] += 1
		state.time[ID] -= 4
		return state
	return False

# iron_pickaxe for ore
def op_iron_pickaxe_for_ore(state, ID):
	if state.time[ID] >= 2 and state.iron_pickaxe[ID] >= 1:
		state.ore[ID] += 1
		state.time[ID] -= 2
		return state
	return False

# wooden_axe for wood
def op_wooden_axe_for_wood(state, ID):
	if state.time[ID] >= 2 and state.wooden_axe[ID] >= 1:
		state.wood[ID] += 1
		state.time[ID] -= 2
		return state
	return False

# craft plank
def op_craft_plank(state, ID):
	if state.time[ID] >= 1 and state.wood[ID] >= 1:
		state.wood[ID] -= 1
		state.plank[ID] += 4
		state.time[ID] -= 1
		return state
	return False

# craft stick
def op_craft_stick(state, ID):
	if state.time[ID] >= 1 and state.plank[ID] >= 2:
		state.plank[ID] -= 2
		state.stick[ID] += 4
		state.time[ID] -= 1
		return state
	return False

# raft rail at bench
def op_craft_rail_at_bench(state, ID):
	if state.time[ID] >= 1 and state.bench[ID] >= 1 and state.ingot[ID] >= 6 and state.stick[ID] >= 1:
		state.ingot[ID] -= 6
		state.stick[ID] -= 1
		state.rail[ID] += 16
		state.time[ID] -= 1
		return state
	return False

# craft cart at bench
def op_craft_cart_at_bench(state, ID):
	if state.time[ID] >= 1 and state.bench[ID] >= 1 and state.ingot[ID] >= 5:
		state.ingot[ID] -= 5
		state.cart[ID] += 1
		state.time[ID] -= 1
		return state
	return False

# iron_pickaxe for cobble
def op_iron_pickaxe_for_cobble(state, ID):
	if state.time[ID] >= 1 and state.iron_pickaxe[ID] >= 1:
		state.cobble[ID] += 1
		state.time[ID] -= 1
		return state
	return False

# stone_axe for wood
def op_stone_axe_for_wood(state, ID):
	if state.time[ID] >= 1 and state.stone_axe[ID] >= 1:
		state.wood[ID] += 1
		state.time[ID] -= 1
		return state
	return False

# craft iron_pickaxe at bench
def op_craft_iron_pickaxe_at_bench(state, ID):
	if state.time[ID] >= 1 and state.bench[ID] >= 1 and state.ingot[ID] >= 3 and state.stick[ID] >= 2:
		state.ingot[ID] -= 3
		state.stick[ID] -= 2
		state.iron_pickaxe[ID] += 1
		state.time[ID] -= 1
		return state
	return False

# craft furnace at bench
def op_craft_furnace_at_bench(state, ID):
	if state.time[ID] >= 1 and state.bench[ID] >= 1 and state.cobble[ID] >= 8:
		state.cobble[ID] -= 8
		state.furnace[ID] += 1
		state.time[ID] -= 1
		return state
	return False

# stone_pickaxe for ore
def op_stone_pickaxe_for_ore(state, ID):
	if state.time[ID] >= 4 and state.stone_pickaxe[ID] >= 1:
		state.ore[ID] += 1
		state.time[ID] -= 4
		return state
	return False

# craft iron_axe at bench
def op_craft_iron_axe_at_bench(state, ID):
	if state.time[ID] >= 1 and state.bench[ID] >= 1 and state.ingot[ID] >= 3 and state.stick[ID] >= 2:
		state.ingot[ID] -= 3
		state.stick[ID] -= 2
		state.iron_axe[ID] += 1
		state.time[ID] -= 1
		return state
	return False

# stone_pickaxe for coal
def op_stone_pickaxe_for_coal(state, ID):
	if state.time[ID] >= 2 and state.stone_pickaxe[ID] >= 1:
		state.coal[ID] += 1
		state.time[ID] -= 2
		return state
	return False

# craft wooden_axe at bench
def op_craft_wooden_axe_at_bench(state, ID):
	if state.time[ID] >= 1 and state.bench[ID] >= 1 and state.plank[ID] >= 3 and state.stick[ID] >= 2:
		state.plank[ID] -= 3
		state.stick[ID] -= 2
		state.wooden_axe[ID] += 1
		state.time[ID] -= 1
		return state
	return False

# stone_pickaxe for cobble
def op_stone_pickaxe_for_cobble(state, ID):
	if state.time[ID] >= 2 and state.stone_pickaxe[ID] >= 1:
		state.cobble[ID] += 1
		state.time[ID] -= 2
		return state
	return False

# wooden_pickaxe for cobble
def op_wooden_pickaxe_for_cobble(state, ID):
	if state.time[ID] >= 4 and state.wooden_pickaxe[ID] >= 1:
		state.cobble[ID] += 1
		state.time[ID] -= 4
		return state
	return False

# iron_pickaxe for coal
def op_iron_pickaxe_for_coal(state, ID):
	if state.time[ID] >= 1 and state.iron_pickaxe[ID] >= 1:
		state.coal[ID] += 1
		state.time[ID] -= 1
		return state
	return False

# craft bench
def op_craft_bench(state, ID):
	if state.time[ID] >= 1 and state.plank[ID] >= 4:
		state.plank[ID] -= 4
		state.bench[ID] += 1
		state.time[ID] -= 1
		return state
	return False

# craft stone_axe at bench
def op_craft_stone_axe_at_bench(state, ID):
	if state.time[ID] >= 1 and state.bench[ID] >= 1 and state.cobble[ID] >= 3 and state.stick[ID] >= 2:
		state.cobble[ID] -= 3
		state.stick[ID] -= 2
		state.stone_axe[ID] += 1
		state.time[ID] -= 1
		return state
	return False

# smelt ore in furnace
def op_smelt_ore_in_furnace(state, ID):
	if state.time[ID] >= 5 and state.furnace[ID] >= 1 and state.ore[ID] >= 1 and state.coal[ID] >= 1:
		state.ore[ID] -= 1
		state.coal[ID] -= 1
		state.ingot[ID] += 1
		state.time[ID] -= 5
		return state
	return False

pyhop.declare_operators(
	op_iron_axe_for_wood,
	op_punch_for_wood,
	op_craft_wooden_pickaxe_at_bench,
	op_craft_stone_pickaxe_at_bench,
	op_wooden_pickaxe_for_coal,
	op_iron_pickaxe_for_ore,
	op_wooden_axe_for_wood,
	op_craft_plank,
	op_craft_stick,
	op_craft_rail_at_bench,
	op_craft_cart_at_bench,
	op_iron_pickaxe_for_cobble,
	op_stone_axe_for_wood,
	op_craft_iron_pickaxe_at_bench,
	op_craft_furnace_at_bench,
	op_stone_pickaxe_for_ore,
	op_craft_iron_axe_at_bench,
	op_stone_pickaxe_for_coal,
	op_craft_wooden_axe_at_bench,
	op_stone_pickaxe_for_cobble,
	op_wooden_pickaxe_for_cobble,
	op_iron_pickaxe_for_coal,
	op_craft_bench,
	op_craft_stone_axe_at_bench,
	op_smelt_ore_in_furnace,
)

