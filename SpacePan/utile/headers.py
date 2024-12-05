a = """accept:
application/json, text/javascript, */*; q=0.01
accept-encoding:
gzip, deflate, br, zstd
accept-language:
zh-CN,zh;q=0.9
cache-control:
no-cache
connection:
keep-alive
content-length:
102843
content-type:
multipart/form-data; boundary=----WebKitFormBoundarywFBx3AJr3MCWCmfg
host:
csdn-img-blog.obs.cn-north-4.myhuaweicloud.com
origin:
https://mp.csdn.net
pragma:
no-cache
referer:
https://mp.csdn.net/mp_blog/creation/editor?not_checkout=1&spm=1015.2103.3001.8012
sec-ch-ua:
"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"
sec-ch-ua-mobile:
?0
sec-ch-ua-platform:
"Windows"
sec-fetch-dest:
empty
sec-fetch-mode:
cors
sec-fetch-site:
cross-site
user-agent:
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"""


i = 1
re = ""
for x in a.split("\n"):
    if i%2 :
        x = x.replace(":","")
        re += "\"" +x+"\":"
    else:
        x = x.replace("\"","\\\"")
        re += "\"" +x+"\",\n"
    i=i+1
print(re)



















