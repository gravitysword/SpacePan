a = """accept:
text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
accept-encoding:
gzip, deflate, br, zstd
accept-language:
zh-CN,zh;q=0.9
cache-control:
max-age=0
cookie:
__ac_signature=_02B4Z6wo00f01nth7cAAAIDDVeYg6ytQEWp7QelAAPnpa6; tt_webid=7422530264213636659; gfkadpd=24,6457; ttcid=85ec7c0b1b684cc5b2523556199a9cf650; x-web-secsdk-uid=b3a2d821-4806-474d-b334-1d3574fd60c2; local_city_cache=%E7%BB%B5%E9%98%B3; csrftoken=9e13a48146216b62a9c9e2fee15bbca4; s_v_web_id=verify_m1x589ii_BgXS3yQY_BtK5_4RHo_8Zo7_J8xGvjeIntmA; _ga=GA1.1.1763289983.1728192563; passport_csrf_token=94824d25e7ca728bf30b5a0b2d512c74; passport_csrf_token_default=94824d25e7ca728bf30b5a0b2d512c74; n_mh=QP5RNJ5WWEiqmngo9SuRWVIzQXcxrTQRjEEejWQIYt8; sso_uid_tt=ac78da1f71c24952aea7dfa0d0cc76e3; sso_uid_tt_ss=ac78da1f71c24952aea7dfa0d0cc76e3; toutiao_sso_user=05aea095f9e177cc18bc2e48d0245831; toutiao_sso_user_ss=05aea095f9e177cc18bc2e48d0245831; sid_ucp_sso_v1=1.0.0-KGEwM2ZlNjllN2FmZTQ3NTIxYTUzZjc5N2E5NWI5ZjMwODc3YzdmZmIKGwiEw_muGRCdwIi4BhgYIAwwmZzAuwU4BkD0BxoCaGwiIDA1YWVhMDk1ZjllMTc3Y2MxOGJjMmU0OGQwMjQ1ODMx; ssid_ucp_sso_v1=1.0.0-KGEwM2ZlNjllN2FmZTQ3NTIxYTUzZjc5N2E5NWI5ZjMwODc3YzdmZmIKGwiEw_muGRCdwIi4BhgYIAwwmZzAuwU4BkD0BxoCaGwiIDA1YWVhMDk1ZjllMTc3Y2MxOGJjMmU0OGQwMjQ1ODMx; passport_auth_status=fd4cbf7a733734b7410f09a7c080e4e4%2C; passport_auth_status_ss=fd4cbf7a733734b7410f09a7c080e4e4%2C; sid_guard=22600c0b6798563ad75e12e7e2d5e470%7C1728192542%7C5184001%7CThu%2C+05-Dec-2024+05%3A29%3A03+GMT; uid_tt=e89b291e5b40ef0f4cccd988762c6157; uid_tt_ss=e89b291e5b40ef0f4cccd988762c6157; sid_tt=22600c0b6798563ad75e12e7e2d5e470; sessionid=22600c0b6798563ad75e12e7e2d5e470; sessionid_ss=22600c0b6798563ad75e12e7e2d5e470; is_staff_user=false; sid_ucp_v1=1.0.0-KDNkMzJmZmU2Yjg4OGM2ZGYyNWZkYzgyZTQ1ZTYzMzc2ZWYyZDBjYTIKFQiEw_muGRCewIi4BhgYIAw4BkD0BxoCaGwiIDIyNjAwYzBiNjc5ODU2M2FkNzVlMTJlN2UyZDVlNDcw; ssid_ucp_v1=1.0.0-KDNkMzJmZmU2Yjg4OGM2ZGYyNWZkYzgyZTQ1ZTYzMzc2ZWYyZDBjYTIKFQiEw_muGRCewIi4BhgYIAw4BkD0BxoCaGwiIDIyNjAwYzBiNjc5ODU2M2FkNzVlMTJlN2UyZDVlNDcw; store-region=cn-ha; store-region-src=uid; odin_tt=95ff31ea9abc5ede6273b278f309a9b0c99d19402ca4b14553c00c56b9b6fe72c3e4a6f49ac26ed79cf458f253d4281c; _ga_QEHZPBE5HH=GS1.1.1728199193.3.1.1728201024.0.0.0; tt_anti_token=pazxJr1mX3iENyq-5efcff47c105f5ed25f59b2497920aaf8542dcbc52ce71f4cd005f21ad37af53; ttwid=1%7CXnPLxbPAgA21lEVSmdr-3JfVpLhPII_lEkvG1PawhrQ%7C1728200988%7C16b22817c82660ccfbb1b742852821cbb46977413b6b37fd16f218c60c8dd95a; tt_scid=wBIdoQJfu6QOnSyROHs9o.XV5q-w0sZmQ6DokiZNRuYq6CEvvv-rKM36BRSJ9QRK6bde
priority:
u=0, i
referer:
https://www.toutiao.com/c/user/token/MS4wLjABAAAA3p6RScMcFryE6ZYrCVPPS8grycaT6z7Gy7Jzz8Iq9aQ/?source=list&log_from=3a66167b720ae_1728201021675
sec-ch-ua:
"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"
sec-ch-ua-mobile:
?0
sec-ch-ua-platform:
"Windows"
sec-fetch-dest:
document
sec-fetch-mode:
navigate
sec-fetch-site:
same-origin
sec-fetch-user:
?1
upgrade-insecure-requests:
1
user-agent:
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"""


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



















