import sys, grader, parse
import collections

def bfs_search(problem):
    """
    广度优先搜索 (BFS) 实现，解决图搜索问题。

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

    # 初始化 BFS 所需的数据结构
    frontier = collections.deque([start_state])  # 队列，用双端队列模拟
    explored = set()                            # 已探索节点
    exploration_order = []                      # 记录探索顺序
    parent_map = {start_state: None}            # 记录路径的父节点映射

    while frontier:
        # 从队列中取出当前节点
        current = frontier.popleft()

        # 如果当前节点未被探索
        if current not in explored:
            # 标记当前节点为已探索
            

            # 检查是否到达目标状态
            if current in goal_states:
                # 如果到达目标状态，构建解路径
                solution_path = []
                while current:
                    solution_path.append(current)
                    current = parent_map[current]
                solution_path.reverse()
                # 返回探索顺序和解路径
                return f"{' '.join(exploration_order)}\n{' '.join(solution_path)}"
            explored.add(current)
            exploration_order.append(current)
            # 将邻居按原始顺序加入队列中
            if current in graph:
                for neighbor in graph[current]:  # 按原始顺序加入队列
                    if neighbor not in explored and neighbor not in parent_map:
                        frontier.append(neighbor)
                        parent_map[neighbor] = current

    # 如果没有找到解，返回空解
    return ""

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 2  # 修改为问题 2
    grader.grade(problem_id, test_case_id, bfs_search, parse.read_graph_search_problem)