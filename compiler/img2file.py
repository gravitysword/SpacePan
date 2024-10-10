import cv2
import os
import time
import json

def img_to_file(img_dir, file_dir):
    config_path = os.path.join(img_dir, 'config.json')
    os.makedirs(file_dir, exist_ok=True)

    with open(config_path, 'r') as f:
        config = json.loads(f.read())
    file_path = os.path.join(file_dir, config['name']).replace("\\", "/")
    size = config['size']

    d = 0
    imgs = [f for f in os.listdir(img_dir) if os.path.splitext(f)[1].lower() in {".png"}]
    l_imgs = len(imgs)
    with open(file_path, 'wb') as f:
        for i, img_name in enumerate(imgs):
            img_path = os.path.join(img_dir, img_name).replace("\\", "/")
            RGB_data = cv2.imread(img_path).tobytes()

            if i == l_imgs - 1:
                f.write(RGB_data[:size - d])
            else:
                f.write(RGB_data)
                d += len(RGB_data)
    print(file_path, "写入成功")


if __name__ == '__main__':
    a = time.time()
    img_dir = "../res/a"
    file_path = "../res/1"
    img_to_file(img_dir, file_path)
    print(time.time() - a)
