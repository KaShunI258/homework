# you should get the theme,time,and profile of the latest news till today.
from bs4 import BeautifulSoup
import requests
import csv
# send GET requests
response = requests.get("https://news.sina.com.cn/world/")
# get the contents from requests
html_content = response.text.encode(response.encoding).decode()
# # decide the file path and name
# file_path = "./xinlang.html"
# # open the file and write the contents
# with open(file_path,'w',encoding='utf=8') as file:
#     file.write(html_content)

# analyze the HTML with beautifulsoup
soup = BeautifulSoup(html_content, 'lxml')
# find the specific title and so on of the news
items = soup.find_all('div', class_='news-item img-news-item')  # though the origin code has 2 spaces between
# the words, you should space only one
news = []  # 将得到的数据以字典的方式存入列表中
for item in items:
    string = item.h2.a.text.strip()
    time_element = item.find(attrs = {'class':'time'})
    time = time_element.text.strip() if time_element else "N/A"  # 防止没有读出时间而出错！
    news.append({'title' : string,'time' : time})

filename = "news.csv"  # 将数据存入news.csv中
fields = ['title','time']  # 确定表头
with open('data.csv','w',newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fields)
    writer.writeheader()  # 写入表头？
    writer.writerows(news)  # 逐行存入数据集
