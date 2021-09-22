#!/usr/bin/python3

""""
Bryan Baker
bake1358@umn.edu
CSCI 5511 - Homework 1

A note on state representations:
All states are represented by integers.
Three functions were written to help deal with these states: get_value_by_location
, get_location_by_value, and replace.  Basically the value from position 2 of the state integer
(which would be the hundreds place) can be found by: state // 10**n % 10
where n would be 2 in this case.
"""

import sys
import time
from queue import PriorityQueue


class Node:
    """
    Class for storing node information
    """
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1


def get_value_by_location(state, loc):
    """
    Will get the number in a certain location from a state representation.
    :param state: State as an integer
    :param loc: Location as an integer
    :return: The value located in location loc
    """
    value = state // 10**loc % 10
    return value


def get_location_by_value(state, value):
    """
    Will get the location for a certain value from a state representation.
    :param state: State as an integer
    :param value: Value to find as an integer
    :return: The location of the value in the state
    """
    for loc in range(9):
        if get_value_by_location(state, loc) == value:
            return loc


def replace(state, loc, value):
    """
    Replace the value at a location in the state representation with a new value.
    :param state: State as an integer
    :param loc: Location as an integer
    :param value: New value to replace at this location
    :return: A new state representation with the value replaced in the appropriate location.
    """
    new_state = 0
    for i in range(9):
        if i == loc:
            place = value*10**i
        else:
            place = get_value_by_location(state, i)*10**i
        new_state += place
    return new_state


def is_cycle(node):
    """
    This is a test for cycles within a node.  It is used for Depth Search.
    :param node: This is an object with class Node.
    :return: Returns true if a cycle is found and false otherwise.
    """
    current_state = node.state
    while node.parent is not None:
        node = node.parent
        if node.state == current_state:
            return True
    return False


def possible_actions(state):
    """
    This function will return the possible next actions from a given state.  The results will be
    returned in the order: Up, Down, Left, Right.  Up will always be before Down, etc.
    :param state: State as an integer
    :return: A list of possible actions from this state.
    """
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


def child_node(parent, action):
    """
    This function will return a child node created when an action is performed on a node.
    :param parent: An object with the class Node.  The starting node.
    :param action: An action (Up, Down, Left, Right) to perform on a state
    :return: An object with the class Node which has been acted upon by the direction given in action.
    """
    p_state = parent.state
    loc = get_location_by_value(p_state, 0)
    val_loc = loc
    if action == 'Up' and loc in [8, 7, 6, 5, 4, 3]:
        val_loc = loc - 3
    if action == 'Down' and loc in [5, 4, 3, 2, 1, 0]:
        val_loc = loc + 3
    if action == 'Left' and loc in [8, 7, 5, 4, 2, 1]:
        val_loc = loc - 1
    if action == 'Right' and loc in [7, 6, 4, 3, 1, 0]:
        val_loc = loc + 1
    temp = get_value_by_location(p_state, val_loc)
    new_state = replace(p_state, val_loc, 9)  # Replace the value with a 9 because 9 is never used.
    new_state = replace(new_state, loc, temp)
    new_state = replace(new_state, val_loc, 0)
    child = Node(new_state, parent, action, parent.path_cost + 1)
    return child


def depth_first_search(initial_state, target_state):
    """
    This is depth first search.  This function will start with an initial state and attempt to reach the
    target state through iterations of child nodes.  When a child node is created the cycles are checked
    and if there are no cycles we travel to that node.  If no new moves are possible the algorithm backs
    up and checks the next possible action of it's parent node.  If still no action possible it will
    continue up the chain until one is found.  This procedure can take a very long time.
    :param initial_state: A state as an integer
    :param target_state: A state as an integer
    :return: A node that is a solution to get from the initial state to the target state.
    """
    initial_node = Node(initial_state)
    if initial_node.state == target_state:  # Check if this first node is a solution
        return initial_node
    actions = possible_actions(initial_node.state)
    this_node = child_node(initial_node, actions[0])  # Get the possible actions and take the first one.
    back = False  # This is a flag to notify if we need to back up the chain.
    while this_node.parent is not None:
        if back:  # This section is only if we are moving back up the chain to find a new path,
            parent = this_node.parent
            action = this_node.action
            actions = possible_actions(parent.state)
            ind = actions.index(action)
            if ind == (len(actions) - 1):
                # If this node is a child of the last possible move of it's parent node
                # then continue up the chain.
                this_node = parent
                continue
            else:
                # Otherwise go to the next action and continue forward.
                this_node = child_node(parent, actions[ind + 1])
                back = False
                continue
        if this_node.state == target_state:  # Return a node if we have found a solution.
            return this_node
        actions = possible_actions(this_node.state)
        # Find the next actions for this node and test the child nodes for cycles.  If no cycles
        # go to the first node that is cycle free.
        for action in actions:
            next_node = child_node(this_node, action)
            if is_cycle(next_node):
                continue
            else:
                this_node = next_node
                break
        if this_node != next_node:  # If this node has not been reset then go back up the chain.
            back = True
    return []


def depth_limited_search(initial_state, target_state, depth_cutoff):
    """
    This is the same search as the depth first search but is limited in depth by the variable in
    depth_cutoff.  Once a child node has reached the depth_cutoff the chain will backup and try to find
    and new route.
    :param initial_state: A state as an integer
    :param target_state: A state as an integer
    :param depth_cutoff: If we find a node that is deeper than this value we will backup and find
    a new path.
    :return: A node that is a solution to get from the initial state to the target state.
    """
    initial_node = Node(initial_state)
    if initial_node.state == target_state:  # Check if this first node is a solution
        return initial_node
    actions = possible_actions(initial_node.state)
    this_node = child_node(initial_node, actions[0])  # Get the possible actions and take the first one.
    back = False  # This is a flag to notify if we need to back up the chain.
    while this_node.parent is not None:
        if back:  # This section is only if we are moving back up the chain to find a new path,
            parent = this_node.parent
            action = this_node.action
            actions = possible_actions(parent.state)
            ind = actions.index(action)
            if ind == (len(actions) - 1):
                # If this node is a child of the last possible move of it's parent node
                # then continue up the chain.
                this_node = parent
                continue
            else:
                # Otherwise go to the next action and continue forward.
                this_node = child_node(parent, actions[ind + 1])
                back = False
                continue
        if this_node.state == target_state:  # Return a node if we have found a solution.
            return this_node
        if this_node.depth > depth_cutoff:  # If we have reached the depth_cutoff, backup.
            back = True
            result = "cutoff"
            continue
        actions = possible_actions(this_node.state)
        # Find the next actions for this node and test the child nodes for cycles.  If no cycles
        # go to the first node that is cycle free.
        for action in actions:
            next_node = child_node(this_node, action)
            if is_cycle(next_node):
                continue
            else:
                this_node = next_node
                break
        if this_node != next_node:  # If this node has not been reset then go back up the chain.
            back = True
    return result


def iterative_deepening(initial_state, target_state):
    """
    This function is used in conjunction with the depth limited search.  The depth will be allowed to
    go deeper once we have searched through the shallowest nodes first.
    :param initial_state: A state as an integer
    :param target_state: A state as an integer
    :return: A node that is a solution to get from the initial state to the target state.
    """
    depth = 0
    while depth > -1:
        result = depth_limited_search(initial_state, target_state, depth)
        depth += 1
        if result != 'cutoff':
            return result


def num_wrong_tiles(state, target):
    """
    This is a heuristic function that counts the number of tiles that are in the wrong locations.
    Used for A* search.
    :param state: A state as an integer
    :param target: A state as an integer
    :return: A count of the number of values in the incorrect locations compared to the target state.
    """
    cnt = 0
    for i in range(9):  # Loop through all locations and compare to target
        if get_value_by_location(state, i) != get_value_by_location(target, i):
            cnt += 1
    if cnt > 1:  # This corrects to prevent double counting the missing tile.
        cnt -= 1
    return cnt


def manhattan_distance(state, target):
    """
    This is a heuristic function that returns the sum for all the manhattan distances for each tile
    from it's correct position.
    :param state: A state as an integer
    :param target: A state as an integer
    :return: A count of the manhattan distances to move each tile to it's correct position.
    """
    cnt = 0
    for i in range(1, 9):  # Loop through all locations
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


def print_solution(solution_node):
    """
    This function prints the solution from a solution node once a search method has found a solution.
    :param solution_node: An object of class Node that is a potential solution.
    :return: Nothing returned, just print all moves to the screen.
    """
    if not isinstance(solution_node, Node):  # Check that this node is of class Node
        if not solution_node:
            print("No solution found.")
        else:
            print("Error: This is not a node.")
        return None
    node = solution_node
    actions = []
    while node.parent is not None:
        # Find the action of this node then continue through the chain
        # until the parent node is reached.
        actions.append(node.action)
        node = node.parent
    actions.reverse()  # The actions are given from solution to initial state.  We need to reverse that.
    print(actions)
    return None


def visualize(state):
    """
    This funciton will print a state to the screen in an easy to understand format.
    :param state: A state as an integer
    :return: Nothing is returned.
    """
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


def astar(initial_state, target_state, method):
    """
    This is A* search.  The method to use as a heuristic is passed into this function.
    :param initial_state: A state as an integer
    :param target_state: A state as an integer
    :param method: The method to use as a heuristic: num_wrong_tiles or manhattan_distance
    :return: A node that is a solution to get from the initial state to the target state.
    """
    initial_node = Node(initial_state)
    reached = {initial_node.state: initial_node}  # This is a dictionary keyed by state for all reached nodes
    value = 0
    if method == "num_wrong_tiles":
        value = num_wrong_tiles(initial_node.state, target_state)
    if method == "manhattan_distance":
        value = manhattan_distance(initial_node.state, target_state)
    frontier = PriorityQueue()  # This is a queue to store the ranks for each state.
    frontier.put((initial_node.path_cost + value, initial_node.state))
    while frontier:
        # First we find the state with the smallest rank and remove it from the frontier.
        state = frontier.get()[1]
        this_node = reached[state]
        if this_node.state == target_state:  # Return a node if we have found a solution
            return this_node
        actions = possible_actions(this_node.state)
        # Find the next possible actions from this node and if we have not reached them
        # add them to the frontier queue and the reached dictionary.
        for action in actions:
            child = child_node(this_node, action)
            if child.state not in reached:
                if method == "num_wrong_tiles":
                    value = num_wrong_tiles(child.state, target_state)
                if method == "manhattan_distance":
                    value = manhattan_distance(child.state, target_state)
                reached[child.state] = child
                frontier.put((child.path_cost + value, child.state))
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
        initial_state = int(initial_state)  # Sets the initial state
    else:
        # Check that the initial state is an integer.  Give an example.
        print("The puzzle configuration should be entered as a nine digit integer.")
        print("Example:")
        visualize(123456780)
        print("This would be entered as: 123456780")
        print(" ")
        exit()

    # Set the target state
    target_state = 123804765  # Sets the target state

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
