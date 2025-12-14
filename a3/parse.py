import os
import sys
def num(s):
    try:
        return float(int(s))
    except ValueError:
        return float(s)
def read_grid_mdp_problem_p1(file_path):
    """解析P1问题的MDP配置"""
    problem = {
        'grid': [],
        'policy': [],
        'noise': 0.1,
        'seed': None,
        'livingReward': 0.0
    }
    
    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    
    current_section = None
    for line in lines:
        if line.startswith('seed:'):
            problem['seed'] = int(line.split(':')[1].strip())
        elif line.startswith('noise:'):
            problem['noise'] = float(line.split(':')[1].strip())
        elif line.startswith('livingReward:'):
            problem['livingReward'] = float(line.split(':')[1].strip())
        elif line == 'grid:':
            current_section = 'grid'
        elif line == 'policy:':
            current_section = 'policy'
        else:
            if current_section == 'grid':
                problem['grid'].append([cell.strip() for cell in line.split()])
            elif current_section == 'policy':
                problem['policy'].append([a.strip().lower() for a in line.split()])
    
    return problem

def read_grid_mdp_problem_p2(file_path):
    problem = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        data = "".join(f.readlines())
    lines = data.split('\n')
    problem['discount'] = num(lines[0].split(":")[1])
    problem['noise'] = num(lines[1].split(':')[1])
    problem['livingReward'] = num(lines[2].split(":")[1])
    problem['iterations'] = num(lines[3].split(":")[1])

    grid_start = lines.index('grid:') + 1
    grid_end = lines.index('policy:') - 1
    problem['grid'] = [line.strip().split() for line in lines[grid_start:grid_end + 1]]

    policy_start = lines.index('policy:') + 1
    problem['policy'] = [line.strip().split() for line in lines[policy_start:]]
    return problem

def read_grid_mdp_problem_p3(file_path):
    """解析P3问题的值迭代配置"""
    problem = {
        'grid': [],
        'discount': 1.0,
        'noise': 0.1,
        'livingReward': -0.1,
        'iterations': 10
    }
    
    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    
    current_section = None
    for line in lines:
        if line.startswith('discount:'):
            problem['discount'] = float(line.split(':')[1].strip())
        elif line.startswith('noise:'):
            problem['noise'] = float(line.split(':')[1].strip())
        elif line.startswith('livingReward:'):
            problem['livingReward'] = float(line.split(':')[1].strip())
        elif line.startswith('iterations:'):
            problem['iterations'] = int(line.split(':')[1].strip())
        elif line == 'grid:':
            current_section = 'grid'
        else:
            if current_section == 'grid':
                problem['grid'].append([cell.strip() for cell in line.split()])
    
    return problem
def read_grid_mdp_problem_p4(file_path):
    problem = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        data = "".join(f.readlines())
    lines = data.split("\n")
    problem['discount'] = num(lines[0].split(":")[1])
    problem['noise']=num(lines[1].split(":")[1])
    problem['livingReward'] = num(lines[2].split(":")[1])
    grid_start_index=lines.index("grid:")+1
    problem['grid']=[line.strip().split() for line in lines[grid_start_index:]]
    return problem
if __name__ == "__main__":
    if len(sys.argv) == 3:
        problem_id, test_case_id = sys.argv[1], sys.argv[2]
        if int(problem_id) == 1:
            problem = read_grid_mdp_problem_p1(os.path.join('test_cases','p'+problem_id, test_case_id+'.prob'))
        elif int(problem_id) == 2:
            problem = read_grid_mdp_problem_p2(os.path.join('test_cases','p'+problem_id, test_case_id+'.prob'))
        elif int(problem_id) == 3:
            problem = read_grid_mdp_problem_p3(os.path.join('test_cases','p'+problem_id, test_case_id+'.prob'))
        print(problem)
    else:
        print('Error: I need exactly 2 arguments!')
    