import time
from updown import up,down

def download_file(url,file_path):
    file_path = f"D:/zzztest/{time.time()}"
    url = 'https://www.toutiao.com/article/7441807664071311926/?log_from=19432a7cffeeb_1732681213061'
    down.download(url, file_path)

def upload_file(file_path):
    file_path = f"D:/zzztest/{time.time()}"
    pan_path = '/res/1.7z'
    url = up.upload(file_path, pan_path)
    print(url)


