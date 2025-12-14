import os, sys

def read_graph_search_problem(file_path):
    """
    解析图搜索问题的 .prob 文件，并返回一个字典结构表示问题。
    """
    problem = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # 解析起始状态
    problem['start_state'] = lines[0].strip().split(":")[1].strip()

    # 解析目标状态列表
    problem['goal_states'] = lines[1].strip().split(":")[1].strip().split()

    # 初始化存储启发式值的字典
    heuristics = {}
    i = 2  # 启发式值从第3行开始
    while i < len(lines):
        parts = lines[i].strip().split()

        # 边的部分开始时，退出启发式值解析
        if len(parts) == 3 and parts[2].replace('.', '', 1).isdigit():
            break

        # 解析启发式值
        if len(parts) == 2:
            state, heuristic = parts
            heuristics[state] = float(heuristic)
        i += 1

    problem['heuristic'] = heuristics

    # 解析边的集合
    edges = []
    while i < len(lines):
        parts = lines[i].strip().split()
        if len(parts) == 3:  # 每行应该有起点、终点、代价
            start_state, end_state, cost = parts
            edges.append((start_state, end_state, float(cost)))
        i += 1

    problem['edges'] = edges

    return problem

def read_8queens_search_problem(file_path):
    # 初始化一个8x8的棋盘，默认每个位置都是'.'
    problem = [['.' for _ in range(8)] for _ in range(8)]

    # 打开文件并读取内容
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # 解析文件内容到棋盘
    for row in range(8):
        line = lines[row].strip().replace(" ", "")  # 去掉换行符和所有空格
        for col in range(8):
            if line[col] == 'q':
                problem[row][col] = 'q'  # 放置皇后
    return problem

if __name__ == "__main__":
    if len(sys.argv) == 3:
        problem_id, test_case_id = sys.argv[1], sys.argv[2]
        if int(problem_id) <= 5:
            problem = read_graph_search_problem(os.path.join('test_cases','p'+problem_id, test_case_id+'.prob'))
        else:
            problem = read_8queens_search_problem(os.path.join('test_cases','p'+problem_id, test_case_id+'.prob'))
        print(problem)
    else:
        print('Error: I need exactly 2 arguments!')