from bs4 import BeautifulSoup
import requests, cv2, os, time, json
import numpy as np

with open('../config/config.json', 'r') as f:
    config = json.loads(f.read())
    play_cookies = config["cookies"]["main"]
    cookies = {cookie['name']: cookie['value'] for cookie in play_cookies}


def down_img(url):
    a = requests.get(url, cookies=cookies).content
    RGB_data = np.frombuffer(a, np.uint8)
    data = cv2.imdecode(RGB_data, cv2.IMREAD_UNCHANGED).tobytes()
    return data


def download(url, file_dir):
    #初始化
    st = time.time()
    os.makedirs(file_dir, exist_ok=True)
    content = requests.get(url, cookies=cookies).text
    soup = BeautifulSoup(content, 'html.parser')
    config_url = soup.find_all('p', attrs={"data-track": "1"})

    #文件信息
    config = json.loads(config_url[0].text.replace("1" * 300, ""))
    file_size, file_name = int(config["file"]["size"]), config["file"]["name"]
    storage_url,storage_size = config["storage"]["url"], int(config["storage"]["size"])
    storage_png = requests.get(storage_url, cookies=cookies).content
    image_array = np.frombuffer(storage_png, np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_UNCHANGED)

    storage = json.loads(image.tobytes()[:storage_size].decode("utf-8"))

    with open(os.path.join(file_dir, file_name), 'wb') as f:
        d = 0
        for j in storage:
            print(f"正在下载第 {int(j) + 1} 张图片")
            url = storage[j]
            data_ps = down_img(url)
            if d + len(data_ps) >= file_size:
                a = data_ps[0:(file_size - d)]
                f.write(a)
                break
            else:
                f.write(data_ps)
            d += len(data_ps)

    print("总计时间：", time.time() - st)




if __name__ == '__main__':
    file_path = f"D:/zzztest/{time.time()}"
    url = 'https://www.toutiao.com/article/7441807664071311926/?log_from=19432a7cffeeb_1732681213061'
    download(url, file_path)
