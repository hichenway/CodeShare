# Author：hichenway
# 功能：计算三维空间异面直线的距离和垂足
# Corresponding Blog: https://blog.csdn.net/songyunli1111

# 参考1：https://www.jianshu.com/p/34a7c4e1f3f5
# 参考2：https://www.cnblogs.com/mazhenyu/p/7154449.html
import math
import numpy as np
def distace(point1, point2):
    num = sum([(point1[i]-point2[i])**2 for i in range(len(point1))])
    return math.sqrt(num)

def distace_3d(p1, p2, q1, q2):
    # 叉乘方法计算三维直线距离

    # p1,p2为L1上的两个节点，q1,q2为L2上的两个节点
    v1 = np.array([p2[i] - p1[i] for i in range(len(p1))])
    v2 = np.array([q2[i] - q1[i] for i in range(len(q1))])

    # 叉乘公式：(a1,a2,a3) X (b1,b2,b3)=(a2b3-a3b2,a3b1-a1b3,a1b2-a2b1)
    chacheng = np.array([v1[1]*v2[2]-v1[2]*v2[1],v1[2]*v2[0]-v1[0]*v2[2],v1[0]*v2[1]-v1[1]*v2[0]])
    temp = np.array([p1[i] - q1[i] for i in range(len(p1))])
    dis_res = abs(sum(chacheng*temp)) / math.sqrt(sum([chacheng[i]**2 for i in range(len(chacheng))]))
    return dis_res

def cross(p1, p2, q1, q2):
    v1 = np.array([p2[i] - p1[i] for i in range(len(p1))])
    v2 = np.array([q2[i] - q1[i] for i in range(len(q1))])
    # l1 = p1 + t1 * v1
    # l2 = q1 + t2 * v2
    a = sum(v1*v2)
    b = sum(v1*v1)
    c = sum(v2*v2)
    d = sum(np.array([q1[i] - p1[i] for i in range(len(p1))])*v1)
    e = sum(np.array([q1[i] - p1[i] for i in range(len(p1))])*v2)
    isParallel = False
    if a==0:        # 对应两直线垂直
        t1 = d/b
        t2 = -e/c
    elif abs(a*a - b*c) > 0.001:     # 普通情况，这里因为浮点数的原因不要用等于0
        t1 = (a * e - c * d) / (a * a - b * c)
        t2 = b * t1 / a - d / a
    else:   # 两直线平行，垂足有无数对，通过在任一一条直线上随便指定一个点，另一条直线上的垂足也就随之确定
        isParallel = True
        t1 = 0
        t2 = - d / a

    point1 = [p1[i] + t1 * v1[i] for i in range(len(p1)) ]
    point2 = [q1[i] + t2 * v2[i] for i in range(len(q1)) ]
    dis = distace(point1, point2)

    return point1, point2, dis, isParallel

if __name__ == "__main__":
    p1 = (2,0,0)
    p2 = (0,2,0)
    q1 = (2,0,2)
    q2 = (0,2,2)
    res = distace_3d(p1, p2, q1, q2)
    point1, point2, dis, isParallel = cross(p1, p2, q1, q2)
    print(dis, res)