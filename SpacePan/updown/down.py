from bs4 import BeautifulSoup
import requests, cv2, os, time, json
import numpy as np
import threading
import concurrent.futures

with open('../config/config.json', 'r') as f:
    config = json.loads(f.read())
    play_cookies = config["cookies"]["main"]
    cookies = {cookie['name']: cookie['value'] for cookie in play_cookies}



def down_img(url, j, f, isEnd=False, file_size=0):
    a = requests.get(url, cookies=cookies).content
    RGB_data = np.frombuffer(a, np.uint8)
    data = cv2.imdecode(RGB_data, cv2.IMREAD_UNCHANGED).tobytes()
    cap = len(data)

    if isEnd:
        remaining = file_size % cap
        data = data[0:remaining]
    f.seek(j * cap)
    f.write(data)
    print(f"finished_{j}")
    return


def download(url, file_dir):
    #初始化

    os.makedirs(file_dir, exist_ok=True)
    content = requests.get(url, cookies=cookies).text
    soup = BeautifulSoup(content, 'html.parser')
    config_url = soup.find_all('p', attrs={"data-track": "1"})

    #文件信息
    config = json.loads(config_url[0].text.replace("1" * 300, ""))
    file_size, file_name = int(config["file"]["size"]), config["file"]["name"]
    storage_url, storage_size = config["storage"]["url"], int(config["storage"]["size"])
    storage_png = requests.get(storage_url, cookies=cookies).content
    image_array = np.frombuffer(storage_png, np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_UNCHANGED)

    storage = json.loads(image.tobytes()[:storage_size].decode("utf-8"))
    print(f"文件大小：{file_size}，文件名：{file_name}，分块数量：{len(storage)}")
    st = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        with open(os.path.join(file_dir, file_name), 'wb') as f:
            f.seek(file_size - 1)
            f.write(b"0")
            for j in range(len(storage)):
                if j == len(storage) - 1:
                    futures.append(executor.submit(down_img, storage[str(j)], j, f, True, file_size))
                else:
                    futures.append(executor.submit(down_img, storage[str(j)], j, f))

            concurrent.futures.wait(futures)

    print("总计时间：", time.time() - st)


if __name__ == '__main__':
    file_path = f"D:/zzztest/{time.time()}"
    url = 'https://www.toutiao.com/article/7442176220483879435/?log_from=295107ab6f76f_1732766718122'
    download(url, file_path)
