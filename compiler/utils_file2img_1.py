import cv2
import numpy as np
import os
import time
import multiprocessing


def file_to_img(file_path, img_size, batch_size=10):
    file_dir = os.path.dirname(os.path.abspath(file_path))   #图片保存路径
    cap = img_size[0] * img_size[1] * 3  #每张图片大小
    frame = 0
    with open(file_path, 'rb') as file:
        while True:
            batch_data = []
            for _ in range(batch_size):
                data_ps = file.read(cap)
                if not data_ps:
                    break
                data_ps += b'0' * (cap - len(data_ps))  #需要补齐

                batch_data.append(np.frombuffer(data_ps, dtype=np.uint8).reshape(img_size[0], img_size[1], 3))

            if not batch_data:
                break

            # 需要保存的图片路径的列表
            image_paths = [f"{file_dir}/frame_{frame + i:06d}.png" for i in range(len(batch_data))]

            with multiprocessing.Pool(processes=min(multiprocessing.cpu_count(), len(batch_data))) as pool:
                # 使用进程池执行保存图片操作
                pool.starmap(save_image, zip(batch_data, image_paths))


            print(f"Processed frames {frame} to {frame + len(batch_data) - 1}")
            frame += len(batch_data)

def save_image(RGB_data, image_path):
    cv2.imwrite(image_path, RGB_data)    # 保存图片


if __name__ == '__main__':
    start_time = time.time()
    file_to_img("res/a/1.7z", (2500, 2500), batch_size=10)
    print(f"Total time: {time.time() - start_time:.2f} seconds")
