import sys,random ,grader ,parse
direction_to_delta = {
    'N': (-1, 0),
    'S': (1, 0),
    'W': (0, -1),
    'E': (0, 1)
}

def get_available_directions(pos, walls):
    i, j = pos
    directions = []
    if i-1 >= 0 and not walls[i-1][j]:
        directions.append('N')
    if i+1 < len(walls) and not walls[i+1][j]:
        directions.append('S')
    if j-1 >= 0 and not walls[i][j-1]:
        directions.append('W')
    if j+1 < len(walls[i]) and not walls[i][j+1]:
        directions.append('E')
    directions.sort()
    return directions

def generate_layout_string(pacman_pos, ghost_pos, foods, original_layout):
    layout = []
    for i in range(len(original_layout)):
        row = []
        for j in range(len(original_layout[i])):
            if pacman_pos is not None and (i, j) == pacman_pos:
                row.append('P')
            elif (i, j) == ghost_pos:
                row.append('W')
            else:
                if original_layout[i][j] == '%':
                    row.append('%')
                elif (i, j) in foods:
                    row.append('.')
                else:
                    row.append(' ')
        layout.append(''.join(row))
    return '\n'.join(layout)

def random_play_single_ghost(problem):
   
    seed = problem['seed']
    layout = problem['layout']
    walls = [[cell == '%' for cell in row] for row in layout]
    pacman_pos = None
    ghost_pos = None
    foods = set()
    for i in range(len(layout)):
        for j in range(len(layout[i])):
            cell = layout[i][j]
            if cell == 'P':
                pacman_pos = (i, j)
            elif cell == 'W':
                ghost_pos = (i, j)
            elif cell == '.':
                foods.add((i, j))
    
    random.seed(seed)
    score = 0
    solution = []
    solution.append(f"seed: {seed}")
    solution.append("0")
    solution.append(generate_layout_string(pacman_pos, ghost_pos, foods, layout))
    
    
    step = 1
    while True:
        pacman_dirs = get_available_directions(pacman_pos, walls)
        if not pacman_dirs:
            break  
        pacman_dirs.sort()
        move = random.choice(pacman_dirs)
        new_pacman = (
            pacman_pos[0] + direction_to_delta[move][0],
            pacman_pos[1] + direction_to_delta[move][1]
        )
        score -= 1  
        ate_food = new_pacman in foods
        if ate_food:
            score += 10
            foods.remove(new_pacman)
        if new_pacman == ghost_pos:
            score -= 500
            solution.append(f"{step}: P moving {move}")
            solution.append(generate_layout_string(None, ghost_pos, foods, layout))
            solution.append(f"score: {score}")
            solution.append("WIN: Ghost")
            return '\n'.join(solution)
        pacman_pos = new_pacman

        if not foods:
            score += 500
            solution.append(f"{step}: P moving {move}")
            solution.append(generate_layout_string(pacman_pos, ghost_pos, foods, layout))
            solution.append(f"score: {score}")
            solution.append("WIN: Pacman")
            return '\n'.join(solution)

        solution.append(f"{step}: P moving {move}")
        solution.append(generate_layout_string(pacman_pos, ghost_pos, foods, layout))
        solution.append(f"score: {score}")
        step += 1
        
        ghost_dirs = get_available_directions(ghost_pos, walls)
        if ghost_dirs:
            ghost_dirs.sort()
            move = random.choice(ghost_dirs)
            new_ghost = (
                ghost_pos[0] + direction_to_delta[move][0],
                ghost_pos[1] + direction_to_delta[move][1]
            )
            if new_ghost == pacman_pos:
                score -= 500
                solution.append(f"{step}: W moving {move}")
                solution.append(generate_layout_string(None, new_ghost, foods, layout))
                solution.append(f"score: {score}")
                solution.append("WIN: Ghost")
                return '\n'.join(solution)
            ghost_pos = new_ghost

            solution.append(f"{step}: W moving {move}")
            solution.append(generate_layout_string(pacman_pos, ghost_pos, foods, layout))
            solution.append(f"score: {score}")
            step += 1
            if ghost_pos == pacman_pos:
                score -= 500
                solution.append("WIN: Ghost")
                return '\n'.join(solution)
        if not foods:
            score += 500
            solution.append("WIN: Pacman")
            return '\n'.join(solution)
    
    return '\n'.join(solution)

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 1
    grader.grade(problem_id, test_case_id, random_play_single_ghost, parse.read_layout_problem)