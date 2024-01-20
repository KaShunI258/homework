from bs4 import BeautifulSoup
import requests
import pandas as pd
# 先创建好一个表格的框架
team_scores = pd.read_csv('team_scores.csv')
country_name = ['BEL', 'BRA', 'BUL', 'CAN', 'CHN', 'DOM', 'GER', 'ITA', 'JPN',
                'KOR', 'NED', 'POL', 'SRB', 'THA', 'TUR', 'USA']
team_scores_v1_index1 = [item for item in country_name for _ in range(len(country_name))]  # 把这个列表中的元素重复21次
team_scores_v1_columns = ['Total Score', 'Match1', 'Match2', 'Match3', 'Match4', 'Match5']
team_scores_v1_index2 = country_name * len(country_name)
team_scores1 = pd.DataFrame(data=None, columns=[team_scores_v1_columns],
                           index=[team_scores_v1_index1, team_scores_v1_index2])

# 从排球网站中爬取相应数据
second_response = requests.get('https://en.volleyballworld.com/volleyball/competitions/vnl-2022/schedule/')
html_content2 = second_response.text.encode(second_response.encoding).decode()
soup2 = BeautifulSoup(html_content2, 'lxml')

# 获得每场大比赛的信息
# matches = soup2.find_all('a', class_='vbw-mu-finished vbw-mu__data')
finished = soup2.select('div.vbw-mu--match.vbw-mu.vbw-mu-finished')
print(len(finished))
parent_of_matches_women = [element for element in finished
            if 'Women' in element.find('div',class_='vbw-mu__info--details').text]
print(len(parent_of_matches_women))
matches_women = [element.find('a',class_='vbw-mu-finished vbw-mu__data') for element in parent_of_matches_women]
print(len(matches_women))
for match in matches_women:
    # 获得本场比赛的队伍的名称
    home_team_name = match.find_all('div', class_='vbw-mu__team__name vbw-mu__team__name--abbr')[0].text
    away_team_name = match.find_all('div', class_='vbw-mu__team__name vbw-mu__team__name--abbr')[1].text

    # 获得本场比赛的total scores
    match_score = match.find('div', class_='vbw-mu__score').text
    team_scores1.at[(home_team_name, away_team_name), 'Total Score'] = match_score

    # 获得本场比赛的小分
    round_scores = match.find_all('div', class_='vbw-mu__sets--result')
    round_scores_list = [item.text for item in round_scores[0:5]]  # 在item后面加text，而非round_scores！
    team_scores1.loc[
        (home_team_name, away_team_name), ['Match1', 'Match2', 'Match3', 'Match4', 'Match5']] = round_scores_list

team_scores1 = team_scores1.fillna('0:0')  # 使用fillna将NaN值填充为0:0

team_scores1.to_csv('team_scores_22Tfinal.csv')


