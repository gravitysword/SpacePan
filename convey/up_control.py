from selenium import webdriver
from selenium.webdriver.common.by import By
import os
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from tqdm import tqdm


# 设置Chrome浏览器无头模式


def up(img_dir):
    with open('../config/config.json', 'r') as f:
        config = json.load(f)
        current_cookies = config['cookies']["upload_images"]
        webdriver_path = config['webdriver']['path']

    img_config = os.path.join(img_dir, 'config.json')
    with open(img_config, 'r') as f:
        img_config = str(json.load(f)).replace("'", '"')

    service = Service(executable_path=webdriver_path)

    options = webdriver.ChromeOptions()
    options.add_argument('window-size=1000,1000')
    #options.add_argument('window-position=2000,1000')
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://mp.toutiao.com/profile_v4/graphic/publish")
    for cookie in current_cookies:
        driver.add_cookie(cookie)
    time.sleep(1)
    driver.get("https://mp.toutiao.com/profile_v4/graphic/publish")
    #删除
    x = WebDriverWait(driver, 20).until(EC.presence_of_element_located(
        (By.XPATH, '//div[@class="byte-drawer drawer slideRight-appear-done slideRight-enter-done"]')))
    driver.execute_script("""var element = arguments[0];element.parentNode.removeChild(element);""", x)

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,
                                                                    '/html/body/div[1]/div/div[3]/section/main/div[2]/div/div/div[2]/div/div/div[1]/div/div[1]/div[4]/div/div[1]/p')))

    title_element = driver.find_element(By.CSS_SELECTOR,
                                        '#root > div > div.left-column > div > div.publish-editor > div.publish-editor-title-wrapper > div > div > div.title-wrapper > div > div > div > textarea')
    title_element.send_keys("test")

    text_element = driver.find_element(By.XPATH,
                                       '/html/body/div[1]/div/div[3]/section/main/div[2]/div/div/div[2]/div/div/div[1]/div/div[1]/div[4]/div/div[1]/p')
    text_element.send_keys(img_config + "1" * 300)

    # 滚动到指定位置
    driver.execute_script("window.scrollTo(0, 500);")  # 滚动到距离顶部 500px 的位置
    #设置无封面
    button_fengmian = driver.find_element(By.XPATH, '//span[text()="无封面"]')
    driver.execute_script("arguments[0].click();", button_fengmian)
    time.sleep(1)
    #上传图片

    action_chains = ActionChains(driver)
    action_chains.key_down(Keys.CONTROL).send_keys('p').key_up(Keys.CONTROL).perform()
    time.sleep(1)

    send_element = driver.find_element(By.XPATH, '//div[@class="btn-upload-handle upload-handler"]/input')
    imgs = [f for f in os.listdir(img_dir) if os.path.splitext(f)[1].lower() in {".png"}]

    progress = tqdm(total=len(imgs), desc="Processing")

    for img_name, j in zip(imgs, range(len(imgs))):
        progress.update(1)
        progress.set_description(f"Processing {j + 1} ")  # 更新描述

        full_path = os.path.join(os.path.abspath(img_dir), img_name)
        #print(full_path)
        send_element.send_keys(full_path)
        if j%3==2:
            time.sleep(1)
            WebDriverWait(driver, 100).until(
                EC.presence_of_element_located((By.XPATH,
                                            '//button[@data-e2e="imageUploadConfirm-btn" and @class="byte-btn byte-btn-primary byte-btn-size-large byte-btn-shape-square" and @type="button"]/span'))
            )

        #确定
    while True:
        a = driver.find_element(By.XPATH, '//div[@class="upload-image-tips"]/span')
        if a.text == f"已上传 {len(imgs)} 张图片，支持拖拽调整图片顺序":
            break
        time.sleep(2)

    driver.find_element(By.XPATH,
                        '//button[@data-e2e="imageUploadConfirm-btn" and @class="byte-btn byte-btn-primary byte-btn-size-large byte-btn-shape-square" and @type="button"]/span').click()
    time.sleep(1)

    #发布1
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH,
                                        '//button[@class="byte-btn byte-btn-primary byte-btn-size-large byte-btn-shape-square publish-btn publish-btn-last"]'))
    )
    driver.execute_script("arguments[0].click();", element)
    #发布2
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH,
                                        '//button[@class="byte-btn byte-btn-primary byte-btn-size-large byte-btn-shape-square publish-btn publish-btn-last"]'))
    )
    driver.execute_script("arguments[0].click();", element)

    input("over")
