import sys, parse, grader

def number_of_attacks(problem):
    # 提取所有皇后原始位置（每列一个）
    original_queens = {}
    for i in range(8):
        line = problem[i]
        for j in range(8):
            if line[j] == 'q':
                original_queens[j] = i  # 假设输入合法（每列一个皇后）
    
    # 初始化攻击次数网格
    attack_grid = [[0] * 8 for _ in range(8)]
    
    # 遍历每一列，计算该列皇后移动到各行的总攻击次数
    for col in range(8):
        for row in range(8):
            # 生成临时皇后集合
            temp_queens = []
            for c in range(8):
                if c == col:
                    temp_queens.append((row, c))
                else:
                    temp_queens.append((original_queens[c], c))
            queens = set(temp_queens)
            
            # 计算总攻击次数
            total_attacks = 0
            queen_attacks = {}
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
                queen_attacks[(r, c)] = attack_count
            total_attacks = sum(queen_attacks.values()) // 2
            attack_grid[row][col] = total_attacks
    
    # 格式化输出，每行开头有一个空格，数字右对齐占2位，用单个空格分隔
    result = []
    for row in attack_grid:
        formatted_row = " ".join(f"{num:2}" for num in row)
        result.append(formatted_row)
    return "\n".join(result)

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 6
    grader.grade(problem_id, test_case_id, number_of_attacks, parse.read_8queens_search_problem)