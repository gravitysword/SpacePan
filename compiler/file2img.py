import os
import math
import time
import numpy as np
import cv2
import multiprocessing
import json

def file_to_img(file_path, img_dir, img_size):
    # 确保输出目录存在
    os.makedirs(img_dir, exist_ok=True)
    # 计算单帧字节数
    cap = img_size[0] * img_size[1] * 3
    with open(file_path, 'rb') as file:
        data = file.read()

    config = {
        "name": os.path.basename(file_path),
        "size": str(len(data)),
    }
    config_path = os.path.join(img_dir, "config.json")
    with open(config_path, "w") as f:
        f.write(json.dumps(config, indent=4))
        
    # 计算需要的帧数
    p = math.ceil(len(data) / cap)
    print("帧数:", p)

    # 使用进程池来优化进程管理
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:

        for i in range(0, len(data), cap):
            image_path = os.path.join(img_dir, f"frame_{i//cap:06d}.png")
            data_ps = data[i:i + cap] + b'0' * (cap - len(data[i:i + cap]))
            RGB_data = np.frombuffer(data_ps, dtype=np.uint8).reshape(img_size[0], img_size[1], 3)
            pool.apply_async(work_file, args=(RGB_data, image_path))

        # 等待所有进程完成
        pool.close()
        pool.join()
def work_file(RGB_data, image_path):
    # 将 RGB 数据写入文件
    cv2.imwrite(image_path, RGB_data)


if __name__ == '__main__':
    start_time = time.time()
    file = "../res/1.7z"
    img_dir = "../res/b"
    img_size = (2500, 2500)
    file_to_img(file, img_dir, img_size)
    print("总耗时:", time.time() - start_time)
