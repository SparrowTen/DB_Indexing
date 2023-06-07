'''
實作資料 repository:

將原始資料檔案以 block 為單位切割分別儲存
單一 block 最多只能存放一百筆選課資料或上限 8KB 的索引資料
DEMO 時不需要展示分割 repository 的程式
僅需說明 repository 產生的方式即可
'''

import os
import csv

class Repository:
    def __init__(self, filename, dir):
        self.filename = filename
        self.dir = '\\repository\\' + dir + '\\'
        self.block_count = 0
        self.workspace = os.path.dirname(__file__).split('python')[0]
        if not os.path.exists(self.workspace + filename):
            print('錯誤! 沒有該檔案')
            os._exit(0)
        
        # 創建 block 資料夾
        if not os.path.exists(self.workspace + dir):
            os.mkdir(self.workspace + dir)

    def getlength(self):
        with open(self.workspace + self.filename, 'r', encoding='utf-8') as csvfile:
            raw_data = csv.reader(csvfile)
            self.length = len(list(raw_data))
        return self.length
    
    def getBlockCount(self):
        return self.block_count
    
    def split(self, size_limit):
        size_limit = size_limit * 1024
        block_index = 0
        buffer = 0
        data = []
        with open(self.workspace + self.filename, 'r', encoding='utf-8') as csvfile:
            rows = csv.reader(csvfile)
            for row in rows:
                buffer += len(str(row).encode('utf-8'))
                if buffer > size_limit:
                    self.create_file('block' + str(block_index) + '.csv', data)
                    block_index += 1
                    buffer = 0
                    data = []
                data.append(row)
    
    def create_file(self, filename, data):
        with open(self.workspace + self.dir + filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            for row in data:
                writer.writerow(row)
        print('已建立 ' + filename)
        self.block_count += 1
    
if __name__ == '__main__':
    print('請輸入來源檔案路徑')
    filename = input()
    print('請輸入輸出檔案資料夾名稱')
    dir = input()
    r = Repository(filename, dir)
    
    print('資料總共' + str(r.getlength()) + '筆')
    print('請輸入每個 block 的上限大小 (KB)')
    size_limit = int(input())
    r.split(size_limit)
    print('共分割成' + str(r.getBlockCount()) + '個 block ')
    print('每個 block 最多' + str(size_limit) + 'KB')