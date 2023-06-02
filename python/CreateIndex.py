'''
以上述 repository 為基礎
製作 sequence index 進行選課查詢
輸入學號可以輸出該學號所選的所有課程之課號
輸入課號可以輸出該課號選課的所有學生之學號
'''

import os
import csv
import numpy as np

class Block:
    def __init__(self, filename):
        self.filename = filename
        self.blockname = filename.split('.')[0]
        self.workspace = os.path.dirname(__file__).split('python')[0]
    
    def getStudentID(self):
        student_id_list = []
        with open(self.workspace + '/repository/' + self.filename, 'r', encoding='utf-8') as csvfile:
            rows = csv.reader(csvfile)
            for row in rows:
                if row[0][0] == 'D':
                    student_id_list.append(row[0])
        # set 去除重複
        # return set(student_id_list)
        
        # numpy sort
        return np.array(student_id_list)
    
    def getSeqIndex(self, data):
        array = np.sort(data)
        args = np.argsort(data)
        output = []
        for i in range(len(array)):
            output.append([array[i], self.blockname + '_' + str(args[i])])
        return output
    
if __name__ == '__main__':
    workspace = os.path.dirname(__file__).split('python')[0] + '/repository/'
    files = os.listdir(workspace)
    # print(files)
    # print('Total: ' + str(len(files)) + ' files')
    # os._exit(0)
    mergedBlock = np.array([['', '']])
    for i in range(len(files)):
        file = files[i]
        block = Block(file)
        raw_array = block.getStudentID()
        seq_array = block.getSeqIndex(raw_array)
        mergedBlock = np.concatenate((mergedBlock, seq_array))
        print('Block ' + str(i) + ' finished')
    mergedBlock = np.sort(mergedBlock, axis=0)
    print(mergedBlock)
    with open (block.workspace + '/index/DB_student_cls_SeqIndex.csv', 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(mergedBlock)