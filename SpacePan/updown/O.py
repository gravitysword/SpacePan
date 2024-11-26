def check(file_1, file_2):
    with open(file_1, 'rb') as f:
        data_1 = f.read()
    with open(file_2, 'rb') as f:
        data_2 = f.read()
    if data_1 == data_2:
        return True
    else:
        return False

if __name__ == '__main__':
    file_1 = 'D:/zzztest/3/Desktop.7z'
    file_2 = '../res/Desktop.7z'
    if check(file_1, file_2):
        print('The files are identical')
    else:
        print('The files are not identical')

