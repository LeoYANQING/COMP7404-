import sys, grader, parse
import collections

def dfs_search(problem):
    """
    深度优先搜索 (DFS) 实现，解决图搜索问题。

    参数:
        problem (dict): 包含图搜索问题的字典。
    
    返回:
        str: 结果字符串，包含探索顺序和解路径。
    """
    # 从问题中提取必要信息
    start_state = problem['start_state']
    goal_states = problem['goal_states']
    edges = problem['edges']

    # 构建图的邻接表
    graph = collections.defaultdict(list)
    for edge in edges:
        start, end, _ = edge
        graph[start].append(end)

    # 初始化 DFS 所需的数据结构
    frontier = collections.deque([start_state])  # 栈，用双端队列模拟
    explored = set()                            # 已探索节点
    exploration_order = []                      # 记录探索顺序
    parent_map = {start_state: None}            # 记录路径的父节点映射

    while frontier:
        # 从栈中取出当前节点
        current = frontier.pop()

        # 如果当前节点未被探索
        if current not in explored:
            # 检查是否到达目标状态
            if current in goal_states:
                # 如果到达目标状态，构建解路径
                solution_path = []
                while current:
                    solution_path.append(current)
                    current = parent_map[current]
                solution_path.reverse()
                # 返回探索顺序（不包含目标状态）和解路径
                return f"{' '.join(exploration_order)}\n{' '.join(solution_path)}"

            # 标记当前节点为已探索
            explored.add(current)
            exploration_order.append(current)

            # 将邻居按原始顺序加入栈中（不逆序）
            if current in graph:
                for neighbor in graph[current]:  # 不逆序，保持原始顺序
                    if neighbor not in explored:
                        frontier.append(neighbor)
                        parent_map[neighbor] = current

    # 如果没有找到解，返回空解
    return ""

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 1
    grader.grade(problem_id, test_case_id, dfs_search, parse.read_graph_search_problem)