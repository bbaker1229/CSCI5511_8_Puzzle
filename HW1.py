#!/usr/bin/python3

import sys

# State Representation
# 123804765
state = 1*10**8 + 2*10**7 + 3*10**6 +\
         8*10**5 + 0*10**4 + 4*10**3 +\
         7*10**2 + 6*10**1 + 5*10**0


def get_value_by_location(state, loc):
    value = state // 10**loc % 10
    return value


def get_location_by_value(state, value):
    for loc in range(9):
        if get_value_by_location(state, loc) == value:
            return loc


def replace(state, loc, value):
    newstate = 0
    for i in range(9):
        if i == loc:
            place = value*10**i
        else:
            place = get_value_by_location(state, i)*10**i
        newstate += place
    return newstate


state = 123804765
get_value_by_location(state, 1)  # This is 6
get_value_by_location(state, 5)  # This is 8
get_value_by_location(state, 8)  # This is 1

get_location_by_value(state, 0)  # This is 4

state = 12345678
get_value_by_location(state, 8)  # This is 0
get_location_by_value(state, 0)  # This is 8

replace(state, 0, 9)
replace(state, 8, 4)


def visualize(state):
    divider = " " + "-"*11 + " "
    print(divider)
    for loc in range(8, -1, -1):
        val = str(get_value_by_location(state, loc))
        if val == '0':
            val = '*'
        place = "| " + val + " "
        print(place, end="")
        if loc in [6, 3, 0]:
            print("|")
            print(divider)


visualize(state)

value = sys.argv[1]
print(str(value))


class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1


def possible_actions(state):
    loc = get_location_by_value(state, 0)
    actions = []
    if loc in [8, 7, 6, 5, 4, 3]:
        actions.append('Up')
    if loc in [5, 4, 3, 2, 1, 0]:
        actions.append('Down')
    if loc in [8, 7, 5, 4, 2, 1]:
        actions.append('Left')
    if loc in [7, 6, 4, 3, 1, 0]:
        actions.append('Right')
    return actions


possible_actions(12345678)
possible_actions(123804765)
possible_actions(120345678)
possible_actions(123456078)
possible_actions(123456780)
possible_actions(102345678)
possible_actions(123045678)
possible_actions(123450678)
possible_actions(123456708)


def child_node(parent, action):
    pstate = parent.state
    loc = get_location_by_value(pstate, 0)
    val_loc = loc
    if action == 'Up' and loc in [8, 7, 6, 5, 4, 3]:
        val_loc = loc - 3
    if action == 'Down' and loc in [5, 4, 3, 2, 1, 0]:
        val_loc = loc + 3
    if action == 'Left' and loc in [8, 7, 5, 4, 2, 1]:
        val_loc = loc - 1
    if action == 'Right' and loc in [7, 6, 4, 3, 1, 0]:
        val_loc = loc + 1
    temp = get_value_by_location(pstate, val_loc)
    newstate = replace(pstate, val_loc, 9)
    newstate = replace(newstate, loc, temp)
    newstate = replace(newstate, val_loc, 0)
    child = Node(newstate, parent, action, parent.path_cost + 1)
    return child


initial_node = Node(123804765)
child_node(initial_node, 'Up').state
child_node(initial_node, 'Down').state
child_node(initial_node, 'Left').state
child_node(initial_node, 'Right').state

visualize(child_node(child_node(child_node(child_node(initial_node, 'Up'), 'Up'), 'Right'), 'Down').state)
child_node(child_node(child_node(child_node(initial_node, 'Up'), 'Up'), 'Right'), 'Down').path_cost

target_state = 123804765


def is_cycle(node):
    current_state = node.state
    while node.parent is not None:
        node = node.parent
        if node.state == current_state:
            return True
    return False


def Depth_First_Search(initial_state, target_state):
    initial_node = Node(initial_state)
    frontier = []
    frontier.append(initial_node)
    reached = []
    reached.append(initial_node.state)
    while frontier:
        this_node = frontier.pop()
        # print("State: " + str(this_node.state) + "; Depth: " + str(this_node.depth))
        if this_node.state == target_state:
            return this_node
        actions = possible_actions(this_node.state)
        actions.reverse()
        for action in actions:
            child = child_node(this_node, action)
            if child.state not in reached:
                frontier.append(child)
                reached.append(child.state)
    return []


def Depth_First_Search(initial_state, target_state):
    # This works but stop using reached list
    initial_node = Node(initial_state)
    reached = [initial_node.state]
    if initial_node.state == target_state:
        return initial_node
    this_node = child_node(initial_node, 'Up')
    while this_node.parent != None:
        # check if we have seen this state
        if this_node.state == target_state:
            return this_node
        if this_node.state in reached:
            action = this_node.action
            parent = this_node.parent
            if action == 'Up':
                this_node = child_node(parent, 'Down')
            if action == 'Down':
                this_node = child_node(parent, 'Left')
            if action == 'Left':
                this_node = child_node(parent, 'Right')
            if action == 'Right':
                this_node = parent
        else:
            reached.append(this_node.state)
            this_node = child_node(this_node, 'Up')
        print("State: " + str(this_node.state) + "; Depth: " + str(this_node.depth))
    return []


def Depth_First_Search(initial_state, target_state):
    initial_node = Node(initial_state)
    if initial_node.state == target_state:
        return initial_node
    actions = possible_actions(initial_node.state)
    this_node = child_node(initial_node, actions[0])
    back = False
    while this_node.parent != None:
        # check if we have seen this state
        if back:
            parent = this_node.parent
            action = this_node.action
            actions = possible_actions(parent.state)
            ind = actions.index(action)
            if ind == (len(actions) - 1):
                this_node = parent
                continue
            else:
                this_node = child_node(parent, actions[ind + 1])
                back = False
                continue
        if this_node.state == target_state:
            return this_node
        actions = possible_actions(this_node.state)
        for action in actions:
            next_node = child_node(this_node, action)
            if is_cycle(next_node):
                continue
            else:
                this_node = next_node
                break
        if this_node != next_node:
            back = True
        print("State: " + str(this_node.state) + "; Depth: " + str(this_node.depth))
    return []


def Print_Solution(solution_node):
    if not isinstance(solution_node, Node):
        if not solution_node:
            print("No solution found.")
        else:
            print("Error: This is not a node.")
        return None
    node = solution_node
    actions = []
    while node.parent is not None:
        actions.append(node.action)
        node = node.parent
    actions.reverse()
    print(actions)
    return None


solution = Depth_First_Search(120843765, 123804765)
Print_Solution(solution)


def Depth_Limited_Search(initial_state, target_state, depth_cutoff):
    initial_node = Node(initial_state)
    if initial_node.state == target_state:
        return initial_node
    actions = possible_actions(initial_node.state)
    this_node = child_node(initial_node, actions[0])
    back = False
    while this_node.parent != None:
        # check if we have seen this state
        if back:
            parent = this_node.parent
            action = this_node.action
            actions = possible_actions(parent.state)
            ind = actions.index(action)
            if ind == (len(actions) - 1):
                this_node = parent
                continue
            else:
                this_node = child_node(parent, actions[ind + 1])
                back = False
                continue
        if this_node.state == target_state:
            return this_node
        if this_node.depth > depth_cutoff:
            back = True
            result = "cutoff"
            continue
        actions = possible_actions(this_node.state)
        for action in actions:
            next_node = child_node(this_node, action)
            if is_cycle(next_node):
                continue
            else:
                this_node = next_node
                break
        if this_node != next_node:
            back = True
        # print("State: " + str(this_node.state) + "; Depth: " + str(this_node.depth))
    return result


solution = Depth_Limited_Search(102843765, 123804765, 2)
Print_Solution(solution)


def iterative_deepening(initial_state, target_state):
    depth = 0
    while depth > -1:
        print(depth)
        result = Depth_Limited_Search(initial_state, target_state, depth)
        depth += 1
        if result != 'cutoff':
            return result


solution = iterative_deepening(102843765, 123804765)
Print_Solution(solution)


def num_wrong_tiles(state, target):
    cnt = 0
    for i in range(9):
        if get_value_by_location(state, i) != get_value_by_location(target, i):
            cnt += 1
    if cnt > 1:
        cnt -= 1
    return cnt


num_wrong_tiles(120843765, 123804765)


def manhattan_distance(state, target):
    cnt = 0
    for i in range(1, 9):
        state_loc = get_location_by_value(state, i)
        target_loc = get_location_by_value(target, i)
        if state_loc != target_loc:
            if state_loc in [0, 1, 2, 6, 7, 8] and target_loc in [3, 4, 5]:
                cnt += 1
            if state_loc in [0, 1, 2] and target_loc in [6, 7, 8]:
                cnt += 2
            if state_loc in [3, 4, 5] and target_loc in [0, 1, 2, 6, 7, 8]:
                cnt += 1
            if state_loc in [6, 7, 8] and target_loc in [0, 1, 2]:
                cnt += 2
            if state_loc in [0, 3, 6, 2, 5, 8] and target_loc in [1, 4, 7]:
                cnt += 1
            if state_loc in [0, 3, 6] and target_loc in [2, 5, 8]:
                cnt += 2
            if state_loc in [1, 4, 7] and target_loc in [0, 3, 6, 2, 5, 8]:
                cnt += 1
            if state_loc in [2, 5, 8] and target_loc in [0, 3, 6]:
                cnt += 2
    return cnt


manhattan_distance(713864025, 123804765)


def astar(initial_state, target_state, method):
    initial_node = Node(initial_state)
    frontier = [initial_node]
    reached = [initial_node.state]
    if method == "num_wrong_tiles":
        value = num_wrong_tiles(initial_node.state, target_state)
    if method == "manhattan_distance":
        value = manhattan_distance(initial_node.state, target_state)
    rank = [initial_node.path_cost + value]
    while frontier:
        ind = rank.index(min(rank))
        this_node = frontier.pop(ind)
        rank.pop(ind)
        if this_node.state == target_state:
            return this_node
        actions = possible_actions(this_node.state)
        # actions.reverse()
        for action in actions:
            child = child_node(this_node, action)
            if child.state not in reached:
                if method == "num_wrong_tiles":
                    value = num_wrong_tiles(child.state, target_state)
                if method == "manhattan_distance":
                    value = manhattan_distance(child.state, target_state)
                frontier.append(child)
                rank.append(child.path_cost + value)
                reached.append(child.state)
    return []


solution = astar(120843765, 123804765, "num_wrong_tiles")
Print_Solution(solution)

solution = astar(120843765, 123804765, "manhattan_distance")
Print_Solution(solution)

# Interesting states:
# 350214876
# 378615042
# 567031428 # This takes the longest time
