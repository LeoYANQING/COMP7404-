import sys, grader, parse, random
direction_to_delta = {
    'N': (-1, 0),
    'S': (1, 0),
    'W': (0, -1),
    'E': (0, 1)
}

def get_available_directions(pos, walls, exclude_positions):

    i, j = pos
    directions = []
    # 北
    if i-1 >= 0 and not walls[i-1][j] and (i-1, j) not in exclude_positions:
        directions.append('N')
    # 南
    if i+1 < len(walls) and not walls[i+1][j] and (i+1, j) not in exclude_positions:
        directions.append('S')
    # 西
    if j-1 >= 0 and not walls[i][j-1] and (i, j-1) not in exclude_positions:
        directions.append('W')
    # 东
    if j+1 < len(walls[i]) and not walls[i][j+1] and (i, j+1) not in exclude_positions:
        directions.append('E')
    directions.sort()
    return directions

def generate_layout_string(pacman_pos, ghosts_pos, foods, original_layout):
    layout = []
    for i in range(len(original_layout)):
        row = []
        for j in range(len(original_layout[i])):
            cell = original_layout[i][j]
            ghost_here = False
            for ghost in sorted(ghosts_pos.keys()):
                if ghosts_pos[ghost] == (i, j):
                    row.append(ghost)
                    ghost_here = True
                    break
            if ghost_here:
                continue
            if pacman_pos is not None and (i, j) == pacman_pos:
                row.append('P')
            elif cell == '%':
                row.append('%')
            elif (i, j) in foods:
                row.append('.')
            else:
                row.append(' ')
        layout.append(''.join(row))
    return '\n'.join(layout)

def random_play_multiple_ghosts(problem):
    seed = problem['seed']
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
            elif cell in ['M', 'X', 'Y', 'Z', 'W']: 
                ghosts_pos[cell] = (i, j)
            elif cell == '.':
                foods.add((i, j))
    
    random.seed(seed)
    score = 0
    solution = []
    solution.append(f"seed: {seed}")
    solution.append("0")
    solution.append(generate_layout_string(pacman_pos, ghosts_pos, foods, layout))
    
    step = 1
    while True:
        pacman_dirs = get_available_directions(pacman_pos, walls, [])
        if not pacman_dirs:
            break
        move = random.choice(sorted(pacman_dirs))
        new_pacman = (
            pacman_pos[0] + direction_to_delta[move][0],
            pacman_pos[1] + direction_to_delta[move][1]
        )
        pacman_pos = new_pacman
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
            solution.append("WIN: Ghost")
            return '\n'.join(solution)
        if not foods:
            score += 500
            solution.append(f"{step}: P moving {move}")
            solution.append(generate_layout_string(pacman_pos, ghosts_pos, foods, layout))
            solution.append(f"score: {score}")
            solution.append("WIN: Pacman")
            return '\n'.join(solution)
        solution.append(f"{step}: P moving {move}")
        solution.append(generate_layout_string(pacman_pos, ghosts_pos, foods, layout))
        solution.append(f"score: {score}")
        step += 1
        for ghost in sorted(ghosts_pos.keys()):
            current_pos = ghosts_pos[ghost]
            other_ghosts_pos = [pos for g, pos in ghosts_pos.items() if g != ghost]
            ghost_dirs = get_available_directions(current_pos, walls, other_ghosts_pos)
            if not ghost_dirs:
                solution.append(f"{step}: {ghost} moving ")
                solution.append(generate_layout_string(pacman_pos, ghosts_pos, foods, layout))
                solution.append(f"score: {score}")
                step += 1
                continue
            move = random.choice(sorted(ghost_dirs))
            new_pos = (
                current_pos[0] + direction_to_delta[move][0],
                current_pos[1] + direction_to_delta[move][1]
            )
            if new_pos == pacman_pos:
                score -= 500
                ghosts_pos[ghost] = new_pos
                solution.append(f"{step}: {ghost} moving {move}")
                solution.append(generate_layout_string(None, ghosts_pos, foods, layout))
                solution.append(f"score: {score}")
                solution.append("WIN: Ghost")
                return '\n'.join(solution)
            ghosts_pos[ghost] = new_pos
            solution.append(f"{step}: {ghost} moving {move}")
            solution.append(generate_layout_string(pacman_pos, ghosts_pos, foods, layout))
            solution.append(f"score: {score}")
            step += 1
        if not foods:
            solution.append("WIN: Pacman")
            break
    
    return '\n'.join(solution)

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 3
    grader.grade(problem_id, test_case_id, random_play_multiple_ghosts, parse.read_layout_problem)