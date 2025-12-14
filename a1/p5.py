import sys, parse, grader
from heapq import heappush, heappop
import collections

def a_star_search(problem):
    """
    实现 A* Search，解决图搜索问题。

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

    # 初始化 A* Search 所需的数据结构
    frontier = []  # 优先队列，存储 (f(n), 节点)
    heappush(frontier, (heuristic[start_state], start_state))  # 初始状态的 f(n) = h(n)
    explored = set()  # 已探索节点
    exploration_order = []  # 记录探索顺序
    parent_map = {start_state: None}  # 记录路径的父节点映射
    cost_map = {start_state: 0}  # 记录从起点到每个节点的实际成本 g(n)

    while frontier:
        # 从优先队列中取出当前节点
        current_f, current_node = heappop(frontier)

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
                    # 计算新路径的实际成本 g(n)
                    new_cost = cost_map[current_node] + edge_cost
                    # 如果邻居未被探索，或者找到更低的成本路径
                    if neighbor not in cost_map or new_cost < cost_map[neighbor]:
                        cost_map[neighbor] = new_cost
                        # 计算 f(n) = g(n) + h(n)
                        f_value = new_cost + heuristic[neighbor]
                        # 将新路径加入优先队列
                        heappush(frontier, (f_value, neighbor))
                        parent_map[neighbor] = current_node

    # 如果没有找到解，返回空解
    return ""

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 5  # 修改为问题 5
    grader.grade(problem_id, test_case_id, a_star_search, parse.read_graph_search_problem)