import json


def x(a):
    a = a.replace(" ", "")
    lines = a.split('\n')
    text = ""
    for line in lines:
        s1 = line.find(":")
        s, e = line[:s1], line[s1 + 1:].replace("\"", "\\\"")
        text += f"\"{s}\":\"{e}\",\n"
    print(text)

a = '''key: direct/ed4fc457aaa64ef5ad4f679fb8d25f1f.png
policy: eyJleHBpcmF0aW9uIjoiMjAyNC0xMS0yM1QxNDoyNjo1OS4xODZaIiwiY29uZGl0aW9ucyI6W3siYnVja2V0IjoiY3Nkbi1pbWctYmxvZyJ9LFsiY29udGVudC1sZW5ndGgtcmFuZ2UiLDAsNTI0Mjg4MF0sWyJzdGFydHMtd2l0aCIsIiRrZXkiLCJkaXJlY3QvZWQ0ZmM0NTdhYWE2NGVmNWFkNGY2NzlmYjhkMjVmMWYucG5nIl1dfQ==
AccessKeyId: HPCIICCXJ0CDSZ7ST7FA
signature: HhfK/t+/+raQY/EoWpoZfBy5Er8=
callbackUrl: https://imgservice.csdn.net/direct/v1.0/image/obs/callback
callbackBody: {"rtype":"$(x:rtype)","watermark":"$(x:watermark)","templateName":"$(x:templateName)","filePath":"$(x:filePath)","isAudit":"$(x:isAudit)","x-image-app":"$(x:x-image-app)","type":"$(x:type)","x-image-suffix":"$(x:x-image-suffix)","username":"$(x:username)"}
callbackBodyType: application/json
x:rtype: blog_picture
x:watermark: 2301_80119627
x:templateName: standard
x:filePath: direct/ed4fc457aaa64ef5ad4f679fb8d25f1f.png
x:isAudit: 1
x:x-image-app: direct_blog
x:type: blog
x:x-image-suffix: png
x:username: 2301_80119627
file: （二进制）'''

x(a)
