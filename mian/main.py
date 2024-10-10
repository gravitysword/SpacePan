import time
from compiler import file2img, img2file
from convey import  down,up_request as up
def Up(file_path):
    imgs_dir = f"../res/temp/{time.time()}"
    size = (2500,2500)
    file2img.file_to_img(file_path, imgs_dir, size)
    up.upload_images(imgs_dir)
def Down(url ,file_path):
    imgs_dir = f"../res/temp/{time.time()}"
    down.download_images(url, imgs_dir)
    print(1)
    img2file.img_to_file(imgs_dir, file_path)


if __name__ == '__main__':
    #上传
    file_path = "../res/1.7z"
    a = time.time()
    Up("../res/1.7z")
    print(time.time()-a)

    #下载
    """a = time.time()
    # 图片要保存的路径
    file_dir = "../res/b"
    # 文章链接
    url = "https://www.toutiao.com/article/7424079831064642075/"
    Down(url, file_dir)
    print(time.time() - a)"""



