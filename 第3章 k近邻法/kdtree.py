'''
2020-8-18
Yanjie Ze
'''

import numpy as np
import operator
import math
from math import sqrt
from collections import namedtuple

# kd tree的节点类
class kdnode(object):
    def __init__(self, data, split, left, right):
        self.data = data
        self.split = split # 对哪个维度进行分割
        self.left = left
        self.right = right


# 功能函数，计算两点间的Lp distance,默认p=2
def lpdistance(x1, x2, p=2.0):
    sum = 0.0
    for i in range(len(x1)):
        sum += math.pow((x1[i]-x2[i]), p)
    result = sum**(1.0/p)
    return result


class kdtree(object):
    def __init__(self, dataset):
        dimension = len(dataset[0]) # data的维度
        # print(dimension)
        def createNode(split, data):
            if not data:
                return None

            data.sort(key=operator.itemgetter(split))
            splitPosition = len(data)//2
            median = data[splitPosition]

            splitNext = (split + 1) % dimension

            return kdnode(
                data=median,
                split=split,
                left=createNode(split=splitNext, data=data[:splitPosition]),
                right=createNode(split=splitNext, data=data[splitPosition+1:])
            )

        self.root = createNode(split=0, data=dataset)

    def get_root(self):
        return self.root

    # 前序遍历
    def preOrder(self):
        def preOrder(root):
            print(root.data)
            if root.left:
                preOrder(root.left)
            if root.right:
                preOrder(root.right)

        preOrder(self.root)


    # 中序遍历
    def midOrder(self):
        def midOrder(root):
            if root.left:
                midOrder(root.left)
            print(root.data)
            if root.right:
                midOrder(root.right)
        midOrder(self.root)

    # 后序遍历
    def backOrder(self):
        def backOrder(root):
            if root.left:
                backOrder(root.left)
            if root.right:
                backOrder(root.right)
            print(root.data)
        backOrder(self.root)

result = namedtuple("Result_tuple",
                    "nearest_point  nearest_dist  nodes_visited")

def find_nearest(tree, point):
    k = len(point)

    def travel(kd_node, target, max_dist):
        if kd_node is None:
            return result([0] * k, float("inf"),0)  # python中用float("inf")和float("-inf")表示正负无穷

        nodes_visited = 1

        s = kd_node.split  # 进行分割的维度
        pivot = kd_node.dom_elt  # 进行分割的“轴”

        if target[s] <= pivot[s]:  # 如果目标点第s维小于分割轴的对应值(目标离左子树更近)
            nearer_node = kd_node.left  # 下一个访问节点为左子树根节点
            further_node = kd_node.right  # 同时记录下右子树
        else:  # 目标离右子树更近
            nearer_node = kd_node.right  # 下一个访问节点为右子树根节点
            further_node = kd_node.left

        temp1 = travel(nearer_node, target, max_dist)  # 进行遍历找到包含目标点的区域

        nearest = temp1.nearest_point  # 以此叶结点作为“当前最近点”
        dist = temp1.nearest_dist  # 更新最近距离

        nodes_visited += temp1.nodes_visited

        if dist < max_dist:
            max_dist = dist  # 最近点将在以目标点为球心，max_dist为半径的超球体内

        temp_dist = abs(pivot[s] - target[s])  # 第s维上目标点与分割超平面的距离
        if max_dist < temp_dist:  # 判断超球体是否与超平面相交
            return result(nearest, dist, nodes_visited)  # 不相交则可以直接返回，不用继续判断

        # ----------------------------------------------------------------------
        # 计算目标点与分割点的欧氏距离
        temp_dist = sqrt(sum((p1 - p2) ** 2 for p1, p2 in zip(pivot, target)))

        if temp_dist < dist:  # 如果“更近”
            nearest = pivot  # 更新最近点
            dist = temp_dist  # 更新最近距离
            max_dist = dist  # 更新超球体半径

        # 检查另一个子结点对应的区域是否有更近的点
        temp2 = travel(further_node, target, max_dist)

        nodes_visited += temp2.nodes_visited
        if temp2.nearest_dist < dist:  # 如果另一个子结点内存在更近距离
            nearest = temp2.nearest_point  # 更新最近点
            dist = temp2.nearest_dist  # 更新最近距离

        return result(nearest, dist, nodes_visited)

    return travel(tree.root, point, float("inf"))  # 从根节点开始递归



if __name__ == '__main__':
    # print(lpdistance([2,2],[1,1],2))
    dataset = [[2,3],[5,4],[9,6],[4,7],[8,1],[7,2]]
    tree = kdtree(dataset=dataset)
    print("前序遍历：")
    tree.preOrder()
    print("中序遍历：")
    tree.midOrder()
    print("后序遍历：")
    tree.backOrder()

