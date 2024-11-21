from multiprocessing import Manager
import requests
from playwright.sync_api import sync_playwright
import os, math, time
import numpy as np
import cv2, json
from utile.u import *
from multiprocessing import Pool, cpu_count

with open('../config/config.json', 'r') as f:
    config = json.loads(f.read())
    play_cookies = config["cookies"]["upload"]
    cookies = {cookie['name']: cookie['value'] for cookie in play_cookies}


def create_element(config):
    config = config["data"]
    img_url = config["image_url"]
    img_uri = config["image_uri"]
    img_width = config["image_width"]
    img_height = config["image_height"]
    img_mime_type = config["image_mime_type"]
    img_type = config["image_type"]

    element = f'''
<div __syl_tag="true" contenteditable="false" draggable="true" class="">
    <mask>
        <div class="pgc-image pgc-card-fixWidth">
            <div class="pgc-img-wrapper">
                <div class="img-wrapper">
                    <div class="img-loading-container default">
                        <img src="{img_url}" class="" image_type="{img_type}" mime_type="{img_mime_type}" web_uri="{img_uri}" img_width="{img_width}" img_height={img_height}" width={img_width}">
                        <span class="img-loading-progress default">
                            <span class="img-loading-bar">
                            </span>
                        </span>
                    </div>
                </div>
            </div>
        </div>
    </mask>
</div>'''
    return element


def upload(img_dir, pan_path):
    a = time.time()
    imgs = [join_path(os.path.abspath(img_dir), img_name) for img_name in os.listdir(img_dir) if
            os.path.splitext(img_name)[1].lower() in {".png"}]

    elements = Manager().dict()
    print(f"上传文件中...")
    for j, img_path in enumerate(imgs):
        up_img(img_path, j, elements)
    print("上传时间", time.time() - a)
    print(f"预发布中...")
    a = time.time()
    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://mp.toutiao.com/profile_v4/graphic/publish?from=toutiao_pc&is_new_connect=0&is_new_user=0")
        context.add_cookies(play_cookies)
        page.set_viewport_size({"width": 1500, "height": 800})
        time.sleep(1)
        #标题与正文
        img_config = join_path(img_dir, 'config.json')
        with open(img_config, 'r') as f:
            config = json.loads(f.read())
            file_name = config["name"]
            img_config = str(config).replace("'", '"')
        title = page.wait_for_selector('//textarea[@placeholder="请输入文章标题（2～30个字）"]')
        title.fill("Pan: " + join_path(pan_path, file_name))
        text = page.locator('//div[@class="ProseMirror"]/p')
        text.fill(img_config + "1" * 300)

        page.wait_for_selector(
            '#root > div > div.left-column > div > div.publish-editor > div.syl-editor-wrap > div > div.ProseMirror')

        #<-- 预发布 -->
        for i in range(len(elements)):
            element_temp = create_element(elements[i])
            page.evaluate(f"""
                    () => {{
                        const element = `{element_temp}`;
                        const container = document.querySelector('#root > div > div.left-column > div > div.publish-editor > div.syl-editor-wrap > div > div.ProseMirror');  // 或者选择其他容器
                        container.insertAdjacentHTML('beforeend', element);
                    }}
                """)

        time.sleep(3)
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


def up_img(img_path, j, elements):
    url = "https://mp.toutiao.com/spice/image?upload_source=20020002&aid=1231&device_platform=web"
    a = requests.post(url=url, files={'image': (os.path.basename(img_path), open(img_path, 'rb'))}, cookies=cookies)
    elements[j] = a.json()
    print(f"第{j + 1}张图片上传完成")


def save_img(image_path, RGB_data):
    cv2.imwrite(image_path, RGB_data)


def file2img(file_path, img_dir, img_size):
    a = time.time()
    os.makedirs(img_dir, exist_ok=True)
    # 计算单帧字节数
    cap = img_size[0] * img_size[1] * 3
    with open(file_path, 'rb') as f:
        data = f.read()
    config = {
        "name": os.path.basename(file_path),
        "size": str(len(data)),
    }
    config_path = os.path.join(img_dir, "config.json")
    with open(config_path, "w") as f:
        f.write(json.dumps(config, indent=4))

    p = math.ceil(len(data) / cap)
    print("帧数:", p)

    with Pool(processes=cpu_count()) as pool:
        for i in range(0, len(data), cap):
            image_path = os.path.join(img_dir, f"frame_{i // cap:06d}.png")
            data_ps = data[i:i + cap] + b'0' * (cap - len(data[i:i + cap]))
            RGB_data = np.frombuffer(data_ps, dtype=np.uint8).reshape(img_size[0], img_size[1], 3)
            pool.apply_async(save_img, args=(image_path, RGB_data))
        pool.close()
        pool.join()
    print("转译时间为", time.time() - a)


if __name__ == '__main__':
    file_path = "../res/video.zip"
    img_dir = f"../res/temp/{time.time()}"
    img_size = (5000,5000)
    pan_path = "../res/pan"
    file2img(file_path, img_dir, img_size)
    upload(img_dir, pan_path)
