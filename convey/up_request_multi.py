from selenium import webdriver
from selenium.webdriver.common.by import By
import os
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import requests
import multiprocessing
from multiprocessing import Manager

from concurrent.futures import ThreadPoolExecutor, as_completed


with open("../config/config.json", 'rb') as f:
    config = json.load(f)
    selenium_cooikes = config["cookies"]["upload_images"]
    cookies = {cookie['name']: cookie['value'] for cookie in selenium_cooikes}
    webdriver_path = config["webdriver"]["path"]


def create_element(args):
    args = dict(args)
    img_url = args["data"]["image_url"]
    img_uri = args["data"]["image_uri"]
    img_width = args["data"]["image_width"]
    img_height = args["data"]["image_height"]
    img_mime_type = args["data"]["image_mime_type"]
    img_type = args["data"]["image_type"]

    element_temp = f'''<div __syl_tag="true" contenteditable="false" draggable="true" class="">
    <mask>
    <div class="pgc-image pgc-card-fixWidth">
    <div class="pgc-img-wrapper">
    <div class="img-wrapper">
    <div class="img-loading-container default">
    <img src="{img_url}" class="" image_type="{img_type}" mime_type="{img_mime_type}" web_uri="{img_uri}" img_width="{img_width}" img_height="{img_height}" width="{img_width}">
    <span class="img-loading-progress default"><span class="img-loading-bar"></span></span></div>
    <div class="mask no-optimize">
    <div class="line-mask"></div>
    <div class="sub-mask"></div>
    </div></div></div></div>
    </mask>
    </div>'''.replace('\n', '')

    return element_temp


def up_img(img_path,j,elements):
    url = "https://mp.toutiao.com/spice/image?upload_source=20020002&aid=1231&device_platform=web"
    a = requests.post(url, files= {'image': open(img_path, 'rb')}, cookies=cookies)
    elements[j] = a.json()



def upload_images(img_dir):
    a = time.time()
    imgs = [os.path.join(os.path.abspath(img_dir), img_name) for img_name in os.listdir(img_dir) if
            os.path.splitext(img_name)[1].lower() in {".png"}]

    elements = Manager().dict()
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        for img_path, j in zip(imgs, range(len(imgs))):
            print(f"uploading {img_path}")
            pool.apply_async(up_img, args=(img_path,j,elements))
        pool.close()
        pool.join()
    print(f"uploading images cost {time.time()-a}s")
    input("1")
    #初始化
    img_config = os.path.join(img_dir, 'config.json')
    with open(img_config, 'r') as f:
        img_config = str(json.load(f)).replace("'", '"')

    service = Service(executable_path=webdriver_path)
    options = webdriver.ChromeOptions()
    options.add_argument('window-size=1000,1000')
    driver = webdriver.Chrome(service=service, options=options)

    driver.get("https://mp.toutiao.com/profile_v4/graphic/publish")
    for cookie in selenium_cooikes:
        driver.add_cookie(cookie)
    time.sleep(1)

    driver.get("https://mp.toutiao.com/profile_v4/graphic/publish")
    driver.maximize_window()
    # 滚动到指定位置
    driver.execute_script("window.scrollTo(0, 500);")  # 滚动到距离顶部 500px 的位置
    # 设置无封面
    button_fengmian = driver.find_element(By.XPATH, '//span[text()="无封面"]')
    driver.execute_script("arguments[0].click();", button_fengmian)
    time.sleep(1)

    diiiv = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//div[@class="ProseMirror"]')))
    title_element = driver.find_element(By.CSS_SELECTOR,
                                        '#root > div > div.left-column > div > div.publish-editor > div.publish-editor-title-wrapper > div > div > div.title-wrapper > div > div > div > textarea')
    title_element.send_keys("test")

    text_element = driver.find_element(By.XPATH,
                                       '/html/body/div[1]/div/div[3]/section/main/div[2]/div/div/div[2]/div/div/div[1]/div/div[1]/div[4]/div/div[1]/p')
    text_element.send_keys(img_config + "1" * 300)
    print(len(elements))
    #上传

    for i in range(len(elements)):
        element_temp = create_element(elements[i])
        print(f"uploading {i}th image")
        script = f"""
        var newElement = document.createElement('div');
        newElement.innerHTML = '{element_temp}';
        arguments[0].appendChild(newElement);
        """
        driver.execute_script(script, diiiv)
        # 发布1
    element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH,
                                            '//button[@class="byte-btn byte-btn-primary byte-btn-size-large byte-btn-shape-square publish-btn publish-btn-last"]'))
        )
    driver.execute_script("arguments[0].click();", element)
        # 发布2
    element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH,
                                            '//button[@class="byte-btn byte-btn-primary byte-btn-size-large byte-btn-shape-square publish-btn publish-btn-last"]'))
        )
    driver.execute_script("arguments[0].click();", element)
    time.sleep(5)
if __name__ == '__main__':
    a = time.time()
    upload_images("../res/b")
    print(time.time()-a)
