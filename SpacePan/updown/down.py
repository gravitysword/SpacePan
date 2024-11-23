from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import requests, cv2, os, time, json
from utile.u import *

with open('../config/config.json', 'r') as f:
    config = json.loads(f.read())
    play_cookies = config["cookies"]["upload"]
    cookies = {cookie['name']: cookie['value'] for cookie in play_cookies}


def download_img(url, file_path, cookies):
    response = requests.get(url, cookies=cookies)
    with open(file_path, 'wb') as f:
        f.write(response.content)
    print(f"图片已保存为 {file_path}")

def download(url, img_dir):
    os.makedirs(img_dir, exist_ok=True)
    content = requests.get(url, cookies=cookies).text
    soup = BeautifulSoup(content, 'html.parser')
    img_tags = soup.find_all('div', attrs={"class": "pgc-img"})
    config_url = soup.find_all('p', attrs={"data-track": "1"})
    #文件信息
    config = config_url[0].text.replace("1" * 300, "")
    print("文件信息", str(config))

    imgs = [i.find_all('img')[0].get("src") for i in img_tags]

    config_path = os.path.join(img_dir, "config.json")
    with open(config_path, 'w') as f:
        f.write(json.dumps(json.loads(config)))

    st = time.time()
    with ThreadPoolExecutor(max_workers=10) as executor:  # 设置最大线程数为10
        th = []
        for j, img_url in enumerate(imgs):
            print(f"正在下载第 {j + 1} 张图片")
            file_path = os.path.join(img_dir, f"frame_{j:06d}.png")
            th.append(executor.submit(download_img, img_url, file_path, cookies))
        for t in th:
            t.result()

    print("下载时间：", time.time() - st)


def img2file(img_dir, file_dir):
    config_path = join_path(img_dir, 'config.json')
    os.makedirs(file_dir, exist_ok=True)

    with open(config_path, 'r') as f:
        config = json.loads(f.read())

    file_path = join_path(file_dir, config['name']).replace("\\", "/")
    size = int(config['size'])

    d = 0
    img = [f for f in os.listdir(img_dir) if os.path.splitext(f)[1].lower() in {".png"}]
    img_len = len(img)
    with open(file_path, 'wb') as f:
        for i, img_name in enumerate(img):
            print(f"正在写入第 {i + 1} 张图片")
            img_path = join_path(img_dir, img_name)
            print(img_path)
            RGB_data = cv2.imread(img_path).tobytes()

            if i == img_len - 1:
                f.write(RGB_data[:size - d])
            else:
                f.write(RGB_data)
                d += len(RGB_data)
    print(file_path, "写入成功")


if __name__ == '__main__':
    a = time.time()
    img_dir = r"../res/temp/1"
    file_path = r"../res/temp/2"
    url = 'https://www.toutiao.com/article/7440027264546275881/'
    #download(url, img_dir)
    img2file(img_dir, file_path)
    print(time.time() - a)
