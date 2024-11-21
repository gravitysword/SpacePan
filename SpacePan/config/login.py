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
        '''login_element = '//div[@class="header-right common-component-wrapper"]//a[text()="登录" and @class="login-button" and @rel="nofollow"]'
        page.wait_for_selector(login_element)
        page.locator(login_element).click()'''


        page.wait_for_selector('//div[@class="user-icon"]', timeout=60000)
        # main
        main_cookies = page.context.cookies()

        #upload
        page.goto("https://mp.toutiao.com/profile_v4/graphic/publish?from=toutiao_pc&is_new_connect=0&is_new_user=0")
        upload_cookies = page.context.cookies()

        #download
        page.goto("https://www.toutiao.com/article/7390283631459140137/")
        download_cookies = page.context.cookies()

        config['cookies'] = {
            'main': main_cookies,
            'upload': upload_cookies,
            'download': download_cookies
        }

        with open('../config/config.json', 'w') as f:
            f.write(json.dumps(config, indent=4))

        # 关闭浏览器
        browser.close()


if __name__ == '__main__':
    login()
