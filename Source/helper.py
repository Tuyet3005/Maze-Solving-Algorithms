import math
import os
import shutil


def heuristic_1(goal, now):  # khoang cach theo toa do
    return abs(goal.self_node[0] - now.self_node[0]) + abs(goal.self_node[1] - now.self_node[1]) + now.self_cost


def heuristic_2(goal, now):
    return math.dist(now.self_node, goal.self_node) + now.self_cost


def heuristic_3(mat, now, next_node):  # giai thuat bam tuong ben phai
    if now.self_node[0] == next_node.self_node[0]:  # 2 node nam cung hang
        if now.self_node[1] > next_node.self_node[1]:  # now nam ben phai cua next_node
            if mat[next_node.self_node[0] - 1][next_node.self_node[1]].element == 'x':
                return 0 + len(next_node.pre_node)
            elif mat[next_node.self_node[0] - 1][next_node.self_node[1] + 1].element == 'x':
                return 1 + len(next_node.pre_node)
            else:
                return 2 + len(next_node.pre_node)
        else:  # now nam ben trai cua next_node
            if mat[next_node.self_node[0] + 1][next_node.self_node[1]].element == 'x':
                return 0 + len(next_node.pre_node)
            elif mat[next_node.self_node[0] + 1][next_node.self_node[1] - 1].element == 'x':
                return 1 + len(next_node.pre_node)
            else:
                return 2 + len(next_node.pre_node)
    else:  # 2 node nam cung cot
        if now.self_node[0] > next_node.self_node[0]:  # now nam tren next_node
            if mat[next_node.self_node[0]][next_node.self_node[1] - 1].element == 'x':
                return 0 + len(next_node.pre_node)
            elif mat[next_node.self_node[0] - 1][next_node.self_node[1] - 1].element == 'x':
                return 1 + len(next_node.pre_node)
            else:
                return 2 + len(next_node.pre_node)
        else:  # now nam duoi next_node
            if mat[next_node.self_node[0]][next_node.self_node[1] + 1].element == 'x':
                return 0 + len(next_node.pre_node)
            elif mat[next_node.self_node[0] + 1][next_node.self_node[1] + 1].element == 'x':
                return 1 + len(next_node.pre_node)
            else:
                return 2 + len(next_node.pre_node)


def heuristic(goal, now, h_type):
    if h_type == 0:
        return heuristic_1(goal, now)
    return heuristic_2(goal, now)


def create_output_folder():
    shutil.rmtree('output', ignore_errors=True)
    try:
        os.mkdir('output')
        os.mkdir('output/level_1')
        os.mkdir('output/level_2')
        os.mkdir('output/advance')
    except:
        pass
