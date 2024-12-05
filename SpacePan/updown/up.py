import requests
from playwright.sync_api import sync_playwright
import os,  time
import numpy as np
import cv2, json
from utile.u import *
import concurrent.futures

with open('../config/config.json', 'r', encoding='utf-8') as f:
    config = json.loads(f.read())
    play_cookies = config["cookies"]["main"]
    cookies = {cookie['name']: cookie['value'] for cookie in play_cookies}
    executor_path = config["webdriver"]["path"]


def up_img(storage,index,data,img_size,cap):
    data_ps = data + b'0' * (cap - len(data))
    RGB_data = np.frombuffer(data_ps, dtype=np.uint8).reshape(img_size[0], img_size[1], 3)
    _, img_data = cv2.imencode('.png', RGB_data)
    url = "https://mp.toutiao.com/spice/image?upload_source=20020002&aid=1231&device_platform=web"
    a = requests.post(url=url, files={'image': img_data}, cookies=cookies)
    storage[str(index)] = a.json()["data"]["image_url"]
    print(f"第 {index + 1} 张图片上传成功")
    return a.json()["data"]["image_url"]


def upload(file_path, pan_path,img_size=(5000, 5000) ):
    a = time.time()
    cap = img_size[0] * img_size[1] * 3
    size_data, i = 0, 0
    storage = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(cap)
                if not data:
                    break
                size_data += len(data)
                futures.append(executor.submit(up_img, storage, i, data, img_size,cap))
                print(f"正在上传第 {i + 1} 张图片")
                i += 1
        concurrent.futures.wait(futures)

    config = {
        "file": {"name": os.path.basename(file_path), "size": str(size_data), },
        "storage": {"url": "", "size": ""}
    }

    print("上传时间为", time.time() - a)

    #获取存储地址
    storage = bytearray(json.dumps(storage), encoding='utf-8')
    storage_size = len(storage)
    storage_url = up_img({},0,storage,(2000,2000),2000*2000*3)

    config["storage"] = {
        "url": storage_url,
        "size": str(storage_size)
    }
    #上传
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False,executable_path=executor_path)
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
        page.evaluate("window.scrollTo(0, 15000);")

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

        page.wait_for_selector(
            '//button[@class="byte-btn byte-btn-primary byte-btn-size-large byte-btn-shape-square publish-btn publish-btn-last"]')

        print(f"总计时间", time.time() - a)
        print(f"上传完成")


if __name__ == '__main__':
    file_path = '../res/README'
    pan_path = '/res/R'
    upload(file_path,  pan_path)
