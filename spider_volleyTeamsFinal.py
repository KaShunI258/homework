from bs4 import BeautifulSoup
import re
import time
import pandas as pd
from selenium import webdriver

# 先搭建队伍各项得分情况的DF框架
team_scores = pd.read_csv('team_scores.csv')
Teams_columns1 = ['Attack', 'Attack', 'Attack', 'Attack', 'Block', 'Serve', 'Dig', 'Reception', 'Error', 'Turns']
Teams_columns2 = ['Total', 'OH', 'MB', 'OP', 'Block', 'Serve', 'Dig', 'Reception', 'Error', 'Turns']
# 引入turns的概念，防止每个国家因为打的总场次不同而无法比较，每场比赛都会有进行3-5局，总局数就是turns。最后一局算0.6局。（15/25）
Teams_index = ['BEL', 'BRA', 'RUS', 'CAN', 'CHN', 'DOM', 'GER', 'ITA', 'JPN',
                'KOR', 'NED', 'POL', 'SRB', 'THA', 'TUR', 'USA']
team_scores_v2 = pd.DataFrame(data=None, index=Teams_index, columns=[Teams_columns1, Teams_columns2])
team_scores_v2 = team_scores_v2.fillna(0)


# 获得起始网页的解析，由于这个网站的超链接是动态加载的，request库已经不能满足需求，因此必须使用更高级的selenium
start_url = 'https://en.volleyballworld.com/volleyball/competitions/vnl-2021/schedule/'
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

# 已知所有女排比赛网址
error = []
number_t = 11830  # 每年不一样，要查看网址
i = 78
while i < 124:  # 21年打了124场！
    new_url = 'https://en.volleyballworld.com/volleyball/competitions/vnl-2021/schedule/' + str(number_t+i)  # 构建完整的URL
    driver.get(new_url)

    # 等待新页面加载完成，否则可能无法读取
    time.sleep(5)

    # 获取新页面的源代码
    new_html_content = driver.page_source

    # 使用Beautiful Soup解析新页面的内容
    new_soup = BeautifulSoup(new_html_content, 'lxml')

    # 获得参加比赛的国家
    country_info = new_soup.find('thead', class_='vbw-o-table__header')
    country1 = country_info.find_all('a', class_='vbw-mu__team__name-link')[1].text if not None else 'others'
    country2 = country_info.find_all('a', class_='vbw-mu__team__name-link')[3].text if not None else 'others'
    print(country1,country2)
    if (country2 == 'others' or country1 == 'others'):
        error.append(number_t+i)
        continue
    # 获得轮次数
    turn_info = new_soup.find('div', class_='vbw-mu__score')
    turn_row = turn_info.get_text()  # 或者使用 turn_row = turn_info.text
    turn_numbers = re.findall(r'\d+', turn_row)
    turn_total = int(turn_numbers[0]) + int(turn_numbers[1])  # 转换为整数再相加
    team_scores_v2.loc[country1, ('Turns', 'Turns')] += 4.6 if turn_total == 5 else turn_total
    team_scores_v2.loc[country2, ('Turns', 'Turns')] += 4.6 if turn_total == 5 else turn_total

    # 获得记录比赛信息的元素
    match_info = new_soup.find('tbody', class_='vbw-o-table__body')
    # 检查是否找到符合条件的元素
    if match_info:
        # 获得attack total的信息
        attack_rows = match_info.find_all('tr', class_='vbw-o-table__row attack')
        for row in attack_rows:
            row_text = row.text
            # print(row_text)
            attack_numbers = re.findall(r'\d+', row_text)  # 使用正则表达式获得其中的数字
            numbers = [int(num) for num in attack_numbers]
            team_scores_v2.loc[country1, ('Attack', 'Total')] += numbers[0]
            team_scores_v2.loc[country2, ('Attack', 'Total')] += numbers[1]

        # 获得block的信息
        block_rows = match_info.find_all('tr', class_='vbw-o-table__row block')
        for row in block_rows:
            row_text = row.text
            block_numbers = re.findall(r'\d+', row_text)
            numbers = [int(num) for num in block_numbers]
            team_scores_v2.loc[country1, ('Block', 'Block')] += numbers[0]
            team_scores_v2.loc[country2, ('Block', 'Block')] += numbers[1]

        # 获得serve
        serve_rows = match_info.find_all('tr', class_='vbw-o-table__row serve')
        for row in serve_rows:
            row_text = row.text
            serve_numbers = re.findall(r'\d+', row_text)
            numbers = [int(num) for num in serve_numbers]
            team_scores_v2.loc[country1, ('Serve', 'Serve')] += numbers[0]
            team_scores_v2.loc[country2, ('Serve', 'Serve')] += numbers[1]

        # 获得己方失误（error）数
        error_rows = match_info.find_all('tr', class_='vbw-o-table__row opponent-error')
        for row in error_rows:
            row_text = row.text
            error_numbers = re.findall(r'\d+', row_text)
            numbers = [int(num) for num in error_numbers]
            team_scores_v2.loc[country1, ('Error', 'Error')] += numbers[1]  # 注意顺序调换了
            team_scores_v2.loc[country2, ('Error', 'Error')] += numbers[0]

        # 获得救球（dig）数
        dig_rows = match_info.find_all('tr', class_='vbw-o-table__row dig')
        for row in dig_rows:
            row_text = row.text
            dig_numbers = re.findall(r'\d+', row_text)
            numbers = [int(num) for num in dig_numbers]
            team_scores_v2.loc[country1, ('Dig', 'Dig')] += numbers[0]
            team_scores_v2.loc[country2, ('Dig', 'Dig')] += numbers[1]

        # 获得一传（reception）数
        rec_rows = match_info.find_all('tr', class_='vbw-o-table__row reception')
        for row in rec_rows:
            row_text = row.text
            rec_numbers = re.findall(r'\d+', row_text)
            numbers = [int(num) for num in rec_numbers]
            team_scores_v2.loc[country1, ('Reception', 'Reception')] += numbers[0]
            team_scores_v2.loc[country2, ('Reception', 'Reception')] += numbers[1]
        # 得到运动员的详细信息
        athletes_info = new_soup.find('table',
                                      class_='vbw-o-table vbw-match-player-statistic-table vbw-stats-scoring vbw-set-all')
        # 获得每个位置的成功进攻总量
        each_athlete_info = athletes_info.find_all('tr')
        # print(len(each_athlete_info))
        for athlete in each_athlete_info:
            athlete_pos = athlete.find('td', class_='vbw-o-table__cell position')
            if athlete_pos:
                athlete_pos = athlete_pos.text
                # print(athlete_pos)
                attack_value = float(athlete.find('td', class_='vbw-o-table__cell attacks').text)
                # print(attack_value)
                if athlete_pos == 'OH':
                    current_value = team_scores_v2.loc[country1, ('Attack', 'OH')]
                    current_value = 0 if pd.isna(current_value) else current_value
                    team_scores_v2.loc[country1, ('Attack', 'OH')] = current_value + attack_value
                    # print(team_scores_v2.loc[country1, ('Attack', 'OH')])
                elif athlete_pos == 'O':
                    current_value = team_scores_v2.loc[country1, ('Attack', 'OP')]
                    current_value = 0 if pd.isna(current_value) else current_value
                    team_scores_v2.loc[country1, ('Attack', 'OP')] = current_value + attack_value
                elif athlete_pos == 'MB':
                    current_value = team_scores_v2.loc[country1, ('Attack', 'MB')]
                    current_value = 0 if pd.isna(current_value) else current_value
                    team_scores_v2.loc[country1, ('Attack', 'MB')] = current_value + attack_value
        print(team_scores_v2.loc[country1])

        athletes_info2 = new_soup.find('table',
                                       class_='vbw-o-table vbw-match-player-statistic-table vbw-stats-scoring vbw-set-all hidden')
        # 这是客场国的比分，它的标签后有hidden
        each_athlete_info2 = athletes_info2.find_all('tr')
        # print(len(each_athlete_info))
        for athlete in each_athlete_info2:
            athlete_pos = athlete.find('td', class_='vbw-o-table__cell position')
            if athlete_pos:
                athlete_pos = athlete_pos.text
                # print(athlete_pos)
                attack_value = float(athlete.find('td', class_='vbw-o-table__cell attacks').text)
                print(attack_value)
                if athlete_pos == 'OH':
                    current_value = team_scores_v2.loc[country2, ('Attack', 'OH')]
                    current_value = 0 if pd.isna(current_value) else current_value
                    team_scores_v2.loc[country2, ('Attack', 'OH')] = current_value + attack_value
                    # print(team_scores_v2.loc[country1, ('Attack', 'OH')])
                elif athlete_pos == 'O':
                    current_value = team_scores_v2.loc[country2, ('Attack', 'OP')]
                    current_value = 0 if pd.isna(current_value) else current_value
                    team_scores_v2.loc[country2, ('Attack', 'OP')] = current_value + attack_value
                elif athlete_pos == 'MB':
                    current_value = team_scores_v2.loc[country2, ('Attack', 'MB')]
                    current_value = 0 if pd.isna(current_value) else current_value
                    team_scores_v2.loc[country2, ('Attack', 'MB')] = current_value + attack_value
        print(team_scores_v2.loc[country2])
        # 保存DataFrame到CSV文件
        team_scores_v2.to_csv('team_scores_21v3.csv', mode='w')
    i += 1
print(error)