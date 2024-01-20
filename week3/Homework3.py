# prac1: decimal to binary
# import math
# def DecToBin(x):
#     integerPart = []
#     i = 0
#     while x != 0 and i < 8:
#         bit = math.floor(x * 2)
#         x = x * 2 - bit
#         integerPart.append(bit)
#         i = i + 1
#     print(integerPart)
#
# DecToBin(0.7)

# prac2: create random float numbers
# import random
# x = random.uniform(10, 20)
# print(x)

# prac3: check if the ID is compliant
# def CheckIsRight(number):
#     i = 0
#     while i < len(number):
#         if i<=16:
#             if number[i] < '0' or number[i] > '9':
#                 return False
#         else:#末位检测方法
#             if (number[i] < '0' or number[i] > '9') and number[i] != 'X':
#                 return False
#         i = i + 1
#     if i != 18:
#         return False
#     else:
#         return True
#
# x = input( "please input your ID number:" )
# print(CheckIsRight(x))

# prac4: creating a nodelist
# class node:
#     data = ''
#     next = None
#     def __init__(self, data=None, next=None):
#         self.data = data
#         self.next = next
#     def getD(self):
#         return self.data
#
# def add_tail(prevN, data):
#     node2 = node(data)
#     nodeTemp = prevN
#     while nodeTemp.next != None:
#         nodeTemp = nodeTemp.next
#     nodeTemp.next = node2
#
#
# def delete(node):
#     nodeTemp = node.next
#     nodePrev = node
#     while nodeTemp.next != None:
#         nodePrev = nodeTemp
#         nodeTemp = nodeTemp.next
#     nodePrev.next = None
#
#
# def modify(node, index, data):
#     nodeTemp = node
#     Isfound = False
#     while not Isfound:
#         nodeTemp = nodeTemp.next
#         if nodeTemp.data == index:
#             Isfound = True
#     if not Isfound:
#         return False
#     else:
#         nodeTemp.data = data
#
#
# def search(node, index):
#     nodeTemp = node
#     counter = 0
#     Isfound = False
#     while not Isfound:
#         nodeTemp = nodeTemp.next
#         counter += 1
#         if nodeTemp == None:
#             break # nodeTemp is running the risk of being a None type, so before this unexpected result, break it.
#         if nodeTemp.getD() == index:
#             Isfound = True
#     if not Isfound:
#         return -1
#     else:
#         return counter
#
#
# def getData(headnode):
#     nodeTemp = headnode.next
#     while nodeTemp != None:
#         print(nodeTemp.data)
#         nodeTemp = nodeTemp.next
#     print()
#
# headNode = node(-1)
# add_tail(headNode, 5)
# add_tail(headNode, 10)
# add_tail(headNode, 15)
# add_tail(headNode, 20)
# getData(headNode)
# delete(headNode)
# getData(headNode)
#
# print(search(headNode, 20))
# modify(headNode, 10, 30)
# print(search(headNode,30))
# print()
# getData(headNode)

# prac5: output the even number
# for i in range(101):
#     if i % 2 == 0:
#         print(i)

# prac6: transform the scores to grades
# def trans(scores):
#     if scores < 60:
#         return 'D'
#     elif scores <= 74 and scores >=60:
#         return 'C'
#     elif scores <= 89 and scores >= 75:
#         return 'B'
#     elif scores >=90:
#         return 'A'
#     else:
#         return False
#
# print(trans(83))

# prac7: calculate the greatest common divisor
# def GCD(x1, x2):
#     dividend = max(x1, x2)
#     divisor = min(x1, x2)
#     remainder = dividend % divisor
#     if remainder == 0:
#         return divisor
#     else:
#         return GCD(divisor , remainder)
#
# print(GCD(36, 75))

# prac8: sort random list with selection sort and merge sort
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

# x = [4,6,9,2,5,1]
# x = selctSort(x)
# print(x)
# l1 = []; l2 = []; l3 = []
# createList(l1,l2,l3)
# selctSort(l1)
# mergeSort(l1)

# prac9: create an array  as required
# import random
# list1 = random.sample(range(1, 50), k=5)
# list2 = []
# for i in range(len(list1)):
#     k = 0
#     sum = list1[i]
#     while k < i:
#         sum *= list1[k]
#         k += 1
#     list2.append(sum)
# print(list1)
# print(list2)
