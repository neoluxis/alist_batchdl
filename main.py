import requests as rqs
import os
from tqdm import rich
import time

# 目标网站 URL
base_url = "https://pan.uvooc.com"
path = ''

def f_url(path): # fetch url
    return f"{base_url}/api/fs/list?path={path}"

def d_url(path, fn, file_sign): # download url
    return f"{base_url}/d/{path}/{fn}/?sign={file_sign}"

def download(path, show, data=None):
    # print(f"Download {path = }, {show = }")
    os.makedirs(path[1:], exist_ok=True)
    for s in show:
        if s[0] != '+':
            continue
        durl = d_url(path[1:], s[3], s[4])
        print("Downloading: ", durl, " ==> ", f"{path[1:]}/{s[3]}")
        data = rqs.get(durl)
        if not data.status_code == 200:
            print(f'Download failed: {data.status_code}')
            continue
        with open(f"{path[1:]}/{s[3]}", 'wb') as f:
            f.write(data.content)
        time.sleep(0.1)


# 伪造请求头，模拟 Chrome 浏览器
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
}

fil = None

while True:
    # 发送 GET 请求
    response = rqs.get(f_url(path), headers=headers)

    # 输出返回的内容
    resp = response.json()

    if not resp['code'] == 200:
        raise Exception(f"Code = {resp['code']}")

    data = resp['data']['content']

    show = []
    for i, p in enumerate(data):
        if p['is_dir']:
            show.append(['X', i, 'd', p['name'], p['sign']])
        else:
            show.append(['-', i, 'f', p['name'], p['sign']])
    print('List (N)')
    print('---------')
    for s in show:
        print(f"{s[0]} {s[1]}. {s[2]} {s[3]}")
    print('---------')
    user = input("Select: ")
    if user == 'q':
        print("End")
        break
    else:
        user = int(user)
        if show[user][2] == 'd':
            path = f"{path}/{show[user][3]}"
        else:
            while user != 'd':
                if user == 'q': break
                elif user == 'a':
                    for s in show:
                        if s[2] == 'f':
                            s[0] = '+'
                    print('List (FD)')
                    print('---------')
                    for s in show:
                        print(f"{s[0]} {s[1]}. {s[2]} {s[3]}")
                    print('---------')
                elif show[int(user)][2] == 'f':
                    show[int(user)][0] = '+'
                    print('List (FD)')
                    print('---------')
                    for s in show:
                        print(f"{s[0]} {s[1]}. {s[2]} {s[3]}")
                    print('---------')
                user = input("Select F: ")
            download(path, show)

