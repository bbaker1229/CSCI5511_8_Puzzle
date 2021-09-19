#!/usr/bin/python3


import sys
import time


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
    state = str(state)
    if len(state) != 9:
        state = '0' + state
    loc = state.find('0')
    actions = []
    if loc in [0, 1, 2, 3, 4, 5]:
        actions.append('Up')
    if loc in [3, 4, 5, 6, 7, 8]:
        actions.append('Down')
    if loc in [0, 1, 3, 4, 6, 7]:
        actions.append('Left')
    if loc in [1, 2, 4, 5, 7, 8]:
        actions.append('Right')
    return actions


def child_node(parent, action):
    pstate = str(parent.state)
    if len(pstate) != 9:
        pstate = '0' + pstate
    loc = pstate.find('0')
    temp = pstate[loc]
    if action == 'Up':
        if loc in [0, 1, 2, 3, 4, 5]:
            temp = pstate[loc + 3]
    if action == 'Down':
        if loc in [3, 4, 5, 6, 7, 8]:
            temp = pstate[loc - 3]
    if action == 'Left':
        if loc in [0, 1, 3, 4, 6, 7]:
            temp = pstate[loc + 1]
    if action == 'Right':
        if loc in [1, 2, 4, 5, 7, 8]:
            temp = pstate[loc - 1]
    newstate = pstate.replace(temp, '*')
    newstate = newstate.replace('0', temp)
    newstate = int(newstate.replace('*', '0'))
    child = Node(newstate, parent, action, parent.path_cost + 1)
    return child


def depth_first_search(initial_state, target_state):
    initial_node = Node(initial_state)
    frontier = [initial_node]
    reached = [initial_node.state]
    while frontier:
        this_node = frontier.pop()
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


def depth_limited_search(initial_state, target_state, depth_cutoff):
    initial_node = Node(initial_state)
    frontier = [initial_node]
    reached = [initial_node.state]
    result = []
    while frontier:
        this_node = frontier.pop()
        if this_node.state == target_state:
            return this_node
        if this_node.depth > depth_cutoff:
            result = "cutoff"
        else:
            actions = possible_actions(this_node.state)
            actions.reverse()
            for action in actions:
                child = child_node(this_node, action)
                if child.state not in reached:
                    frontier.append(child)
                    reached.append(child.state)
    return result


def iterative_deepening(initial_state, target_state):
    depth = 0
    while depth > -1:
        result = depth_limited_search(initial_state, target_state, depth)
        depth += 1
        if result != 'cutoff':
            return result


def num_wrong_tiles(state, target):
    cnt = 0
    for i in range(9):
        if get_place(state, i) != get_place(target, i):
            cnt += 1
    if cnt > 1:
        cnt -= 1
    return cnt


def manhattan_distance(state, target):
    state = str(state)
    target = str(target)
    if len(state) != 9:
        state = '0' + state
    if len(target) != 9:
        target = '0' + target
    cnt = 0
    for i in range(1, 9):
        state_loc = state.find(str(i))
        target_loc = target.find(str(i))
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


def print_solution(solution_node):
    if not isinstance(solution_node, Node):
        if not solution_node:
            print("No solution found.")
        else:
            print("Error: This is not a node.")
        return None
    depth = solution_node.depth
    actions = []
    for node in range(depth):
        if node == 0:
            actions.append(solution_node.action)
        else:
            solution_node = solution_node.parent
            actions.append(solution_node.action)
    actions.reverse()
    print(actions)
    return None


def get_place(state, n):
    return str(state // 10 ** n % 10)


def visualize(state):
    divider = " " + "-" * 11 + " "
    print(divider)
    for i in range(8, -1, -1):
        val = get_place(state, i)
        if val == '0':
            val = '*'
        place = "| " + val + " "
        print(place, end="")
        if i in [6, 3, 0]:
            print("|")
            print(divider)


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
        actions.reverse()
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


if __name__ == "__main__":
    # Test input values
    if len(sys.argv) != 2:
        # Check for the correct number of commandline args
        print("Usage: python run_me.py <puzzle config as integer>")
        print(" ")
        exit()
    initial_state = sys.argv[1]
    if len(initial_state) != 9:
        # Check that the initial state is an integer.  Give an example.
        print("The puzzle configuration should be entered as a nine digit integer.")
        print("Example:")
        visualize(123456780)
        print("This would be entered as: 123456780")
        print(" ")
        exit()
    if initial_state.isdigit():
        initial_state = int(initial_state)
    else:
        # Check that the initial state is an integer.  Give an example.
        print("The puzzle configuration should be entered as a nine digit integer.")
        print("Example:")
        visualize(123456780)
        print("This would be entered as: 123456780")
        print(" ")
        exit()
    # Set the target state
    target_state = 123804765
    # Show initial and target configuration
    print(" ")
    print("Initial State:")
    visualize(initial_state)
    print(" ")
    print("Target State:")
    visualize(target_state)
    print(" ")
    # Solve iterative deepening.
    print("Solving with iterative deepening:")
    time_start = time.perf_counter()
    solution = iterative_deepening(initial_state, target_state)
    time_end = time.perf_counter()
    iterative_deepening_time = time_end - time_start
    print("The solution is: ")
    print_solution(solution)
    print(f"The time to solve was: {iterative_deepening_time:0.6f} seconds")
    print(" ")
    # Solve A* with num_wrong_tiles
    print("Solving with A* using num_wrong_tiles:")
    time_start = time.perf_counter()
    solution = astar(initial_state, target_state, "num_wrong_tiles")
    time_end = time.perf_counter()
    astar_time = time_end - time_start
    print("The solution is: ")
    print_solution(solution)
    print(f"The time to solve was: {astar_time:0.6f} seconds")
    print(" ")
    # Solve A* with manhattan_distance
    print("Solving with A* using manhattan_distance:")
    time_start = time.perf_counter()
    solution = astar(initial_state, target_state, "manhattan_distance")
    time_end = time.perf_counter()
    astar_time = time_end - time_start
    print("The solution is: ")
    print_solution(solution)
    print(f"The time to solve was: {astar_time:0.6f} seconds")
    print(" ")
