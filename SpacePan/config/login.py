from playwright.sync_api import sync_playwright
import json
import os

def login():
    os.system('python -m playwright install chromium')
    with sync_playwright() as p:
        with open('../config/config.json', 'r') as f:
            config = json.loads(f.read())

        # 启动浏览器，并设置 headless=False 显示界面
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        # 主页
        page.goto("https://www.toutiao.com/")

        page.wait_for_selector('//div[@class="user-icon"]', timeout=120000)
        # main
        main_cookies = page.context.cookies()

        config['cookies'] = {
            'main': main_cookies,
        }

        with open('../config/config.json', 'w') as f:
            f.write(json.dumps(config, indent=4))
        # 关闭浏览器
        browser.close()


if __name__ == '__main__':
    login()
