#!/usr/bin/python3

import sys

# State Representation
# 123804765
state = 1*10**8 + 2*10**7 + 3*10**6 +\
         8*10**5 + 0*10**4 + 4*10**3 +\
         7*10**2 + 6*10**1 + 5*10**0


def get_place(state, n):
    return str(state // 10**n % 10)


get_place(state, 1)
get_place(state, 5)
get_place(state, 8)


def visualize(state):
    divider = " " + "-"*11 + " "
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
    loc = str(state).find('0')
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
    pstate = parent.state
    loc = str(pstate).find('0')
    temp = str(pstate)[loc]
    if action == 'Up':
        if loc in [0, 1, 2, 3, 4, 5]:
            temp = str(pstate)[loc+3]
    if action == 'Down':
        if loc in [3, 4, 5, 6, 7, 8]:
            temp = str(pstate)[loc-3]
    if action == 'Left':
        if loc in [0, 1, 3, 4, 6, 7]:
            temp = str(pstate)[loc+1]
    if action == 'Right':
        if loc in [1, 2, 4, 5, 7, 8]:
            temp = str(pstate)[loc-1]
    newstate = str(pstate).replace(temp, '*')
    newstate = newstate.replace('0', temp)
    newstate = int(newstate.replace('*', '0'))
    child = Node(newstate, parent, action, parent.path_cost + 1)
    return child


initial_node = Node(123804765)

visualize(child_node(child_node(child_node(child_node(initial_node, 'Up'), 'Up'), 'Right'), 'Down').state)
child_node(child_node(child_node(child_node(initial_node, 'Up'), 'Up'), 'Right'), 'Down').path_cost

target_state = 123804765

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


def Print_Solution(solution_node):
    if type(solution_node) != type(Node(1)):
        if solution_node == []:
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
    return actions


solution = Depth_First_Search(120843765, 123804765)
Print_Solution(solution)

def Depth_Limited_Search(initial_state, target_state, depth_cutoff):
    initial_node = Node(initial_state)
    frontier = []
    frontier.append(initial_node)
    reached = []
    reached.append(initial_node.state)
    result = []
    while frontier:
        this_node = frontier.pop()
        # print("State: " + str(this_node.state) + "; Depth: " + str(this_node.depth))
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

solution = Depth_Limited_Search(102843765, 123804765, 2)
Print_Solution(solution)

def iterative_deepening(initial_state, target_state):
    depth = 0
    while depth > -1:
        result = Depth_Limited_Search(initial_state, target_state, depth)
        depth += 1
        if result != 'cutoff':
            return result

solution = iterative_deepening(102843765, 123804765)
Print_Solution(solution)
