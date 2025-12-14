import sys, parse, grader
from heapq import heappush, heappop
import collections

def greedy_search(problem):
    """
    实现 Greedy Search,解决图搜索问题。

    参数:
        problem (dict): 包含图搜索问题的字典。
    
    返回:
        str: 结果字符串，包含探索顺序和解路径。
    """
    # 从问题中提取必要信息
    start_state = problem['start_state']
    goal_states = problem['goal_states']
    edges = problem['edges']
    heuristic = problem['heuristic']  # 启发式函数

    # 构建图的邻接表
    graph = collections.defaultdict(list)
    for edge in edges:
        start, end, cost = edge
        graph[start].append((end, float(cost)))

    # 初始化 Greedy Search 所需的数据结构
    frontier = []  # 优先队列，存储 (启发式值, 节点)
    heappush(frontier, (heuristic[start_state], start_state))  # 初始状态的启发式值
    explored = set()  # 已探索节点
    exploration_order = []  # 记录探索顺序
    parent_map = {start_state: None}  # 记录路径的父节点映射

    while frontier:
        # 从优先队列中取出当前节点
        current_heuristic, current_node = heappop(frontier)

        # 如果当前节点未被探索
        if current_node not in explored:
            # 标记当前节点为已探索
            

            # 检查是否到达目标状态
            if current_node in goal_states:
                # 如果到达目标状态，构建解路径
                solution_path = []
                while current_node:
                    solution_path.append(current_node)
                    current_node = parent_map[current_node]
                solution_path.reverse()
                # 返回探索顺序和解路径
                return f"{' '.join(exploration_order)}\n{' '.join(solution_path)}"
            explored.add(current_node)
            exploration_order.append(current_node)
            # 扩展当前节点的邻居
            if current_node in graph:
                for neighbor, edge_cost in graph[current_node]:
                    if neighbor not in explored:
                        # 使用启发式值作为优先级
                        heappush(frontier, (heuristic[neighbor], neighbor))
                        parent_map[neighbor] = current_node

    # 如果没有找到解，返回空解
    return ""

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 4  # 修改为问题 4
    grader.grade(problem_id, test_case_id, greedy_search, parse.read_graph_search_problem)