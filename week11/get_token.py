import requests
import json

# 替换成你自己的GitHub用户名和生成的访问令牌
username = 'your_username'
token = 'your_token'

# GitHub API的基本URL
base_url = 'https://api.github.com/'

# 获取关注者列表
def get_followers(username):
    url = base_url + f'users/{username}/followers'
    response = requests.get(url, auth=(username, token))
    followers = response.json()
    return [follower['login'] for follower in followers]

# 获取关注者仓库数据
def get_repositories(username):
    url = base_url + f'users/{username}/repos'
    response = requests.get(url, auth=(username, token))
    repositories = response.json()
    return repositories

# 存储数据到本地文件
def save_to_file(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=2)

if __name__ == '__main__':
    # 获取关注者列表
    followers = get_followers(username)

    # 查询每个关注者的仓库数据并存储
    for follower in followers:
        repositories = get_repositories(follower)
        save_to_file(repositories, f'{follower}_repositories.json')