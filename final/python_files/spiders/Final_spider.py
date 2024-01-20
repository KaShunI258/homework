import os
from bs4 import BeautifulSoup
import time
import pandas as pd
from selenium import webdriver
import re

"""
本次的任务是把主要参赛国的每场比赛原始表格全部爬取，并按照csv文件保存。注意，在爬取完表格后，应该按比赛
把表格分类，即标注表格的主场国和客场国，这在最后五行实现。
"""
# 这是三年来的比赛原链接
start_url23 = 'https://en.volleyballworld.com/volleyball/competitions/vnl-2023/schedule/'
start_url22 = 'https://en.volleyballworld.com/volleyball/competitions/vnl-2022/schedule/'
start_url21 = 'https://en.volleyballworld.com/volleyball/competitions/vnl-2021/schedule/'
years = 2023
start_url = start_url23
"""接下来，按照女排比赛顺序，依次爬取表格内容。
补充：2023年女排比赛序号：16024 - 16127
     2022年女排比赛序号：13754 - 13857
     2021年女排比赛序号：11830 - 11953"""
begin_num = 16024
end_num = 16127


# 这是通过网站的cookie验证，从而获得更多信息
driver = webdriver.Chrome()  # 请确保你的ChromeDriver已经安装并在PATH中
driver.get(start_url)
driver.implicitly_wait(10)
driver.delete_all_cookies()  # 固定搭配暂不知道具体原因
cookies = [{'domain': '.volleyballworld.com', 'expiry': 1705370977, 'httpOnly': False, 'name': '_hjIncludedInSessionSample_1859763', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '0'},
 {'domain': '.volleyballworld.com', 'expiry': 1705371008, 'httpOnly': False, 'name': '_hjSession_1859763', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'eyJpZCI6ImJiY2EwMDZhLTVmMDEtNGUzNi04NjFmLWNiOTQ1ZWZhNDU1NyIsImMiOjE3MDUzNjkxNzc4OTcsInMiOjAsInIiOjAsInNiIjoxLCJzciI6MCwic2UiOjAsImZzIjoxLCJzcCI6MX0='},
 {'domain': '.volleyballworld.com', 'expiry': 1736905177, 'httpOnly': False, 'name': '_hjSessionUser_1859763', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'eyJpZCI6IjVhOTU5YjI0LTUyNTctNWIyMy05ZmJjLTM2OGRlYjU4MGFhMyIsImNyZWF0ZWQiOjE3MDUzNjkxNzc4OTYsImV4aXN0aW5nIjpmYWxzZX0='},
 {'domain': '.volleyballworld.com', 'expiry': 1739237978, 'httpOnly': False, 'name': '__qca', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'P0-1930540427-1705369177238'},
 {'domain': '.volleyballworld.com', 'expiry': 1705455576, 'httpOnly': False, 'name': '_gid', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'GA1.2.1968396925.1705369177'},
 {'domain': '.volleyballworld.com', 'expiry': 1739929176, 'httpOnly': False, 'name': '_ga_R215V1S3VM', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'GS1.1.1705369176.1.1.1705369176.60.0.0'},
 {'domain': '.volleyballworld.com', 'expiry': 1739929176, 'httpOnly': False, 'name': '_ga_0XQMFZ8Y93', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'GS1.2.1705369176.1.1.1705369176.0.0.0'},
 {'domain': '.volleyballworld.com', 'expiry': 1739929176, 'httpOnly': False, 'name': '_ga', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'GA1.2.2082547222.1705369177'},
 {'domain': '.volleyballworld.com', 'expiry': 1705369236, 'httpOnly': False, 'name': '_gat_UA-185656906-1', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '1'},
 {'domain': '.volleyballworld.com', 'expiry': 1739929176, 'httpOnly': False, 'name': '_ga_5ZY57D5RSS', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'GS1.1.1705369176.1.0.1705369176.60.0.0'},
 {'domain': '.en.volleyballworld.com', 'expiry': 1736991576, 'httpOnly': False, 'name': '_vwo_uuid_v2', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'D72DEF0D3CC158B21EE65E432171BA7A3|4d10c619ffe29b8993620be3fe219b07'},
 {'domain': '.volleyballworld.com', 'expiry': 1713145177, 'httpOnly': False, 'name': '_gcl_au', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '1.1.350320605.1705369177'}]

for cookie in cookies:
    if 'expiry' in cookie:  # 有的cookie里面有这个参数，有的没有。有的话，需要做处理。
        del cookie['expiry']   # 这个expiry参数值得类型会影响到登录识别，所以需要删掉或者更改值为整形
    driver.add_cookie(cookie)
driver.refresh()   # 刷新页面

"""接下来，按照女排比赛顺序，依次爬取表格内容。
补充：2023年女排比赛序号：16024 - 16127
     2022年女排比赛序号：13754 - 13857
     2021年女排比赛序号：11830 - 11953"""



# 这是三年都参加比赛的队伍
Main_Country = ['BRA', 'CAN', 'CHN', 'DOM', 'GER', 'ITA', 'JPN',
                 'KOR', 'NED', 'POL', 'SRB', 'THA', 'TUR', 'USA']

# 7种DF具有的列，对不同的表格而言表头也不同
DF_columns1 = ['Player No', 'Player Name', 'Position', 'Total ABS', 'Attack Points',
              'Block Points', 'Serve Points', 'Errors',' Efficiency %',
               'Country','type','num_set','this_turn_score','num_race', 'win_or_lose']

DF_columns2 = ['Player No','Player Name','Position','Point','Errors',
               'Attempts','Total','Efficiency %',
               'Country','type','num_set','this_turn_score','num_race', 'win_or_lose']

DF_columns3 = ['Player No',	'Player Name','Position','Point','Errors',
               'Touches','Total','Efficiency %',
               'Country','type','num_set','this_turn_score','num_race', 'win_or_lose']

DF_columns4 = ['Player No','Player Name','Position','Point','Errors',
               'Attempts','Total','Efficiency %',
               'Country','type','num_set','this_turn_score','num_race', 'win_or_lose']

DF_columns5 = ['Player No','Player Name','Position','Successful','Errors',
               'Attempts','Total','Efficiency %',
               'Country','type','num_set','this_turn_score','num_race', 'win_or_lose']

DF_columns6 = ['Player No','Player Name','Position','Digs','Errors',
               'Total','Efficiency %',
               'Country','type','num_set','this_turn_score','num_race', 'win_or_lose']

DF_columns7 = ['Player No','Player Name','Position','Point','Errors',
               'Attempts','Total','Efficiency %',
               'Country','type','num_set','this_turn_score','num_race', 'win_or_lose']
# 这是表数据的种类
types = ['SCORING', 'ATTACK', 'BLOCK', 'SERVE', 'RECEPTION', 'DIG', 'SET']

# 这是在表后新增的6列
Meta_columns = ['Country', 'type', 'num_set', 'this_turn_score', 'num_race', 'win_or_lose']

first_save = 7
# 最外层每次循环都会打开一个新的网页
for i in range(begin_num,end_num):
    new_url = start_url + str(i)  # 每一次比赛的网址
    driver.get(new_url)
    # 等待新页面加载完成，否则可能无法读取
    time.sleep(3)
    # 获取新页面的源代码
    new_html_content = driver.page_source
    # 使用Beautiful Soup解析新页面的内容
    soup = BeautifulSoup(new_html_content, 'lxml')
    #得到所有tabs
    tabs = soup.find_all('tbody',class_='vbw-o-table__body')
    # 每个tabs数量的情况是固定的，即57（3set），71，85（5set），这就为我们提供了分类的便利。
    # (1：homelen)是主场国家的表格

    Length = len(tabs)
    HomeLen = int((Length + 1) / 2)
    # 爬取国家名称

    Homecountry = soup.find_all('div','vbw-mu__team__name vbw-mu__team__name--abbr')[0].text
    Awaycountry = soup.find_all('div','vbw-mu__team__name vbw-mu__team__name--abbr')[1].text

    # 不是主要国家，直接不爬取！
    if Homecountry not in Main_Country or Awaycountry not in Main_Country:
        continue

    # 用于得到每场比赛的小比分
    scores = [element.text for element in soup.find_all('div','vbw-mu__sets--result')]
    # 这里的每次循环相当于读取一张表。7种表按次序循环出现。
    # 每个表循环set+1次，然后从主场国家进入客场国家。
    for j in range(1,HomeLen):
        nums = (j - 1) % 7
        if nums == 0:
            DF_columns = DF_columns1
        elif nums == 1:
            DF_columns = DF_columns2
        elif nums == 2:
            DF_columns = DF_columns3
        elif nums == 3:
            DF_columns = DF_columns4
        elif nums == 4:
            DF_columns = DF_columns5
        elif nums == 5:
            DF_columns = DF_columns6
        elif nums == 6:
            DF_columns = DF_columns7
        df = pd.DataFrame(columns=DF_columns)

        # 标记了Meta数据
        type_name = types[(j - 1) % 7]
        number_set = int((j - 1) / 7 + 1) - 1

        # 本轮得分有问题！数据的格式可能是x-xx或者xx-x，因此，必须使用其他方式读取分数

        """
['25-21', '25-22', '20-25', '25-22', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-']
"""
        if number_set == 0:
            This_turn_score = 0
            WinOrLose = None
        else:
        # 使用正则表达式提取数字
            # sco_numbers = re.findall(r'\d+', scores[number_set - 1])  # 现在每组scores的数字都存在一个数组中
            sco_numbers = [int(num) for num in re.findall(r'\d+', scores[number_set - 1])]
            This_turn_score = sco_numbers[0]
            WinOrLose = 1 if sco_numbers[0] > sco_numbers[1] else 0

        trs = tabs[j].find_all('tr')
        len1 = len(trs)
        for p in range(len1):
            tds = trs[p].find_all('td')
            len2 = len(tds)

            # 确保DataFrame有足够的行
            if len(df) <= p:
                df.loc[p] = [None] * len(df.columns)

            # 把meta数据存入每一行种，尽管信息冗余，但是有助于减轻合并csv的压力
            df.loc[p, Meta_columns[0]] = Homecountry
            df.loc[p, Meta_columns[1]] = type_name
            df.loc[p, Meta_columns[2]] = number_set
            df.loc[p, Meta_columns[3]] = This_turn_score
            df.loc[p, Meta_columns[4]] = i
            df.loc[p, Meta_columns[5]] = WinOrLose

            for q in range(len2):
                # 使用.loc为DataFrame分配值
                df.loc[p, DF_columns[q]] = tds[q].text

        # 保存文件的路径！
        exam = os.path.join('New_data', f'Final_{type_name}_{years}.csv')
        # 后续文件不需要表头了
        if first_save > 0:
            df.to_csv(exam, mode='a')
            first_save -= 1
        else:
            df.to_csv(exam, mode='a', header=False)

    for j in range(HomeLen, Length):
        nums = (j - HomeLen) % 7
        if nums == 0:
            DF_columns = DF_columns1
        elif nums == 1:
            DF_columns = DF_columns2
        elif nums == 2:
            DF_columns = DF_columns3
        elif nums == 3:
            DF_columns = DF_columns4
        elif nums == 4:
            DF_columns = DF_columns5
        elif nums == 5:
            DF_columns = DF_columns6
        elif nums == 6:
            DF_columns = DF_columns7

        df = pd.DataFrame(columns=DF_columns)

        type_name = types[(j - HomeLen) % 7]
        number_set = int((j - HomeLen)/7 + 1) - 1
        # This_turn_score = scores[number_set - 1][3:5] if number_set != 0 else 0

        if number_set == 0:
            This_turn_score = 0
            WinOrLose = None
        else:
        # 使用正则表达式提取数字
            # sco_numbers = re.findall(r'\d+', scores[number_set - 1])  # 现在每组scores的数字都存在一个数组中
            sco_numbers = [int(num) for num in re.findall(r'\d+', scores[number_set - 1])]
            This_turn_score = sco_numbers[1]
            WinOrLose = 1 if sco_numbers[1] > sco_numbers[0] else 0

        trs = tabs[j].find_all('tr')
        len1 = len(trs)

        for p in range(len1):
            tds = trs[p].find_all('td')
            len2 = len(tds)

            df.loc[p, Meta_columns[0]] = Awaycountry
            df.loc[p, Meta_columns[1]] = type_name
            df.loc[p, Meta_columns[2]] = number_set
            df.loc[p, Meta_columns[3]] = This_turn_score
            df.loc[p, Meta_columns[4]] = i
            df.loc[p, Meta_columns[5]] = WinOrLose

            # 确保DataFrame有足够的行
            if len(df) <= p:
                df.loc[p] = [None] * len(df.columns)

            for q in range(len2):
                # 使用.loc为DataFrame分配值
                df.loc[p, DF_columns[q]] = tds[q].text

        exam = os.path.join('New_data', f'Final_{type_name}_{years}.csv')

        df.to_csv(exam, mode='a', header=False)