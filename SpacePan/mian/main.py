import time
from updown import up,down


def Up():
    file_path = "../res/README"
    img_dir = f"../res/temp/{time.time()}"
    img_size = (5000,5000)
    pan_path = "../res/pan"
    up.file2img(file_path, img_dir, img_size)
    up.upload(img_dir, pan_path)


def Down():
    a = time.time()
    img_dir = f"../res/temp/{time.time()}"
    file_path = r"../res/b1"
    url = 'https://www.toutiao.com/article/7439754964227899915/'
    down.download(url, img_dir)
    down.img2file(img_dir, file_path)
    print(time.time() - a)



if __name__ == '__main__':
    x = input("输入操作模式\n")
    if x == "1":
        Up()
    else:
        Down()
