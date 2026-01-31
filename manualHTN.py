import pyhop

# ---------------------------
# GATHER WOOD
# ---------------------------

# Iron axe
def op_iron_axe_for_wood(state, ID):
    if state.time[ID] >= 1 and state.iron_axe[ID] >= 1:
        state.wood[ID] += 1
        state.time[ID] -= 1
        return state
    return False

def iron_axe_for_wood_method(state, ID):
    return [('have_enough', ID, 'iron_axe', 1), ('op_iron_axe_for_wood', ID)]

# Punch
def op_punch_for_wood(state, ID):
    if state.time[ID] >= 4:
        state.wood[ID] += 1
        state.time[ID] -= 4
        return state
    return False

def punch_for_wood_method(state, ID):
    return [('op_punch_for_wood', ID)]

# Wooden axe
def op_wooden_axe_for_wood(state, ID):
    if state.time[ID] >= 2 and state.wooden_axe[ID] >= 1:
        state.wood[ID] += 1
        state.time[ID] -= 2
        return state
    return False

def wooden_axe_for_wood_method(state, ID):
    return [('have_enough', ID, 'wooden_axe', 1), ('op_wooden_axe_for_wood', ID)]

# Stone axe
def op_stone_axe_for_wood(state, ID):
    if state.time[ID] >= 1 and state.stone_axe[ID] >= 1:
        state.wood[ID] += 1
        state.time[ID] -= 1
        return state
    return False

def stone_axe_for_wood_method(state, ID):
    return [('have_enough', ID, 'stone_axe', 1), ('op_stone_axe_for_wood', ID)]

# ---------------------------
# CRAFT TOOLS
# ---------------------------

# Wooden pickaxe
def op_craft_wooden_pickaxe_at_bench(state, ID):
    if state.time[ID] >= 1 and state.bench[ID] >= 1 and state.plank[ID] >= 3 and state.stick[ID] >= 2:
        state.plank[ID] -= 3
        state.stick[ID] -= 2
        state.wooden_pickaxe[ID] += 1
        state.time[ID] -= 1
        return state
    return False

def craft_wooden_pickaxe_method(state, ID):
    return [('have_enough', ID, 'bench', 1), ('op_craft_wooden_pickaxe_at_bench', ID)]

# Stone pickaxe
def op_craft_stone_pickaxe_at_bench(state, ID):
    if state.time[ID] >= 1 and state.bench[ID] >= 1 and state.cobble[ID] >= 3 and state.stick[ID] >= 2:
        state.cobble[ID] -= 3
        state.stick[ID] -= 2
        state.stone_pickaxe[ID] += 1
        state.time[ID] -= 1
        return state
    return False

def craft_stone_pickaxe_method(state, ID):
    return [('have_enough', ID, 'bench', 1), ('op_craft_stone_pickaxe_at_bench', ID)]

# Iron pickaxe
def op_craft_iron_pickaxe_at_bench(state, ID):
    if state.time[ID] >= 1 and state.bench[ID] >= 1 and state.ingot[ID] >= 3 and state.stick[ID] >= 2:
        state.ingot[ID] -= 3
        state.stick[ID] -= 2
        state.iron_pickaxe[ID] += 1
        state.time[ID] -= 1
        return state
    return False

def craft_iron_pickaxe_method(state, ID):
    return [('have_enough', ID, 'bench', 1), ('op_craft_iron_pickaxe_at_bench', ID)]

# Wooden axe
def op_craft_wooden_axe_at_bench(state, ID):
    if state.time[ID] >= 1 and state.bench[ID] >= 1 and state.plank[ID] >= 3 and state.stick[ID] >= 2:
        state.plank[ID] -= 3
        state.stick[ID] -= 2
        state.wooden_axe[ID] += 1
        state.time[ID] -= 1
        return state
    return False

def craft_wooden_axe_method(state, ID):
    return [('have_enough', ID, 'bench', 1), ('op_craft_wooden_axe_at_bench', ID)]

# Stone axe
def op_craft_stone_axe_at_bench(state, ID):
    if state.time[ID] >= 1 and state.bench[ID] >= 1 and state.cobble[ID] >= 3 and state.stick[ID] >= 2:
        state.cobble[ID] -= 3
        state.stick[ID] -= 2
        state.stone_axe[ID] += 1
        state.time[ID] -= 1
        return state
    return False

def craft_stone_axe_method(state, ID):
    return [('have_enough', ID, 'bench', 1), ('op_craft_stone_axe_at_bench', ID)]

# Iron axe
def op_craft_iron_axe_at_bench(state, ID):
    if state.time[ID] >= 1 and state.bench[ID] >= 1 and state.ingot[ID] >= 3 and state.stick[ID] >= 2:
        state.ingot[ID] -= 3
        state.stick[ID] -= 2
        state.iron_axe[ID] += 1
        state.time[ID] -= 1
        return state
    return False

def craft_iron_axe_method(state, ID):
    return [('have_enough', ID, 'bench', 1), ('op_craft_iron_axe_at_bench', ID)]

# ---------------------------
# CRAFT MATERIALS
# ---------------------------

# Plank
def op_craft_plank(state, ID):
    if state.time[ID] >= 1 and state.wood[ID] >= 1:
        state.wood[ID] -= 1
        state.plank[ID] += 4
        state.time[ID] -= 1
        return state
    return False

def craft_plank_method(state, ID):
    return [('have_enough', ID, 'wood', 1), ('op_craft_plank', ID)]

# Stick
def op_craft_stick(state, ID):
    if state.time[ID] >= 1 and state.plank[ID] >= 2:
        state.plank[ID] -= 2
        state.stick[ID] += 4
        state.time[ID] -= 1
        return state
    return False

def craft_stick_method(state, ID):
    return [('have_enough', ID, 'plank', 2), ('op_craft_stick', ID)]

# Bench
def op_craft_bench(state, ID):
    if state.time[ID] >= 1 and state.plank[ID] >= 4:
        state.plank[ID] -= 4
        state.bench[ID] += 1
        state.time[ID] -= 1
        return state
    return False

def craft_bench_method(state, ID):
    return [('have_enough', ID, 'plank', 4), ('op_craft_bench', ID)]

# Furnace
def op_craft_furnace_at_bench(state, ID):
    if state.time[ID] >= 1 and state.bench[ID] >= 1 and state.cobble[ID] >= 8:
        state.cobble[ID] -= 8
        state.furnace[ID] += 1
        state.time[ID] -= 1
        return state
    return False

def craft_furnace_method(state, ID):
    return [('have_enough', ID, 'bench', 1), ('have_enough', ID, 'cobble', 8), ('op_craft_furnace_at_bench', ID)]

# Cart
def op_craft_cart_at_bench(state, ID):
    if state.time[ID] >= 1 and state.bench[ID] >= 1 and state.ingot[ID] >= 5:
        state.ingot[ID] -= 5
        state.cart[ID] += 1
        state.time[ID] -= 1
        return state
    return False

def craft_cart_method(state, ID):
    return [('have_enough', ID, 'bench', 1), ('have_enough', ID, 'ingot', 5), ('op_craft_cart_at_bench', ID)]

# Rail
def op_craft_rail_at_bench(state, ID):
    if state.time[ID] >= 1 and state.bench[ID] >= 1 and state.ingot[ID] >= 6 and state.stick[ID] >= 1:
        state.ingot[ID] -= 6
        state.stick[ID] -= 1
        state.rail[ID] += 16
        state.time[ID] -= 1
        return state
    return False

def craft_rail_method(state, ID):
    return [('have_enough', ID, 'bench', 1), ('have_enough', ID, 'ingot', 6), ('have_enough', ID, 'stick', 1), ('op_craft_rail_at_bench', ID)]

# ---------------------------
# MINING
# ---------------------------

# Wooden pickaxe
def op_wooden_pickaxe_for_cobble(state, ID):
    if state.time[ID] >= 4 and state.wooden_pickaxe[ID] >= 1:
        state.cobble[ID] += 1
        state.time[ID] -= 4
        return state
    return False

def wooden_pickaxe_for_cobble_method(state, ID):
    return [('have_enough', ID, 'wooden_pickaxe', 1), ('op_wooden_pickaxe_for_cobble', ID)]

def op_wooden_pickaxe_for_coal(state, ID):
    if state.time[ID] >= 4 and state.wooden_pickaxe[ID] >= 1:
        state.coal[ID] += 1
        state.time[ID] -= 4
        return state
    return False

def wooden_pickaxe_for_coal_method(state, ID):
    return [('have_enough', ID, 'wooden_pickaxe', 1), ('op_wooden_pickaxe_for_coal', ID)]

# Iron pickaxe
def op_iron_pickaxe_for_cobble(state, ID):
    if state.time[ID] >= 1 and state.iron_pickaxe[ID] >= 1:
        state.cobble[ID] += 1
        state.time[ID] -= 1
        return state
    return False

def iron_pickaxe_for_cobble_method(state, ID):
    return [('have_enough', ID, 'iron_pickaxe', 1), ('op_iron_pickaxe_for_cobble', ID)]

def op_iron_pickaxe_for_ore(state, ID):
    if state.time[ID] >= 2 and state.iron_pickaxe[ID] >= 1:
        state.ore[ID] += 1
        state.time[ID] -= 2
        return state
    return False

def iron_pickaxe_for_ore_method(state, ID):
    return [('have_enough', ID, 'iron_pickaxe', 1), ('op_iron_pickaxe_for_ore', ID)]

def op_iron_pickaxe_for_coal(state, ID):
    if state.time[ID] >= 1 and state.iron_pickaxe[ID] >= 1:
        state.coal[ID] += 1
        state.time[ID] -= 1
        return state
    return False

def iron_pickaxe_for_coal_method(state, ID):
    return [('have_enough', ID, 'iron_pickaxe', 1), ('op_iron_pickaxe_for_coal', ID)]

# ---------------------------
# STONE PICKAXE MINING
# ---------------------------

def op_stone_pickaxe_for_cobble(state, ID):
    if state.time[ID] >= 2 and state.stone_pickaxe[ID] >= 1:
        state.cobble[ID] += 1
        state.time[ID] -= 2
        return state
    return False

def stone_pickaxe_for_cobble_method(state, ID):
    return [('have_enough', ID, 'stone_pickaxe', 1), ('op_stone_pickaxe_for_cobble', ID)]

def op_stone_pickaxe_for_ore(state, ID):
    if state.time[ID] >= 4 and state.stone_pickaxe[ID] >= 1:
        state.ore[ID] += 1
        state.time[ID] -= 4
        return state
    return False

def stone_pickaxe_for_ore_method(state, ID):
    return [('have_enough', ID, 'stone_pickaxe', 1), ('op_stone_pickaxe_for_ore', ID)]

def op_stone_pickaxe_for_coal(state, ID):
    if state.time[ID] >= 2 and state.stone_pickaxe[ID] >= 1:
        state.coal[ID] += 1
        state.time[ID] -= 2
        return state
    return False

def stone_pickaxe_for_coal_method(state, ID):
    return [('have_enough', ID, 'stone_pickaxe', 1), ('op_stone_pickaxe_for_coal', ID)]

# ---------------------------
# SMELTING
# ---------------------------

def op_smelt_ore_in_furnace(state, ID):
    if state.time[ID] >= 5 and state.furnace[ID] >= 1 and state.ore[ID] >= 1 and state.coal[ID] >= 1:
        state.ore[ID] -= 1
        state.coal[ID] -= 1
        state.ingot[ID] += 1
        state.time[ID] -= 5
        return state
    return False

def smelt_ore_method(state, ID):
    return [('have_enough', ID, 'furnace', 1), ('have_enough', ID, 'ore', 1), ('have_enough', ID, 'coal', 1), ('op_smelt_ore_in_furnace', ID)]

# ---------------------------
# DECLARE OPERATORS
# ---------------------------

pyhop.declare_operators(
    op_iron_axe_for_wood, op_punch_for_wood, op_wooden_axe_for_wood, op_stone_axe_for_wood,
    op_craft_wooden_pickaxe_at_bench, op_craft_stone_pickaxe_at_bench, op_craft_iron_pickaxe_at_bench,
    op_craft_wooden_axe_at_bench, op_craft_stone_axe_at_bench, op_craft_iron_axe_at_bench,
    op_craft_plank, op_craft_stick, op_craft_bench, op_craft_furnace_at_bench, op_craft_cart_at_bench, op_craft_rail_at_bench,
    op_wooden_pickaxe_for_cobble, op_wooden_pickaxe_for_coal,
    op_iron_pickaxe_for_cobble, op_iron_pickaxe_for_ore, op_iron_pickaxe_for_coal,
    op_stone_pickaxe_for_cobble, op_stone_pickaxe_for_ore, op_stone_pickaxe_for_coal,
    op_smelt_ore_in_furnace
)

# ---------------------------
# DECLARE METHODS
# ---------------------------

pyhop.declare_methods('gather_wood', iron_axe_for_wood_method, punch_for_wood_method, wooden_axe_for_wood_method, stone_axe_for_wood_method)
pyhop.declare_methods('craft_wooden_pickaxe', craft_wooden_pickaxe_method)
pyhop.declare_methods('craft_stone_pickaxe', craft_stone_pickaxe_method)
pyhop.declare_methods('craft_iron_pickaxe', craft_iron_pickaxe_method)
pyhop.declare_methods('craft_wooden_axe', craft_wooden_axe_method)
pyhop.declare_methods('craft_stone_axe', craft_stone_axe_method)
pyhop.declare_methods('craft_iron_axe', craft_iron_axe_method)
pyhop.declare_methods('craft_plank', craft_plank_method)
pyhop.declare_methods('craft_stick', craft_stick_method)
pyhop.declare_methods('craft_bench', craft_bench_method)
pyhop.declare_methods('craft_furnace', craft_furnace_method)
pyhop.declare_methods('craft_cart', craft_cart_method)
pyhop.declare_methods('craft_rail', craft_rail_method)
pyhop.declare_methods('mine_cobble', wooden_pickaxe_for_cobble_method, iron_pickaxe_for_cobble_method, stone_pickaxe_for_cobble_method)
pyhop.declare_methods('mine_coal', wooden_pickaxe_for_coal_method, iron_pickaxe_for_coal_method, stone_pickaxe_for_coal_method)
pyhop.declare_methods('mine_ore', iron_pickaxe_for_ore_method, stone_pickaxe_for_ore_method)
pyhop.declare_methods('smelt_ore', smelt_ore_method)