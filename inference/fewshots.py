CRAFTER_SAMPLE = """
Task: Place Table.
Thought 1: I need to collect wood first to place table, then I need to collect wood to make wood pickaxe, finally I need to collect coal using the wood pickaxe.
Action 1: Act[Move South, 4, 3]
Observation 1: There is water 7 steps to your south-east, grass 1 steps to your west, tree 2 steps to your south. You face grass at your front. You have nothing in your inventory.
Thought 2: I need to go to the front of the tree to get the wood.
Action 2: Act[Move South, 4, 1]
Observation 2: There is grass 1 steps to your west, tree 1 steps to your south. You face tree at your front. You have nothing in your inventory.
Thought 3: I need to collect wood now.
Action 3: Act[Do, 5, 1]
Observation 3: There is grass 1 steps to your west, tree 3 steps to your west. You face grass at your front. Your inventory is 1 wood.
Thought 4: I need to move to the tree in my south-west and collect wood.
Action 4: Act[Move West, 1, 2]
Observation 4: There is grass 2 steps to your north-east, sand 6 steps to your south-west, tree 1 steps to your west. You face tree at your front. Your inventory is 1 wood.
Thought 5: I need to collect wood now.
Action 5: Act[Do, 5, 1]
Observation 5: There is grass 2 steps to your north-east, sand 6 steps to your south-west, tree 3 steps to your south-east. You face grass at your front. Your inventory is 2 wood.
Thought 6: I have enough wood and can place table now.
Action 6: Act[Place Table, 8, 1]
Observation 6:There is grass 2 steps to your north-east, sand 6 steps to your south-west, tree 3 steps to your south-east, table 1 step to your west. You face table at your front. You have nothing in your inventory.
Thought 7: I have already placed table.
Action 7: Finish[Place Table]

Task: Make Wood Pickaxe.
Thought 1: I need to collect one wood to make wood pickaxe.
Action 1: Act[Move South, 4, 1]
Observation 1: There is water 4 steps to your south-west, grass 1 steps to your west, sand 2 steps to your south-west, tree 1 steps to your south. You face tree at your front. You have nothing in your inventory.
Thought 2: I need to collect wood now.
Action 2: Act[Do, 5, 1]
Observation 2: There is water 4 steps to your south-west, grass 1 steps to your west, sand 2 steps to your south-west. You face grass at your front. Your inventory is 1 wood.
Thought 3: I need to back to table and make wood pickaxe.
Action 3: Act[Move North, 3, 1]
Observation 3: There is water 4 steps to your south-west, grass 1 steps to your west, sand 2 steps to your south-west. You face table at your front. Your inventory is 1 wood.
Thought 4: I can make wood pickaxe now.
Action 4: Act[Make Wood Pickaxe, 11, 1]
Observation 4: There is water 4 steps to your south-west, grass 1 steps to your west, sand 2 steps to your south-west. You face grass at your front. Your inventory is 1 wood pickaxe.
Thought 5: I have already made wood pickaxe.
Action 4: Finish[Make Wood Pickaxe]

Task: Place Furnace.
Thought 1: I need to collect stone to place furnace.
Action 1: Act[Move North, 3, 1]
Observation 1: There is grass 1 steps to your south, stone 1 steps to your west, path 2 steps to your south-west, tree 5 steps to your north-west, table 4 steps to your south-east. You face stone at your front. Your inventory is 1 wood pickaxe.
Thought 2: I need to collect stone now.
Action 2: Act[Do, 5, 1]
Observation 2: There is grass 1 steps to your south, stone 1 steps to your west, path 1 steps to your south-west, tree 5 steps to your north-west, table 4 steps to your south-east. You face path at your front. Your inventory is 1 wood pickaxe, 1 stone.
Thought 3: Now, I have 1 stone in my inventory, I need to collect more stone.
Action 3: Act[Move West, 1, 1]
Observation 3: There is grass 1 steps to your south, stone 1 steps to your west, path 1 steps to your north, tree 5 steps to your north-west, table 4 steps to your south-east. You face stone at your front. Your inventory is 1 wood pickaxe, 1 stone.
Thought 4: I need to collect stone now.
Action 4: Act[Do, 5, 1]
Observation 4: There is grass 1 steps to your south, stone 2 steps to your west, path 1 steps to your north, tree 5 steps to your north-west, table 4 steps to your south-east. You face grass at your front. Your inventory is 1 wood pickaxe, 2 stone.
Thought 5: I need to collect more stone.
Action 5: Act[Move North, 3, 1]
Observation 5: There is grass 1 steps to your south, path 1 steps to your west, stone 1 steps to your north, tree 5 steps to your north-west, table 4 steps to your south-east. You face stone at your front. Your inventory is 1 wood pickaxe, 2 stone.
Thought 6: I can collect stone now.
Action 6: Act[Do, 5, 1]
Observation 6: There is grass 1 steps to your south, path 1 steps to your west, stone 2 steps to your north, tree 5 steps to your north-west, table 4 steps to your south-east. You face grass at your front. Your inventory is 1 wood pickaxe, 3 stone.
Thought 6: I need to collect one more stone.
Action 6: Act[Move North, 3, 1]
Observation 6: There is grass 1 steps to your south, stone 1 steps to your north, path 1 steps to your west, table 4 steps to your south-east. You face stone at your front. Your inventory is 1 wood pickaxe, 3 stone.
Thought 7: I can collect stone now.
Action 7: Act[Do, 5, 1]
Observation 7: There is grass 1 steps to your south, tree 3 steps to your north, path 1 steps to your west, table 4 steps to your south-east. You face grass at your front. Your inventory is 1 wood pickaxe, 4 stone.
Thought 8: Now I can place furnace.
Action 8: Act[Move East, 2, 1]
Observation 8: There is grass 1 steps to your south, stone 1 steps to your north, path 1 steps to your west, tree 4 steps to your east, table 4 steps to your south-east. You face grass at your front. Your inventory is 1 wood pickaxe.
Thought 9: Now I can place furnace.
Action 9: Act[Place Furnace, 9, 1]
Observation 9: There is grass 1 steps to your south, stone 1 steps to your north, path 1 steps to your west, tree 4 steps to your east, table 4 steps to your south-east, furnace 1 steps to your east. You face furnace at your front. Your inventory is 1 wood pickaxe.
Though 10: I have placed furnace.
Action 10: Finish[Place Furnace]
"""

CRAFTER_REFLECTIONS = """
Previous Trial:
Task: Collect Wood.
Thought 1: I should find a tree and then collect wood.
Action 1: Act[Move South, 4, 1]
Observation 1: There is water 7 steps to your south-east, grass 1 steps to your west, sand 5 steps to your south-east, tree 4 steps to your west. You face grass at your front. You have nothing in your inventory.
Thought 2: The tree is 4 steps to my west, so I need to move west to collect wood.
Action 2: Act[Move West, 1, 2]
Observation 2: There is grass 1 steps to your west, sand 5 steps to your south-west, tree 2 steps to your west. You face grass at your front. You have nothing in your inventory.
Thought 3: I can collect wood now.
Action 3: Act[Do, 5, 1]
Observation 3: There is grass 1 steps to your west, sand 5 steps to your south-west, tree 2 steps to your west. You face grass at your front. You have nothing in your inventory.
Thought 4: I have finished this task.
Action 4: Finish[Collect Wood]

Reflection: I consider I have already collected wood. But I didn't reach the front of the tree. I need to move one more step to reach in front of the tree. And then collect wood.

Previous Trial:
Task: Place Table.
Thought 1: I need to collect wood first to place table, then I need to collect wood to make wood pickaxe, finally I need to collect coal using the wood pickaxe.
Action 1: Act[Move South, 4, 3]
Observation 1: There is water 7 steps to your south-east, grass 1 steps to your west, tree 2 steps to your south. You face grass at your front. You have nothing in your inventory.
Thought 2: I need to go to the front of the tree to get the wood.
Action 2: Act[Move South, 4, 1]
Observation 2: There is grass 1 steps to your west, tree 1 steps to your south. You face tree at your front. You have nothing in your inventory.
Thought 3: I need to collect wood now.
Action 3: Act[Do, 5, 1]
Observation 3: There is grass 1 steps to your west, tree 3 steps to your west. You face grass at your front. Your inventory is 1 wood.
Thought 4: I need to move to the tree in my south-west and collect wood.
Action 4: Act[Move West, 1, 2]
Observation 4: There is grass 2 steps to your north-east, sand 6 steps to your south-west, tree 1 steps to your west. You face tree at your front. Your inventory is 1 wood.
Thought 5: I need to collect wood now.
Action 5: Act[Do, 5, 1]
Observation 5: There is grass 2 steps to your north-east, sand 6 steps to your south-west, tree 3 steps to your south-east, stone 1 steps to your west. You face stone at your front. Your inventory is 2 wood.
Thought 6: I have enough wood and can place table now.
Action 6: Act[Place Table, 8, 1]
Observation 6:There is grass 2 steps to your north-east, sand 6 steps to your south-west, tree 3 steps to your south-east, stone 1 steps to your west. You face stone at your front. Your inventory is 2 wood.
Thought 7: I have already placed table.
Action 7: Finish[Place Table]

Reflection: Because there is a stone in front of me, so I can't place table here. I should go to the place where the grass is in front of me. And then place table.
"""

CRAFTER_FEEDBACK = """ """