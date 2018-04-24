"""
删除源文件未做
"""

import os, sys
from basic import * 


filename = "test.mp4"                   #要处理

def merge_file():  
    '将src路径下的所有文件块合并，并存储到des路径下。'
    files = sort_file()
    outputpath = DES + filename
    with open(outputpath, 'wb') as output:  
        for file in files:
            file = SRC + file    
            with open(file, 'rb') as infile:  
                data = infile.read()  
                output.write(data) 
    delete_file() 


def sort_file():
    files = os.listdir(SRC)
    for i in range(len(files)):
        files[i] = files[i].split('^')
        files[i][0] = int(files[i][0])
    files.sort()
    for i in range(len(files)):
        files[i][0] = str(files[i][0])
        files[i] = files[i][0] + '^' + files[i][1]
    return files


def delete_file():
    files = os.listdir(SRC)
    for file in files:
        file = SRC + file
        if os.path.exists(file):
            #删除文件，可使用以下两种方法。
            os.remove(file)
            #os.unlink(my_file)
        else:
            print("no such file: "+ file)


if __name__ == '__main__':
    merge_file()