import json
import requests

with open('config.json', 'r', encoding='utf-8') as f:
    q = json.loads(f.read())["cookies"]["main"]
    cookies = {cookie['name']: cookie['value'] for cookie in q}
def get_conf():
    url = "https://imgservice.csdn.net/direct/v1.0/image/obs/upload?type=blog&rtype=blog_picture&x-image-template=standard&x-image-app=direct_blog&x-image-dir=direct&x-image-suffix=png"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
        'Content-Type': 'application/json',
    }
    a = requests.get(url, headers=headers, cookies=cookies).json()
    #print(json.dumps(a, indent=4))
    return a


def up(conf, img_path):
    with open("img.png", "rb") as f:
        img_data = f.read()
    url = "https://csdn-img-blog.obs.cn-north-4.myhuaweicloud.com/"
    data = {
        "key": conf["data"]["customParam"]['filePath'],
        "policy": conf['data']["policy"],
        "AccessKeyId": conf['data']['accessId'],
        "signature": conf['data']['signature'],
        "callbackUrl": conf['data']['callbackUrl'],
        "callbackBody": conf['data']['callbackBody'],
        "callbackBodyType": conf['data']['callbackBodyType'],
        "x:rtype": conf['data']['customParam']['rtype'],
        "x:watermark": conf['data']['customParam']['watermark'],
        "x:templateName": conf['data']['customParam']['templateName'],
        "x:filePath": conf['data']['filePath'],
        "x:isAudit": conf['data']['customParam']['isAudit'],
        "x:x-image-app": conf['data']['customParam']['x-image-app'],
        "x:type": conf['data']['customParam']['type'],
        "x:x-image-suffix": conf['data']['customParam']['x-image-suffix'],
        "x:username": conf['data']['customParam']['username'],
    }
    files = {
        "file": open(img_path, 'rb'),
       }
    with open(img_path, "rb") as f:
        img_data = f.read()
        print(len(img_data))
    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "connection": "keep-alive",
        "content-length": "102843",
        "content-type": "multipart/form-data; boundary=----WebKitFormBoundarywFBx3AJr3MCWCmfg",
        "host": "csdn-img-blog.obs.cn-north-4.myhuaweicloud.com",
        "origin": "https://mp.csdn.net",
        "pragma": "no-cache",
        "referer": "https://mp.csdn.net/mp_blog/creation/editor?not_checkout=1&spm=1015.2103.3001.8012",
        "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    }
    r = requests.post(url, headers=headers, data=data,cookies=cookies,files=files)
    print(r.text)


conf = get_conf()
up(conf, "img.png")
