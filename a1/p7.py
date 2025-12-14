import sys, parse, grader

def number_of_attacks(problem):
    # 提取所有皇后位置
    queens = set()
    for i in range(8):
        line = problem[i]
        for j in range(8):
            if line[j] == 'q':
                queens.add((i, j))
    
    # 计算总攻击次数
    total_attacks = 0
    for (r, c) in queens:
        attack_count = 0
        # 检查同一行
        for j in range(8):
            if j != c and (r, j) in queens:
                attack_count += 1
        # 检查同一列
        for i in range(8):
            if i != r and (i, c) in queens:
                attack_count += 1
        # 检查对角线
        # 左上到右下
        i, j = r - 1, c - 1
        while i >= 0 and j >= 0:
            if (i, j) in queens:
                attack_count += 1
            i -= 1
            j -= 1
        i, j = r + 1, c + 1
        while i < 8 and j < 8:
            if (i, j) in queens:
                attack_count += 1
            i += 1
            j += 1
        # 右上到左下
        i, j = r - 1, c + 1
        while i >= 0 and j < 8:
            if (i, j) in queens:
                attack_count += 1
            i -= 1
            j += 1
        i, j = r + 1, c - 1
        while i < 8 and j >= 0:
            if (i, j) in queens:
                attack_count += 1
            i += 1
            j -= 1
        total_attacks += attack_count
    # 总攻击次数需除以2避免重复计数
    return total_attacks // 2

def better_board(problem):
    # 提取所有皇后原始位置（每列一个）
    original_queens = {}
    for i in range(8):
        line = problem[i]
        for j in range(8):
            if line[j] == 'q':
                original_queens[j] = i  # 假设输入合法（每列一个皇后）
    
    # 初始化最佳棋盘和最小攻击次数
    best_board = [list(row) for row in problem]
    min_attacks = number_of_attacks(problem)
    
    # 遍历每一列
    for col in range(8):
        # 遍历该列的每一行
        for row in range(8):
            if row == original_queens[col]:
                continue  # 跳过当前皇后所在的行
            # 生成临时棋盘
            temp_board = [list(row) for row in problem]
            # 移动皇后到新位置
            temp_board[original_queens[col]][col] = '.'  # 移除原皇后
            temp_board[row][col] = 'q'  # 放置新皇后
            # 计算攻击次数
            current_attacks = number_of_attacks(temp_board)
            # 如果攻击次数更小，更新最佳棋盘
            if current_attacks < min_attacks:
                min_attacks = current_attacks
                best_board = temp_board
    
    # 将最佳棋盘转换为字符串列表，每行末尾添加换行符
    result = ""
    for row in best_board:
        result += " ".join(row) + "\n"
    return result.strip()  # 去除末尾多余的换行符

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 7
    grader.grade(problem_id, test_case_id, better_board, parse.read_8queens_search_problem)