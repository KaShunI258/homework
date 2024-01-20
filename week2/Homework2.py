# prac 1
# n = int(input())
# i = 1
# while i <= n/2:
#     max = 0
#     result = i*(n-i)
#     if max < result:
#         max = result
#         mul1 = i
#     i = i + 1
# print(result, mul1, n-mul1)
""" 
assume a number i=1,then restrict i in range from 1 to n/2.
compute the result respectively, noting the maximum.
"""

# prac 2
# a = 2**10
# b = 2**20
# c = 2**30
# d = 2**40
# e = 2**50
# print(a);print(b);print(c);print(d);print(e)

# prac 3
# suppose vector x = [man, wolf, sheep, grass]

# prac 4
# l = 1
# r = int(input())
# mid = (r + l) / 2
# while abs(r-l) >= 0.001:
#     if mid * mid < 2:
#         l = mid
#     else:
#         r = mid
#     mid = (r + l) / 2
# print(mid)

# prac 5 6
# def newton_sqrt(c):
#     g = c/2
#     while abs(g*g - c) > 0.0000001:
#         g = (g + c/g) / 2
#     return g
#
# def newton_sqrt2(c):
#     g = c/4
#     while abs(g*g - c) > 0.0000001:
#         g = (g + c/g) / 2
#     return g
#
# x = int(input())
# res1 = newton_sqrt(x)
# res2 = newton_sqrt2(x)
# print(res1)
# print(res2)

"""6.没有影响"""

# prac 7
# def newton_cube(c):
#     g = c/3
#     while abs(g*g*g - c) > 0.0000001:
#         g = (2*g + c/(g*g)) / 3
#     return g
#
# x = int(input())
# res = newton_cube(x)
# print(res)
"""公式最初计算错了"""

# prac 8
# import math
# #Newton formula calculate pai
# def doubFactorial(n):
#     sum = 1
#     s = 1 if n%2 == 1 else 2
#     for i in range(s,n+1,2):
#         sum *= i
#     return sum
#
# def Newton(x):
#     sum = 0
#     for i in range(x):
#         expr1 = doubFactorial(2*i + 1)
#         expr2 = doubFactorial(2*i) * math.pow(2*i + 1,2) * pow(2,2*i + 1)
#         sum += expr1 / expr2
#     return sum
#
#
# for i in range(3,10):
#     res = Newton(i) * 6
#     print("%-20d%-20.12f" % (i,res))
# print()
#
# # incise circles
# n = 6
# a = 1
# print("%-20d%-20.12f" % (n, n*a/2))
# for i in range(14):
#   n = 2 * n
#   a = math.sqrt(2-2*math.sqrt(1-(a/2)**2))
#   print("%-20d%-20.12f" % (n, n*a/2))
# print()
#
# # Machin formula
# def Machin(n):
#     sum1 = 0
#     sum2 = 0
#     for i in range(n):
#         sum1 += math.pow(-1, i) * 1/((2*i+1) * pow(5, 2*i+1))
#     for j in range(n):
#         sum2 += math.pow(-1, j) * 1/((2*j+1) * pow(239, 2*j+1))
#     sum = 16*sum1 - 4*sum2
#     return sum
#
# for i in range(0,10):
#     res = Machin(i)
#     print("%-20d%-20.12f" % (i,res))

# prac 9: Monte carmello method
# import math
# import random
# def function(x):
#     return x*x + 4*x*math.sin(x)
#
# def monte(n):
#     for i in range(n):
#         sum = 0
#         x = random.randrange(2,3)
#         sum += function(x)
#     return sum/n
#
# print(monte(10))
