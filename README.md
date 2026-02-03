Heuristics:
- Wooden axe optimization: when the recipe needs a lot of wood, the planner forces a wooden axe after a bench exists, then uses the axe for getting wood
- Tool preference: prioritize the better tool gathering methods when available
- Dependency filtering: skip methods that require tools currently in production or that are impossible with the current inventory
- Cycle control: cap repetitive material production to avoid deep recursion