import time
from updown import up,down


def Up():
    file_path = "../res/z.7z"
    img_dir = f"../res/temp/{time.time()}"
    img_size = (5000,5000)
    pan_path = "../res/pan"
    up.file2img(file_path, img_dir, img_size)
    up.upload(img_dir, pan_path)


def Down():
    a = time.time()
    img_dir = f"D:/zzztest/2"
    file_path = r"D:/zzztest/3"
    url = 'https://www.toutiao.com/article/7439928751518925353/'
    down.download(url, img_dir)
    down.img2file(img_dir, file_path)
    print(time.time() - a)



if __name__ == '__main__':
    x = input("输入操作模式\n")
    if x == "1":
        Up()
    else:
        Down()
