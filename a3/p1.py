import sys
import grader
import parse
import random
from collections import Counter

DIRECTIONS = {'N': ["N", "E", "W"], "E": ["E", "S", "N"], "S": ["S", "W", "E"], "W": ["W", "N", "S"]}
DELTA = {"N": (-1, 0), "E": (0, 1), "W": (0, -1), "S": (1, 0)}
def format_reward(num):
    num_float = float(num)
    if num_float.is_integer():
        return f"{num_float:.1f}"
    else:
        formatted = f"{num_float:.2f}".rstrip('0').rstrip('.')
        return formatted if '.' in formatted else f"{formatted}.0"

def generate_action_sequence(intended, noise, seed, length=100000):
    direction_map = {
        'N': ['N', 'E', 'W'],
        'E': ['E', 'S', 'N'],
        'S': ['S', 'W', 'E'],
        'W': ['W', 'N', 'S']
    }
    random.seed(seed, version=1)
    sequence = []
    for _ in range(length):
        possible_actions = direction_map[intended]
        weights = [1 - 2*noise, noise, noise]
        chosen = random.choices(possible_actions, weights=weights, k=1)[0]
        sequence.append(chosen)
    return sequence

action_sequences = {}
current_step = 0

def play_episode(problem):
    global current_step
    start_pos = next((i, j) for i, row in enumerate(problem['grid']) 
                    for j, cell in enumerate(row) if cell == 'S')
    
    if problem['seed'] not in action_sequences:
        new_sequences = {
            'N': generate_action_sequence('N', problem['noise'], problem['seed']),
            'E': generate_action_sequence('E', problem['noise'], problem['seed']),
            'S': generate_action_sequence('S', problem['noise'], problem['seed']),
            'W': generate_action_sequence('W', problem['noise'], problem['seed'])
        }
        action_sequences[problem['seed']] = new_sequences
    current_step = 0

    cr, cc = start_pos
    cumulative = 0.0
    experience = []
    
    grid = [row.copy() for row in problem['grid']]
    grid[cr][cc] = 'P'
    experience.append(
        f"Start state:\n{format_grid(grid)}\n"
        f"Cumulative reward sum: {format_reward(cumulative)}\n"
        "-------------------------------------------- "
    )
    
    while True:
        current_cell = problem['grid'][cr][cc]
        try:
            # 尝试转换为浮点数，若能转换则为终止状态
            reward = float(current_cell)
            is_terminal = True
            action = 'exit'
            nr, nc = cr, cc
        except ValueError:
            # 非终止状态，获取策略动作
            is_terminal = False
            intended = problem['policy'][cr][cc].upper()
            action = action_sequences[problem['seed']][intended][current_step]
            current_step += 1
            nr, nc = calculate_new_pos(cr, cc, action, problem['grid'])
            reward = problem['livingReward']

        cumulative += reward
        
        new_grid = [row.copy() for row in problem['grid']]
        if not is_terminal:
            for r in range(len(new_grid)):
                new_grid[r] = ['_' if cell == 'P' else cell for cell in new_grid[r]]
            new_grid[nr][nc] = 'P'
        else:
            for r in range(len(new_grid)):
                new_grid[r] = ['_' if cell == 'P' else cell for cell in new_grid[r]]
        
        step_lines = [
            f"Taking action: {action.lower() if action == 'exit' else action.upper()} (intended: {intended if not is_terminal else 'exit'})",
            f"Reward received: {format_reward(reward)}",
            f"New state:\n{format_grid(new_grid)}",
            f"Cumulative reward sum: {format_reward(cumulative)}"
        ]
        if not is_terminal:
            step_lines.append("-------------------------------------------- ")
        experience.append('\n'.join(step_lines))
        
        cr, cc = nr, nc
        
        if is_terminal:
            break

    return '\n'.join(experience)

def format_grid(grid):
    formatted_rows = []
    for row in grid:
        formatted_cells = []
        for cell in row:
            formatted_cell = f"{cell:>5}"
            formatted_cells.append(formatted_cell)
        formatted_row = ''.join(formatted_cells)
        formatted_rows.append(formatted_row)
    return '\n'.join(formatted_rows)

def calculate_new_pos(r, c, action, grid):
    moves = {'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'W': (0, -1)}
    dr, dc = moves.get(action.upper(), (0, 0))
    nr, nc = r + dr, c + dc
    if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] != '#':
        return nr, nc
    return r, c

def check_direction_feasibility(m:int, n:int, row:int, col:int, grid:list[list[int]])->bool:
    """
    check the feasibility of the new position
    :param m: int, the height of board.
    :param n: int, the weight of board.
    :param row: int, the current row position.
    :param col: int, the current col position.
    :param grid: list[list[int]], the game board.
    :return: boolean, the feasibility of new position
    """
    if row < 0 or row >= m or col < 0 or col >= n:
        return False
    if grid[row][col] == "#": return False
    return True
if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 1
    grader.grade(problem_id, test_case_id, play_episode, parse.read_grid_mdp_problem_p1)