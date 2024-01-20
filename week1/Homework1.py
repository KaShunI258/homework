# practice 1
# print("Hello,world!")

# practice 2
# star = chr(0x2605)
# print(star,star,star,star,star,star,star,star,star)
# print(star,"Name:junwei He    ",star)
# print(star,"Number:10225501436",star)
# print(star,star,star,star,star,star,star,star,star)

# practice 3
# x = input(); y = input(); z = input()
# num = [x, y, z]
# num.sort()
# print(num)

# practice 4
# w = input(); x = input(); y = input(); z = input()
# num1 = [w, x, y, z]
# num1.sort(reverse=True)
# print(num1)

#practice 5
# i = 1
# while i<=100:
#     if i%2==1:
#         print(i)
#     i = i + 1

#practice 6
# sum = 0
# i=1
# while i<=100:
#     sum = sum + i
#     i = i + 1
# print(sum)

#practice 7
# num2 = [4,5,6,7,8]
# num3 = []; num4 = []
# for i in range(len(num2)):
#     num3.append(num2[len(num2)-i-1])
# print(num3)
# t = 0
# while t <len(num2):
#     num4.append(num2[len(num2)-t-1])
#     t = t + 1
# print(num4)

# practice 8
"""这是在判断有无重复字符"""
# def IsRepeating(strs):
#     existed = [] #已有的字母
#     x = 0
#     for i in strs:
#         thing_index = existed.index(i) if i in existed else -1
#         if thing_index == -1:
#             existed.append(i)
#         else:
#             x = -1
#             break
#     if x == -1:
#         return False
#     return True
# strs2 = "asdidcasd"
# strs3 = "asdfghj"
# print(IsRepeating(strs2))
# print(IsRepeating(strs3))
"""正确解法"""
# def Isrepeating(str):
#     for i in range(len(str)):
#         checking = str[i]
#         if i == len(str)-1:
#             return False
#         if checking == str[i+1]:
#             return True
# strs2 = "assdidcasd"
# strs3 = "asdfghj"
# print(Isrepeating(strs2))
# print(Isrepeating(strs3))

# practice 9
# def DelSpace(str):
#     newstr = []
#     symbol = ''
#     for i in str:
#         if i != ' ':
#             newstr.append(i)
#     newstr1 = symbol.join(newstr)
#     return newstr1
# str1 = "nihao wojiao he junwei"
# print(DelSpace(str1))

# practice 10
"""好像没做对"""
# def Cuberoot(n):
#     l = 0
#     r = 100
#     mid = (l + r) / 2
#     while abs(mid - n) > 1e-6 :
#         if mid * mid * mid > n:
#             r = mid
#         else:
#             l = mid
#         mid = (l + r) / 2
#     return mid
# print(Cuberoot(27))

# practice 11
# def factorial(n):
#     sum = 1
#     i = 1
#     while i <= n:
#         sum = i * sum
#         i = i + 1
#     return sum
# print(factorial(5))