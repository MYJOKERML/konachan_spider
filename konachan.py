# 爬取konachan网站的图片
import os
import requests
import json
import time
from fake_useragent import UserAgent

# 生成随机的User-Agent，模仿人类操作请求
ua = UserAgent()
user_agent = ua.random

headers = {"User-Agent": user_agent}

# print(headers)

# 代理, 视自己使用的软件情况而定
proxies = {
    'http': 'http://127.0.0.1:33210',
    'https': 'http://127.0.0.1:33210',
    'all': 'socks5://127.0.0.1:33211'
}

# 下载图片
# tags = 'rating:safe+order:score'
safe_mode = False # 是否开启安全模式
tags = 'rating:safe' # 防止爬取到R18图片，要添加其他tag请在后面加上+号，例如 'rating:safe+girl'
pages_num = 5 # 爬取的页数

proxies_on = False # 是否开启代理 (如果开启代理，需要在上面设置好代理的端口)
if not proxies_on:
    proxies = None

# 保存路径
if safe_mode:
    if os.name == 'nt':
        save_path = 'D:\\dataset\\konachan\\'
    elif os.name == 'posix':
        save_path = '~/dataset/konachan/'
else:
    if os.name == 'nt':
        save_path = 'D:\\dataset\\konachan\\explicit\\'
    elif os.name == 'posix':
        save_path = '~/dataset/konachan/explicit/'

if not os.path.exists(save_path):
    os.makedirs(save_path)

# 没梯子只能上.net
# print(proxies)
print('Safe mode: ', safe_mode)
print('代理：', proxies_on)
print('保存路径：', save_path)
print('开始爬取...')

for page in range(1, pages_num + 1):
    while True:
        if safe_mode:
            if proxies_on:
                url = 'https://konachan.com/post.json?tags={}&page={}'.format(tags, page)
            else:
                url = 'https://konachan.net/post.json?tags={}&page={}'.format(tags, page)
        else:
            if proxies_on:
                url = 'https://konachan.com/post.json?page={}'.format(page)
            else:
                url = 'https://konachan.net/post.json?page={}'.format(page)
        try:
            post_req = requests.get(url, headers=headers, proxies=proxies)
            post = json.loads(post_req.content)
            # print(post)
            for i in range(len(post)):
                img_url = post[i]['file_url']
                img_name = post[i]['id']
                img_suffix = os.path.splitext(img_url)[1]
                if os.path.exists(save_path + str(img_name) + img_suffix):
                    print('第{}页第{}张图片已存在'.format(page, i + 1))
                    continue
                else:
                    time.sleep(0.1) # 防止爬取过快被封IP
                    img_req = requests.get(img_url, headers=headers, proxies=proxies)
                    img = img_req.content
                    with open(save_path + str(img_name) + img_suffix, 'wb') as f:
                        f.write(img)
                        print('第{}页第{}张图片下载完成'.format(page, i + 1), f'图片id: {img_name}{img_suffix}')

            print('第{}页爬取完成'.format(page))
            break
        except Exception as e:
            print(e)
            # 继续从失败处开始爬取
            print('第{}页爬取失败，正在重新爬取...'.format(page))
            continue
