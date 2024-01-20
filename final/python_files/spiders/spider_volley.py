from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd

first_response = requests.get("https://en.volleyballworld.com/volleyball/competitions/vnl-2023/teams/women/")
html_content = first_response.text.encode(first_response.encoding).decode()  # get the code of the current page
soup = BeautifulSoup(html_content, 'lxml')  # analyse the code with soup

# 获得所有女排队伍名称 并把他们应用于DataFrame的表头中
team_names = []
items = soup.find_all('div', class_ = 'vbw-mu__team__name vbw-mu__team__name--abbr')
for item in items:
    item = item.text
    team_names.append(item)

# 获得每一场大比赛的分数，并且得到每一局的小分（暂未实现）

second_response = requests.get('https://en.volleyballworld.com/volleyball/competitions/vnl-2023/schedule/')
html_content2 = second_response.text.encode(first_response.encoding).decode()
soup2 = BeautifulSoup(html_content2, 'lxml')

team_scores = pd.DataFrame(data = None, columns= team_names, index= team_names)
matches = soup2.find_all('a',class_='vbw-mu-finished vbw-mu__data')
for match in matches:
    # 获得本场比赛的队伍的名称
    home_team_name = match.find_all('div',class_ = 'vbw-mu__team__name vbw-mu__team__name--abbr')[0].text
    away_team_name = match.find_all('div',class_ = 'vbw-mu__team__name vbw-mu__team__name--abbr')[1].text
    match_score = match.find('div',class_ = 'vbw-mu__score').text
    team_scores.at[home_team_name, away_team_name] = match_score  # 注意，这里不能直接用homename和awayname作为索引！！

team_scores = team_scores.fillna('0:0')  # 使用fillna将NaN值填充为0:0
team_scores.to_csv('team_scores_modified.csv',index=team_names)  # 将修改后的DataFrame保存回CSV文件

"""
大致效果：
     BRA  BUL  CAN  CHN  CRO  DOM  GER  ...  TUR  USA  IRI  ARG  CUB  FRA  SLO
BRA  NaN  3:0  2:3  1:3  NaN  3:1  3:1  ...  0:3  0:3  NaN  NaN  2:3  3:1  3:1
BUL  NaN  NaN  0:3  1:3  NaN  2:3  NaN  ...  NaN  NaN  3:2  NaN  2:3  NaN  NaN
"""

