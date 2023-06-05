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
        self.blocknum = filename.split('.')[0].split('block')[1]
        self.workspace = os.path.dirname(__file__).split('python')[0]
    
    def getStudentID(self):
        student_id_list = []
        with open(self.workspace + '/raw_repo/' + self.filename, 'r', encoding='utf-8') as csvfile:
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
            output.append([array[i], self.blocknum + '_' + str(args[i])])
        return output
    
if __name__ == '__main__':
    workspace = os.path.dirname(__file__).split('python')[0]
    # 建立原始 seq_index 檔案
    if not os.path.exists(os.path.dirname(__file__).split('python')[0] + '/index/DB_student_cls_SeqIndex.csv'):
        raw_repo_dir = workspace + '/raw_repo/'
        files = os.listdir(raw_repo_dir)
        ## 合併 Block 檔案
        mergedBlock = np.array([['', '']])
        for i in range(len(files)):
            file = files[i]
            block = Block(file)
            raw_array = block.getStudentID()
            seq_array = block.getSeqIndex(raw_array)
            mergedBlock = np.concatenate((mergedBlock, seq_array))
            print('Block ' + str(i) + ' finished')
        
        ## 寫入原始 seq_index 檔案
        with open (workspace + '/index/DB_student_cls_SeqIndex.csv', 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(mergedBlock)
    
    # 精簡化 seq_index 檔案
    ## 讀取原始 seq_index 檔案
    seq_index = np.array([])
    new_seq_index = np.array([['', '']])
    with open (workspace + '/index/DB_student_cls_SeqIndex.csv', 'r', encoding='utf-8') as csvfile:
        seq_index = np.array(list(csv.reader(csvfile)))
    
    ## 取得不重複的學號
    student_id_arr = set(seq_index[:, 0])
    student_id_arr = np.array(list(student_id_arr))
    student_id_arr = np.sort(student_id_arr)
    # print(student_id_arr)
    
    ## 以學號為 key，將所有課程編號合併成一個字串
    for i in range(len(student_id_arr)):
        student_id = student_id_arr[i]
        student_all_class = ''
        for i in range(len(seq_index)):
            if seq_index[i][0] == student_id:
                student_all_class += seq_index[i][1] + '-'
        student_all_class = student_all_class.rstrip('-')
        new_seq_index = np.concatenate((new_seq_index, [[student_id, str(student_all_class)]]))
        if len(student_all_class) != 0:
            print(student_id + ',' + student_all_class)
        else:
            print('no class')
    
    print(new_seq_index)
    
    ## 寫入精簡化 seq_index 檔案
    with open (workspace + '/index/DB_student_cls_SeqIndex_new.csv', 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(new_seq_index)