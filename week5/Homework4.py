# prac 1: if is prime number
# import math
# def isPrimeNumber(n):
#     i = 2
#     if n == 1:
#         return False
#     while i <= math.sqrt(n):
#         if n % i == 0:
#             return False
#         i += 1
#     return True
#
# print(isPrimeNumber(91))

# prac 2: get the running time of the code
# import time
# time_start = time.time()
# # function()   执行的程序
# import random
# def createList(l1,l2,l3):
#     l1 = random.sample(range(1,999),k = 100)
#     l2 = random.sample(range(1,9999),k = 1000)
#     l3 = random.sample(range(1,99999),k = 10000)
#     return l1,l2,l3
#
# def selctSort(l):
#     for i in range(len(l)):
#         k = i
#         min = l[i]
#         j = i + 1
#         while j < len(l):
#             if l[j] < min:
#                 min = l[j]
#                 k = j
#             j += 1
#         temp = l[i]
#         l[i] = l[k]
#         l[k] = temp
#     return l
#
# def merge(l1,l2):
#     i = 0
#     j = 0
#     l3 = []
#     while i < len(l1) and j < len(l2):
#         if l1[i] < l2[j]:
#             l3.append(l1[i])
#             i += 1
#         else:
#             l3.append(l2[j])
#             j += 1
#     if i == len(l1):
#         l3.extend(l2[j:len(l2)])
#     else:
#         l3.extend(l1[i:len(l1)])
#     return l3
# def mergeSort(l):
#     if len(l) == 1:
#         return l
#     else:
#         l1 = l[0:int(len(l)/2)]
#         l2 = l[int(len(l)/2):len(l)]
#         l1 = mergeSort(l1)
#         l2 = mergeSort(l2)
#         lAns = merge(l1, l2)
#         return lAns
#
# x = [4,6,9,2,5,1]
# x = selctSort(x)
# print(x)
# l1 = []; l2 = []; l3 = []
# createList(l1,l2,l3)
# selctSort(l1)
#
# time_end = time.time()
# time_sum = time_end - time_start
# print('the time is : %fs' %time_sum)

# prac 3: the code of straight insertion sort
# import random
# def createList():
#     return random.sample(range(1, 99), k=10)
#
# def rightShift(l,i,j):
#     while i > j:
#         l[i] = l[i-1]
#         i -= 1
#
# def straightInsert(sequence):
#     i = 1
#     while i < len(sequence):
#         temp = sequence[i]
#         j = i - 1
#         while j >= 0:
#             if temp < sequence[j] and (temp >= sequence[j-1] if j>0 else 1) :
#                 rightShift(sequence, i, j)
#                 sequence[j] = temp
#                 break
#             j -= 1
#         i += 1
#
# list1 = createList()
# print(list1)
# straightInsert(list1)
# print(list1)

# prac 4: O(n^2) O(n)

