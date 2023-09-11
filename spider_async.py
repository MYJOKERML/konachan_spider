import os
import json
import asyncio
import aiohttp
import time
from fake_useragent import UserAgent

ua = UserAgent()
user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"

headers = {"User-Agent": user_agent}

# 代理, 视自己使用的软件情况而定
proxies = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890',
    'all': 'socks5://127.0.0.1:7890'
}

# 下载图片
# tags = 'rating:safe+order:score'
safe_mode = True # 是否开启安全模式
# tags = 'rating:safe' # 防止爬取到R18图片，要添加其他tag请在后面加上+号，例如 'rating:safe+girl'
tag = ''
tags = f"rating:safe+{tag}" if safe_mode else f"{tag}"
pages_num = 10 # 爬取的页数，默认10页，每页21张图片

proxies_on = False # 是否开启代理 (如果开启代理，需要在上面设置好代理的端口)
if not proxies_on:
    proxies = None

date = time.strftime('%Y-%m-%d', time.localtime(time.time()))

# 保存路径
if safe_mode:
    if os.name == 'nt':
        save_path = f'D:\\dataset\\konachan\\{date}\\'
    elif os.name == 'posix':
        save_path = f'./dataset/konachan/{date}/'
else:
    if os.name == 'nt':
        save_path = f'D:\\dataset\\konachan\\explicit\\{date}\\'
    elif os.name == 'posix':
        save_path = f'./dataset/konachan/explicit/{date}/'
        
if tag != '':
    save_path = os.path.join(save_path, tag + '\\')

if not os.path.exists(save_path):
    os.makedirs(save_path)

# 没梯子只能上.net
# print(proxies)
print('Safe mode: ', safe_mode)
print('代理：', proxies_on)
print('保存路径：', save_path)
print('开始爬取...')


async def fetch_page(session, page):
    if safe_mode:
        if proxies_on:
            url = 'https://konachan.com/post.json?tags={}&page={}'.format(tags, page)
        else:
            url = 'https://konachan.net/post.json?tags={}&page={}'.format(tags, page)
    else:
        if proxies_on:
            url = 'https://konachan.com/post.json?page={}'.format(page)
            if tag != '':
                url = 'https://konachan.com/post.json?tags={}&page={}'.format(tag, page)
        else:
            url = 'https://konachan.net/post.json?page={}'.format(page)
            if tag != '':
                url = 'https://konachan.net/post.json?tags={}&page={}'.format(tag, page)
    # try_times = 0
    while True:
        try:
            async with session.get(url, headers=headers, proxy=proxies.get('http', None) if proxies_on else None) as response:
                return await response.json()
        except Exception as e:
            print(f'Error fetching page {page}: {str(e)}')
            # time.sleep(0.1)
            # try_times += 1
            # if try_times >= 100:
            #     return []

async def download_image(session, img_url, img_name, img_suffix):
    while True:
        try:
            async with session.get(img_url, headers=headers, proxy=proxies.get('http', None) if proxies_on else None) as response:
                if response.status == 200:
                    img_data = await response.read()
                    img_path = os.path.join(save_path, f'{img_name}{img_suffix}')
                    if not os.path.exists(img_path):
                        with open(img_path, 'wb') as f:
                            f.write(img_data)
                        print(f'Downloaded {img_path}')
                        break
                else:
                    print(f'Error downloading image {img_url}')
                    # time.sleep(0.1)
        except Exception as e:
            print(f'Error downloading image {img_name}: {str(e)}')
            # time.sleep(0.1)

async def crawl_page(session, page):
    post = await fetch_page(session, page)
    if not post:
        return

    print(f'Crawling page {page}')
    tasks = []

    for i, item in enumerate(post):
        img_url = item['file_url']
        img_name = item['id']
        img_suffix = os.path.splitext(img_url)[1]
        img_path = os.path.join(save_path, f'{img_name}{img_suffix}')

        if not os.path.exists(img_path):
            tasks.append(download_image(session, img_url, img_name, img_suffix))
        else:
            print(f'Image {img_path} already exists')

    await asyncio.gather(*tasks)

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [crawl_page(session, page) for page in range(1, pages_num + 1)]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
