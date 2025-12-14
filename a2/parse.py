import os, sys
def read_layout_problem(file_path):
    # 读取文件所有行，并去除行尾的换行符
    with open(file_path, 'r') as f:
        lines = [line.rstrip('\n') for line in f]
    
    # 提取随机种子
    seed_line = lines[0].strip()
    seed = int(seed_line.split(': ')[1])
    
    # 解析布局部分，过滤空行
    layout = []
    for line in lines[1:]:
        stripped_line = line.strip()
        if stripped_line:  # 忽略空行
            layout.append(list(line))  # 直接转换为字符列表
    
    # 返回包含种子和布局的字典
    problem = {
        'seed': seed,
        'layout': layout
    }
    return problem

if __name__ == "__main__":
    if len(sys.argv) == 3:
        problem_id, test_case_id = sys.argv[1], sys.argv[2]
        problem = read_layout_problem(os.path.join('test_cases','p'+problem_id, test_case_id+'.prob'))
        print(problem)
    else:
        print('Error: I need exactly 2 arguments!')