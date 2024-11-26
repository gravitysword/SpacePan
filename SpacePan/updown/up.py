from multiprocessing import Manager
import requests
from playwright.sync_api import sync_playwright
import os, math, time
import numpy as np
import cv2, json
from utile.u import *
from multiprocessing import Pool, cpu_count

with open('../config/config.json', 'r',encoding='utf-8') as f:
    config = json.loads(f.read())
    play_cookies = config["cookies"]["upload"]
    cookies = {cookie['name']: cookie['value'] for cookie in play_cookies}

def up_img(img_path=None,img_data=None):


    if img_data:
        url = "https://mp.toutiao.com/spice/image?upload_source=20020002&aid=1231&device_platform=web"
        a = requests.post(url=url, files={'image': img_data}, cookies=cookies)
    else:
        url = "https://mp.toutiao.com/spice/image?upload_source=20020002&aid=1231&device_platform=web"
        a = requests.post(url=url, files={'image': open(img_path, 'rb')}, cookies=cookies)
    return a.json()["data"]["image_url"]


def save_img(image_path, RGB_data):
    cv2.imwrite(image_path, RGB_data)

def upload(img_dir, pan_path):
    a = time.time()

    storage = {}

    imgs = [join_path(os.path.abspath(img_dir), img_name) for img_name in os.listdir(img_dir) if
            os.path.splitext(img_name)[1].lower() in {".png"} and os.path.splitext(img_name)[0].lower() not in {"config"} ]

    for j, img_path in enumerate(imgs):
        storage[str(j)] = up_img(img_path=img_path)
        print(f"第{j + 1}张图片上传完成")

    stroage = bytearray(json.dumps(storage),encoding='utf-8')
    storage_size = len(stroage)

    stroage = stroage + b'0' * (2000 * 2000 * 3 - len(stroage))
    RGB_data = np.frombuffer(stroage, dtype=np.uint8).reshape(2000, 2000, 3)
    img_data = cv2.imencode('.png', RGB_data)[1].tobytes()
    storage_url = up_img(img_data=img_data)

    with open(join_path(img_dir, "config.json"), 'r',encoding='utf-8') as f:
        config = json.loads(f.read())

    config["storage"] = {
        "url": storage_url,
        "size": str(storage_size)
    }
    print(config)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://mp.toutiao.com/profile_v4/graphic/publish?from=toutiao_pc&is_new_connect=0&is_new_user=0")
        context.add_cookies(play_cookies)
        page.set_viewport_size({"width": 1500, "height": 800})
        time.sleep(1)
        #标题与正文
        file_name = config["file"]["name"]
        img_config = str(config).replace("'", '"')
        title = page.wait_for_selector('//textarea[@placeholder="请输入文章标题（2～30个字）"]')
        title.fill("Pan: " + join_path(pan_path, file_name))
        text = page.locator('//div[@class="ProseMirror"]/p')
        text.fill(img_config + "1" * 300)

        page.wait_for_selector(
            '#root > div > div.left-column > div > div.publish-editor > div.syl-editor-wrap > div > div.ProseMirror')
        #封面
        page.evaluate("window.scrollTo(0, 150000);")

        button_fengmian = page.locator('//span[text()="无封面"]')
        button_fengmian.click()

        # 提交
        page.wait_for_selector(
            '#root > div > div.left-column > div > div.publish-editor > div.syl-editor-wrap > div > div.ProseMirror')

        publish = page.wait_for_selector(
            '//button[@class="byte-btn byte-btn-primary byte-btn-size-large byte-btn-shape-square publish-btn publish-btn-last"]')
        publish.click()
        publish = page.wait_for_selector(
            '//button[@class="byte-btn byte-btn-primary byte-btn-size-large byte-btn-shape-square publish-btn publish-btn-last"]')
        publish.click()

        publish = page.wait_for_selector(
            '//button[@class="byte-btn byte-btn-primary byte-btn-size-large byte-btn-shape-square publish-btn publish-btn-last"]')

        print(f"f发布时间", time.time() - a)
        print(f"上传完成")




def file2img(file_path, img_dir, img_size):
    a = time.time()
    os.makedirs(img_dir, exist_ok=True)
    # 计算单帧字节数
    cap = img_size[0] * img_size[1] * 3
    with open(file_path, 'rb') as f:
        data = f.read()
    config = {
        "file": {"name": os.path.basename(file_path),"size": str(len(data)),},
        "storage": {"url": "","size": ""}
    }
    config_path = os.path.join(img_dir, "config.json")
    with open(config_path, "w") as f:
        f.write(json.dumps(config, indent=4))

    p = math.ceil(len(data) / cap)
    print("帧数:", p)

    with Pool(processes=cpu_count() - 1) as pool:
        for i in range(0, len(data), cap):
            print(f"正在转译第{i // cap + 1}帧")
            image_path = join_path(img_dir, f"frame_{i // cap:06d}.png")
            data_ps = data[i:i + cap] + b'0' * (cap - len(data[i:i + cap]))
            RGB_data = np.frombuffer(data_ps, dtype=np.uint8).reshape(img_size[0], img_size[1], 3)
            pool.apply_async(save_img, args=(image_path, RGB_data))
        pool.close()
        pool.join()
    print("转译时间为", time.time() - a)


if __name__ == '__main__':
    file_path = r'../res/Desktop.7z'
    img_dir = r"D:/zzztest/1"
    img_size = (5000, 5000)
    pan_path = "../res/pan"
    file2img(file_path, img_dir, img_size)
    upload(img_dir, pan_path)
    #up_img("../res/temp/1732262973.5431807/frame_000001.png", 0, Manager().dict())
