import sys, parse
import time, os, copy
import random

def expecti_max_multiple_ghosts(problem, k):
    layout = problem['layout']
    seed = problem['seed']
    walls = [[cell == '%' for cell in row] for row in layout]
    ghost_names = sorted([cell for row in layout for cell in row if cell in ['W', 'X', 'Y', 'Z']])
    pacman_pos = next(((i,j) for i, row in enumerate(layout) for j, cell in enumerate(row) if cell == 'P'), None)
    ghost_pos = {cell: (i,j) for i, row in enumerate(layout) for j, cell in enumerate(row) if cell in ghost_names}
    foods = set((i,j) for i, row in enumerate(layout) for j, cell in enumerate(row) if cell == '.')
    state = {
        'pacman': pacman_pos,
        'ghosts': ghost_pos.copy(),
        'foods': foods.copy(),
        'score': 0,
        'turn': 0
    }

    solution = []
    solution.append(f"seed: {seed}")
    solution.append("0")
    solution.append(generate_layout(state, walls))
    step = 1

    while True:
        current_turn = state['turn']
        if current_turn == 0:
            legal_moves = get_legal_moves(state['pacman'], walls, list(state['ghosts'].values()))
            if not legal_moves:
                solution.append("WIN: Ghost")
                return '\n'.join(solution), 'Ghost'
            best_val = -float('inf')
            best_move = 'Stop'
            for move in legal_moves:
                new_state = apply_move(state, walls, 'P', move)
                val = expectimax(new_state, walls, ghost_names, k-1, 1)
                if val > best_val:
                    best_val = val
                    best_move = move
            
            new_state = apply_move(state, walls, 'P', best_move)
            solution.append(f"{step}: P moving {best_move}")
            solution.append(generate_layout(new_state, walls))
            solution.append(f"score: {new_state['score']}")
            state = new_state
            step += 1

            if check_win(state):
                solution.append("WIN: Pacman")
                return '\n'.join(solution), 'Pacman'
            if check_lose(state):
                solution.append("WIN: Ghost")
                return '\n'.join(solution), 'Ghost'
        else:
            ghost_idx = (current_turn - 1) % len(ghost_names)
            current_ghost = ghost_names[ghost_idx]
            current_pos = state['ghosts'].get(current_ghost, (-1,-1))
            other_ghosts = [pos for g, pos in state['ghosts'].items() if g != current_ghost]
            legal_moves = get_legal_moves(current_pos, walls, other_ghosts)
            
            if not legal_moves:
                solution.append(f"{step}: {current_ghost} cannot move")
                solution.append(generate_layout(state, walls))
                solution.append(f"score: {state['score']}")
                step += 1
            else:
                chosen_move = random.choice(legal_moves)
                new_state = apply_move(state, walls, current_ghost, chosen_move)
                solution.append(f"{step}: {current_ghost} moving {chosen_move}")
                solution.append(generate_layout(new_state, walls))
                solution.append(f"score: {new_state['score']}")
                state = new_state
                step += 1

                if check_lose(state):
                    solution.append("WIN: Ghost")
                    return '\n'.join(solution), 'Ghost'
        state['turn'] = (current_turn + 1) % (len(ghost_names) + 1)

def expectimax(state, walls, ghost_order, depth, agent_index):
    if depth == 0 or check_terminal(state):
        return evaluate(state)
    if agent_index == 0:
        max_val = -float('inf')
        legal_moves = get_legal_moves(state['pacman'], walls, list(state['ghosts'].values()))
        for move in legal_moves:
            new_state = apply_move(state, walls, 'P', move)
            val = expectimax(new_state, walls, ghost_order, depth, 1)
            max_val = max(max_val, val)
        return max_val
    else:
        ghost_idx = agent_index - 1
        if ghost_idx >= len(ghost_order):
            return expectimax(state, walls, ghost_order, depth-1, 0)
        
        current_ghost = ghost_order[ghost_idx]
        current_pos = state['ghosts'].get(current_ghost, (-1,-1))
        if current_pos == (-1,-1):
            return expectimax(state, walls, ghost_order, depth, agent_index+1)
        
        other_ghosts = [pos for g, pos in state['ghosts'].items() if g != current_ghost]
        legal_moves = get_legal_moves(current_pos, walls, other_ghosts)
        if not legal_moves:
            return expectimax(state, walls, ghost_order, depth, agent_index+1)
        

        total = 0.0
        prob = 1.0 / len(legal_moves)
        for move in legal_moves:
            new_state = apply_move(state, walls, current_ghost, move)
            val = expectimax(new_state, walls, ghost_order, depth, agent_index+1)
            total += prob * val
        
        return total
def generate_layout(state, walls):
    layout = []
    for i in range(len(walls)):
        row = []
        for j in range(len(walls[i])):
            if walls[i][j]:
                row.append('%')
            else:
                cell = ' '
                for ghost, pos in state['ghosts'].items():
                    if (i,j) == pos:
                        cell = ghost
                        break
                if cell == ' ' and (i,j) == state['pacman']:
                    cell = 'P'
                if cell == ' ' and (i,j) in state['foods']:
                    cell = '.'
                row.append(cell)
        layout.append(''.join(row))
    return '\n'.join(layout)

def apply_move(old_state, walls, agent, move):
    state = copy.deepcopy(old_state)
    delta = {'N': (-1,0), 'S': (1,0), 'W': (0,-1), 'E': (0,1)}.get(move, (0,0))
    
    if agent == 'P':
        new_pos = (state['pacman'][0]+delta[0], state['pacman'][1]+delta[1])
        if 0 <= new_pos[0] < len(walls) and 0 <= new_pos[1] < len(walls[0]) and not walls[new_pos[0]][new_pos[1]]:

            state['pacman'] = new_pos
            state['score'] -= 1
            if new_pos in state['foods']:
                state['foods'].remove(new_pos)
                state['score'] += 10
                if not state['foods']:
                    state['score'] += 500  

            if new_pos in state['ghosts'].values():
                state['score'] -= 500  
    
    else:  
        current_pos = state['ghosts'].get(agent, (-1,-1))
        new_pos = (current_pos[0]+delta[0], current_pos[1]+delta[1])
        other_ghosts = [pos for g, pos in state['ghosts'].items() if g != agent]
        if (0 <= new_pos[0] < len(walls) and 
            0 <= new_pos[1] < len(walls[0]) and 
            not walls[new_pos[0]][new_pos[1]] and
            new_pos not in other_ghosts):
            state['ghosts'][agent] = new_pos
            if state['ghosts'][agent] == state['pacman']:
                state['score'] -= 500  #
                
    return state

def check_win(state):
    return len(state['foods']) == 0

def check_lose(state):
    return state['pacman'] in state['ghosts'].values()

def check_terminal(state):
    return check_win(state) or check_lose(state)

def get_legal_moves(pos, walls, exclude):
    moves = []
    for d, delta in {'N': (-1,0), 'S': (1,0), 'W': (0,-1), 'E': (0,1)}.items():
        new_i = pos[0] + delta[0]
        new_j = pos[1] + delta[1]
        if (0 <= new_i < len(walls) and 
            0 <= new_j < len(walls[0]) and 
            not walls[new_i][new_j] and 
            (new_i, new_j) not in exclude):
            moves.append(d)
    return moves if moves else ['Stop']

def manhattan(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])
def evaluate(state):
    if check_win(state): 
        return 9999 + state['score']
    if check_lose(state): 
        return -9999 + state['score']
    
    score = state['score']
    score -= 20 * len(state['foods']) 
    
    ghost_dists = [manhattan(state['pacman'], g) for g in state['ghosts'].values()]
    min_ghost_dist = max(min(ghost_dists), 1) if ghost_dists else 1
    score += 5 * min_ghost_dist  
    
    if state['foods']:
        food_dists = [manhattan(state['pacman'], f) for f in state['foods']]
        min_food_dist = max(min(food_dists), 1)
        score -= 10 * min_food_dist  
        
    return score
def evaluate(state):
    if check_win(state): 
        return 9999 + state['score']
    if check_lose(state): 
        return -9999 + state['score']
    
    score = state['score']
    score -= 15 * len(state['foods'])
    

    if state['foods']:
        food_dists = [manhattan(state['pacman'], f) for f in state['foods']]
        avg_food_dist = sum(food_dists) / len(food_dists)
        score -= 5 * avg_food_dist
    

    ghost_dists = [manhattan(state['pacman'], g) for g in state['ghosts'].values()]
    if ghost_dists:
        avg_ghost_dist = sum(ghost_dists) / len(ghost_dists)
        score += 3 * avg_ghost_dist
    
    return score

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])    
    problem_id = 6
    file_name_problem = str(test_case_id)+'.prob' 
    file_name_sol = str(test_case_id)+'.sol'
    path = os.path.join('test_cases','p'+str(problem_id)) 
    problem = parse.read_layout_problem(os.path.join(path,file_name_problem))
    k = int(sys.argv[2])
    num_trials = int(sys.argv[3])
    verbose = bool(int(sys.argv[4]))
    print('test_case_id:',test_case_id)
    print('k:',k)
    print('num_trials:',num_trials)
    print('verbose:',verbose)
    start = time.time()
    win_count = 0
    for i in range(num_trials):
        solution, winner = expecti_max_multiple_ghosts(copy.deepcopy(problem), k)
        if winner == 'Pacman':
            win_count += 1
        if verbose:
            print(solution)
    win_p = win_count/num_trials * 100
    end = time.time()
    print('time: ',end - start)
    print('win %',win_p)