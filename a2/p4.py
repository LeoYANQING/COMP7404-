import sys, parse, random, copy, os, time
direction_to_delta = {
    'N': (-1, 0),
    'S': (1, 0),
    'W': (0, -1),
    'E': (0, 1)
}

def get_available_directions(pos, walls, ghosts_pos):
    i, j = pos
    directions = []
    if i-1 >= 0 and not walls[i-1][j] and (i-1, j) not in ghosts_pos.values():
        directions.append('N')
    if i+1 < len(walls) and not walls[i+1][j] and (i+1, j) not in ghosts_pos.values():
        directions.append('S')
    if j-1 >= 0 and not walls[i][j-1] and (i, j-1) not in ghosts_pos.values():
        directions.append('W')
    if j+1 < len(walls[i]) and not walls[i][j+1] and (i, j+1) not in ghosts_pos.values():
        directions.append('E')
    directions.sort()
    return directions

def generate_layout_string(pacman_pos, ghosts_pos, foods, original_layout):
    layout = []
    for i in range(len(original_layout)):
        row = []
        for j in range(len(original_layout[i])):
            if pacman_pos is not None and (i, j) == pacman_pos:
                row.append('P')
            elif (i, j) in ghosts_pos.values():
                for ghost in sorted(ghosts_pos.keys()):
                    if ghosts_pos[ghost] == (i, j):
                        row.append(ghost)
                        break
            elif original_layout[i][j] == '%':
                row.append('%')
            elif (i, j) in foods:
                row.append('.')
            else:
                row.append(' ')
        layout.append(''.join(row))
    return '\n'.join(layout)

def evaluate_move(new_pos, foods, ghosts_pos):
    if not foods:
        return 0  

    min_food_dist = min(abs(new_pos[0]-f[0]) + abs(new_pos[1]-f[1]) for f in foods)

    ghost_dists = [abs(new_pos[0]-g[0]) + abs(new_pos[1]-g[1]) for g in ghosts_pos.values()]
    min_ghost_dist = min(ghost_dists) if ghost_dists else 0
    return -min_food_dist * 2 + min_ghost_dist * 1  

def better_play_multiple_ghosts(problem):
    layout = problem['layout']
    walls = [[cell == '%' for cell in row] for row in layout]
    pacman_pos = None
    ghosts_pos = {}  
    foods = set()
    for i in range(len(layout)):
        for j in range(len(layout[i])):
            cell = layout[i][j]
            if cell == 'P':
                pacman_pos = (i, j)
            elif cell in ['M', 'X', 'Y', 'Z']: 
                ghosts_pos[cell] = (i, j)
            elif cell == '.':
                foods.add((i, j))
    
    score = 0
    solution = []
    solution.append("0")
    solution.append(generate_layout_string(pacman_pos, ghosts_pos, foods, layout))
    step = 1
    winner = 'Ghost'  
    
    while True:
        pacman_dirs = get_available_directions(pacman_pos, walls, ghosts_pos)
        if not pacman_dirs:
            break
        best_score = -float('inf')
        best_dirs = []
        for dir in pacman_dirs:
            di, dj = direction_to_delta[dir]
            new_i = pacman_pos[0] + di
            new_j = pacman_pos[1] + dj
            new_pos = (new_i, new_j)
            current_score = evaluate_move(new_pos, foods, ghosts_pos)
            if current_score > best_score:
                best_score = current_score
                best_dirs = [dir]
            elif current_score == best_score:
                best_dirs.append(dir)
        best_dirs.sort()
        move = best_dirs[0]
        new_pacman = (
            pacman_pos[0] + direction_to_delta[move][0],
            pacman_pos[1] + direction_to_delta[move][1]
        )
        score -= 1
        ate_food = new_pacman in foods
        if ate_food:
            score += 10
            foods.remove(new_pacman)
        if new_pacman in ghosts_pos.values():
            score -= 500
            solution.append(f"{step}: P moving {move}")
            solution.append(generate_layout_string(None, ghosts_pos, foods, layout))
            solution.append(f"score: {score}")
            winner = 'Ghost'
            break
        
        pacman_pos = new_pacman
        if not foods:
            score += 500
            solution.append(f"{step}: P moving {move}")
            solution.append(generate_layout_string(pacman_pos, ghosts_pos, foods, layout))
            solution.append(f"score: {score}")
            winner = 'Pacman'
            break
        solution.append(f"{step}: P moving {move}")
        solution.append(generate_layout_string(pacman_pos, ghosts_pos, foods, layout))
        solution.append(f"score: {score}")
        step += 1
        ghost_collision = False
        for ghost in sorted(ghosts_pos.keys()):
            current_pos = ghosts_pos[ghost]
            ghost_dirs = get_available_directions(current_pos, walls, ghosts_pos)
            if not ghost_dirs:
                solution.append(f"{step}: {ghost} moving")
                solution.append(generate_layout_string(pacman_pos, ghosts_pos, foods, layout))
                solution.append(f"score: {score}")
                step += 1
                continue
            move = random.choice(sorted(ghost_dirs))
            new_ghost = (
                current_pos[0] + direction_to_delta[move][0],
                current_pos[1] + direction_to_delta[move][1]
            )
            if new_ghost == pacman_pos:
                score -= 500
                solution.append(f"{step}: {ghost} moving {move}")
                solution.append(generate_layout_string(None, ghosts_pos, foods, layout))
                solution.append(f"score: {score}")
                winner = 'Ghost'
                ghost_collision = True
                break
            ghosts_pos[ghost] = new_ghost
            solution.append(f"{step}: {ghost} moving {move}")
            solution.append(generate_layout_string(pacman_pos, ghosts_pos, foods, layout))
            solution.append(f"score: {score}")
            step += 1
        
        if ghost_collision:
            break
        if not foods:
            score += 500
            solution.append("WIN: Pacman")
            winner = 'Pacman'
            break
    
    solution = '\n'.join(solution)
    return solution, winner

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])    
    problem_id = 4
    file_name_problem = str(test_case_id)+'.prob' 
    file_name_sol = str(test_case_id)+'.sol'
    path = os.path.join('test_cases','p'+str(problem_id)) 
    problem = parse.read_layout_problem(os.path.join(path,file_name_problem))
    num_trials = int(sys.argv[2])
    verbose = bool(int(sys.argv[3]))
    print('test_case_id:',test_case_id)
    print('num_trials:',num_trials)
    print('verbose:',verbose)
    start = time.time()
    win_count = 0
    for i in range(num_trials):
        solution, winner = better_play_multiple_ghosts(copy.deepcopy(problem))
        if winner == 'Pacman':
            win_count += 1
        if verbose:
            print(solution)
    win_p = win_count/num_trials * 100
    end = time.time()
    print('time: ',end - start)
    print('win %',win_p)