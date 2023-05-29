'''
以上述 repository 為基礎
製作 sequence index 進行選課查詢
輸入學號可以輸出該學號所選的所有課程之課號
輸入課號可以輸出該課號選課的所有學生之學號
'''

import os
import csv

class Block:
    def __init__(self, filename):
        self.blockname = filename
        self.workspace = os.path.dirname(__file__).split('python')[0]
    
    def getStudentID(self):
        student_id_list = []
        with open(self.workspace + '/repository/' + self.blockname, 'r', encoding='utf-8') as csvfile:
            rows = csv.reader(csvfile)
            for row in rows:
                student_id_list.append(row[0])
        # set 去除重複
        return set(student_id_list)
    
    def add_seqIndex(self, data):
        pass
        
    
if __name__ == '__main__':
    workspace = os.path.dirname(__file__).split('python')[0] + '/repository'
    files = os.listdir(workspace)
    block = Block(files[0])
    print(block.getStudentID())
    
    # for file in files:
    #     block = Block(file)
        