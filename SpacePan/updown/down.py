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


def download(url,img_dir):
    os.makedirs(img_dir, exist_ok=True)
    content = requests.get(url, cookies=cookies).text
    soup = BeautifulSoup(content, 'html.parser')
    config_url = soup.find_all('p', attrs={"data-track": "1"})
    #文件信息
    config = config_url[0].text.replace("1" * 300, "")
    config = json.loads(config)
    json.dump(config, open(os.path.join(img_dir, "config.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=4)
    storage_url = config["storage"]["url"]
    storage_size = int(config["storage"]["size"])
    with open(join_path(img_dir, "config.png"), 'wb') as f:
        f.write(requests.get(storage_url, cookies=cookies).content)

    urls = cv2.imread(join_path(img_dir, "config.png")).tobytes()[:storage_size].decode("utf-8")
    urls = json.loads(urls)
    st = time.time()
    with ThreadPoolExecutor(max_workers=10) as executor:  # 设置最大线程数为10
        th = []
        for j in urls:
            j = int(j)
            print(f"正在下载第 {j + 1} 张图片")
            file_path = join_path(img_dir, f"frame_{j:06d}.png")
            j = str(j)
            th.append(executor.submit(download_img, urls[j], file_path, cookies))
        for t in th:
            t.result()

    print("下载时间：", time.time() - st)


def img2file(img_dir, file_dir):
    config_path = join_path(img_dir, 'config.json')
    os.makedirs(file_dir, exist_ok=True)

    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.loads(f.read())

    file_path = join_path(file_dir, config["file"]['name']).replace("\\", "/")
    size = int(config["file"]['size'])

    d = 0
    img = [f for f in os.listdir(img_dir) if os.path.splitext(f)[1].lower() in {".png"} and  os.path.splitext(f)[0].lower() not in {"config"} ]
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
    img_dir = r"D:/zzztest/2"
    file_path = r"D:/zzztest/3"
    url = ''
    download(url,img_dir)
    img2file(img_dir, file_path)
    print(time.time() - a)
