from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

def login():
    with open('config.json', 'r') as f:
        config = json.load(f)
    webdriver_path = config['webdriver']['path']

    service =Service(executable_path=webdriver_path)
    driver = webdriver.Chrome(service= service)
    driver.maximize_window()

    driver.get("https://www.toutiao.com")

    #点击登录按钮
    log = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//a[@class="login-button"]')))
    driver.execute_script("arguments[0].click();", log)

    #等待用户登录
    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH,'//div[@class="user-icon"]')))

    #获取用户信息
    driver.get("https://mp.toutiao.com/profile_v4/graphic/publish")
    upload_cookie = driver.get_cookies()
    time.sleep(1)
    driver.get("https://www.toutiao.com/article/7422639326531453492/")
    download_cookie = driver.get_cookies()

    config['cookies']['upload_images'] = upload_cookie
    config['cookies']['download_images'] = download_cookie

    #写入配置文件
    with open('config.json', 'w') as f:
        f.write(json.dumps(config,indent=4))

    print("初始化完成")
    input("Press Enter to continue...")

login()
















