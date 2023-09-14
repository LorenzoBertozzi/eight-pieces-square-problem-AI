import heapq

class PuzzleNode:

    def __init__(self, state, parent=None, action=None):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = 0 if parent is None else parent.cost + 1
    
    def __lt__(self, other):
        return (self.cost + self.heuristic()) < (other.cost + other.heuristic())

    def __eq__(self, other):
        return self.state == other.state

    def __hash__(self):
        return hash(self.state)

    def is_goal(self, goal_state):
        return self.state == goal_state

    def find_legal_actions(self):
        actions = []
        i, j = self.state.index(0) // 3, self.state.index(0) % 3  # Find the empty square
        if i > 0:
            actions.append('Up')
        if i < 2:
            actions.append('Down')
        if j > 0:
            actions.append('Left')
        if j < 2:
            actions.append('Right')
        return actions

    def move(self, action):
        i, j = self.state.index(0) // 3, self.state.index(0) % 3
        new_state = list(self.state)
        if action == 'Up':
            new_i = i - 1
            new_state[i * 3 + j], new_state[new_i * 3 + j] = new_state[new_i * 3 + j], new_state[i * 3 + j]
        elif action == 'Down':
            new_i = i + 1
            new_state[i * 3 + j], new_state[new_i * 3 + j] = new_state[new_i * 3 + j], new_state[i * 3 + j]
        elif action == 'Left':
            new_j = j - 1
            new_state[i * 3 + j], new_state[i * 3 + new_j] = new_state[i * 3 + new_j], new_state[i * 3 + j]
        elif action == 'Right':
            new_j = j + 1
            new_state[i * 3 + j], new_state[i * 3 + new_j] = new_state[i * 3 + new_j], new_state[i * 3 + j]
        return PuzzleNode(tuple(new_state), self, action)

    def heuristic(self):
      total_distance = 0;
      for i in range(3):
          for j in range(3):
              if self.state[i * 3 + j] != 0:
                  goal_position = goal_state.index(self.state[i * 3 + j])
                  goal_i, goal_j = goal_position // 3, goal_position % 3
                  total_distance += abs(i - goal_i) + abs(j - goal_j)
      return total_distance

def solve_puzzle(initial_state, goal_state):
    open_set = [PuzzleNode(initial_state)]
    closed_set = set()
    
    while open_set:
        current_node = heapq.heappop(open_set)
        
        if current_node.is_goal(goal_state):
            solution = []
            while current_node.parent:
                solution.append(current_node.action)
                current_node = current_node.parent
            solution.reverse()
            return solution
        
        closed_set.add(current_node)
        
        for action in current_node.find_legal_actions():
            child_node = current_node.move(action)
            if child_node in closed_set:
                continue
            if child_node not in open_set:
                heapq.heappush(open_set, child_node)
    
    return None

# Exemplo de uso:
initial_state = (1, 2, 3, 0, 4, 6, 7, 5, 8)  # Estado inicial
goal_state = (1, 2, 3, 4, 5, 6, 7, 8, 0)  # Estado objetivo

solution = solve_puzzle(initial_state, goal_state)
if solution:
    print("Solução encontrada:", solution)
else:
    print("Não foi possível encontrar uma solução.")
