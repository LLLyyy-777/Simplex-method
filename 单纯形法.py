# -*- coding: utf-8 -*-
# @File    : 单纯形法.py
# @Time    : 2021/3/27
# @Author  : laipinyan


# 输入
def input_():
    print('请输入目标函数：')
    objective = input()
    print('请输入约束条件：')
    restrictions = input()
    return objective, restrictions


# 获取系数
def get_nub(str_):
    lis = [[], []]  # [系数, b]
    num = 0
    symbol = 0  # 大小号
    sign = 0  # 正负号
    index = 0
    n = 0
    N = len(str_)
    for i in str_:
        n += 1
        if i.isdigit():
            num = 10 * num + int(i)
            if n == N and index == 1:
                if sign == 0:
                    lis[index].append(num)
                else:
                    lis[index].append(num * sign)
        elif i == 'x':
            if sign == 0:
                lis[index].append(num)
            else:
                lis[index].append(num * sign)
        elif i == '+':
            num = 0
            sign = 0
        elif i == '-':
            num = 0
            sign = -1
        elif i == '<' or i == '>' or i == '=':
            num = 0
            sign = 0
            symbol = i
            index = 1
    return lis, symbol


# 获取目标函数系数
def get_c(objective):
    lis_obj = objective.split(' ')
    lis_c, _ = get_nub(lis_obj[1])[0]
    if lis_obj[0] == 'min':
        lis_c = [i*-1 for i in lis_c]
    return lis_c


# 获取约束条件系数
def get_s(restrictions):
    lis_st = restrictions.split(' ')
    lis_A = []
    lis_b = []
    lis_sym = []
    for i in lis_st:
        x, sym = get_nub(i)
        lis_A.append(x[0])
        lis_b.append(x[1][0])
        lis_sym.append(sym)
    for j in range(len(lis_sym)):
        if lis_sym[j] == '>':
            lis_A[j] = [i*-1 for i in lis_A[j]]
            lis_b[j] = lis_b[j]*-1
    return lis_A, lis_b, lis_sym


# 标准化
def standardization(A, c, sym, M):
    m = len(sym)
    for i in range(m):
        slack = [0] * m
        if sym[i] == '=':
            slack[i] = 1
            A[i] += slack
            c.append(-M)
        else:
            slack[i] = 1
            A[i] += slack
            c.append(0)
    return A, c


# 递归
def iteration(A, b, c, M):
    m = len(b)  # 约束数
    n = len(c)  # 变量数
    if -M in c:  # 大M法
        for i in range(m):
            c = [c[j]+M*A[i][j] for j in range(n)]
    c_in = c.index(max(c))
    b_a = []  # b/a
    for i in range(m):
        b_a.append(b[i] / A[i][c_in])
    in_ = b_a.index(min(b_a))
    divisor = A[in_][c_in]
    A[in_] = [x/divisor for x in A[in_]]
    b[in_] = b[in_]/divisor
    for i in range(m):
        if i == in_:
            continue
        div = A[i][c_in]
        A[i] = [A[i][j]-div*A[in_][j] for j in range(n)]
        b[i] = b[i]-div*b[in_]
    div = c[c_in]
    c = [c[j]-div*A[in_][j] for j in range(n)]
    if max(c) <= 0:
        return A, b, c
    else:
        return iteration(A, b, c, M)


def main():
    obj, st = input_()
    lis_obj = obj.split(' ')
    c = get_c(obj)
    A, b, sym = get_s(st)
    obj_x = c
    M = 10000
    A, c = standardization(A, c, sym, M)
    A, b, c = iteration(A, b, c, M)
    value = 0
    for i in range(len(A)):
        index = A[i].index(1)
        value += b[i]*obj_x[index]
        print('x{}={}'.format(index+1, round(b[i], 2)))
    if lis_obj[0] == 'min':
        print('目标函数最小值：', -1*value)
    else:
        print('目标函数最大值：', value)


if __name__ == '__main__':
    main()
