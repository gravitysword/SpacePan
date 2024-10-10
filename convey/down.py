from bs4 import BeautifulSoup
import json
import multiprocessing
import requests
import os
import time


def down_img(url, file_path, cookies):
    response = requests.get(url,cookies=cookies)
    with open(file_path, 'wb') as f:
        f.write(response.content)
    print(f"图片已保存为 {file_path}")


def download_images(url,img_dir):
    os.makedirs(img_dir, exist_ok=True)

    with open('../config/config.json', 'r') as f:
        selenium_cookies = json.load(f)['cookies']["download_images"]
        cookies = {cookie['name']: cookie['value'] for cookie in selenium_cookies}


    content = requests.get(url, cookies=cookies).text
    soup = BeautifulSoup(content, 'html.parser')

    img_tags = soup.find_all('div', attrs={"class": "pgc-img"})
    config_url = soup.find_all('p', attrs={"data-track":"1"})

    a1 = "1"*300
    config = config_url[0].text.replace(a1, "")
    print("文件信息",str(config))

    imgs = [ i.find_all('img', )[0].get("src")  for i in img_tags]

    config_path = os.path.join(img_dir, "config.json")
    with open(config_path, 'w') as f:
        f.write(json.dumps(json.loads(config)))

    processes = []
    for j, img_url in enumerate(imgs):
        print(f"正在下载{j+1}图片")
        file_path = os.path.join(img_dir, f"frame_{j:06d}.png").replace("\\", "/")

        p = multiprocessing.Process(target=down_img, args=(img_url, file_path, cookies))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

if __name__ == '__main__':
    a  =time.time()
    #图片要保存的路径
    img_dir = "../res/b"
    #文章链接
    url = "https://www.toutiao.com/article/7424079831064642075/"
    download_images(url,img_dir)
    print(time.time()-a)