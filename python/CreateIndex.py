'''
以上述 repository 為基礎
製作 sequence index 進行選課查詢
輸入學號可以輸出該學號所選的所有課程之課號
輸入課號可以輸出該課號選課的所有學生之學號
'''

import os
import csv
import numpy as np
from tqdm import tqdm, trange

class Block:
    def __init__(self, dir, filename):
        self.dir = '\\' + dir + '\\'
        self.filename = filename
        self.blocknum = filename.split('.')[0].split('block')[1]
        self.workspace = os.path.dirname(__file__).split('python')[0]
    
    def getStudentID(self):
        student_id_list = []
        with open(self.workspace + self.dir + self.filename, 'r', encoding='utf-8') as csvfile:
            rows = csv.reader(csvfile)
            for row in rows:
                if row[0][0] == 'D':
                    student_id_list.append(row[0])
        return np.array(student_id_list)
    
    def getSeqIndex(self, data):
        array = np.sort(data)
        args = np.argsort(data)
        output = []
        for i in range(len(array)):
            output.append([array[i], self.blocknum + '_' + str(args[i])])
        return output

if __name__ == '__main__':
    # 程式資料夾工作區
    workspace = os.path.dirname(__file__).split('python')[0]
    dir = '\\raw_block\\'
    
    # 建立原始 seq_index 檔案
    
    if not os.path.exists(os.path.dirname(__file__).split('python')[0] + '/index/seq_student_cls.csv'):
        raw_repo_dir = workspace + dir
        files = os.listdir(raw_repo_dir)
        create_block_process = tqdm(total=len(files), desc='分割 block ', ncols=100)
        # 合併 Block 檔案
        mergedBlock = np.array([['', '']])
        for i in range(len(files)):
            file = files[i]
            block = Block(dir, file)
            raw_array = block.getStudentID()
            seq_array = block.getSeqIndex(raw_array)
            mergedBlock = np.concatenate((mergedBlock, seq_array))
            create_block_process.update(1)

        # 讀取原始 seq_index 檔案
        seq_index = mergedBlock
        
        # 取得不重複的學號
        student_id_arr = set(seq_index[:, 0])
        student_id_arr = np.array(list(student_id_arr))
        student_id_arr = np.sort(student_id_arr)
        
        # 創建進度條
        simple_process = tqdm(total=len(student_id_arr), desc='簡化 seq_index 檔案', ncols=100)
        
        # 寫入精簡化 seq_index 檔案
        with open (workspace + '/index/seq_student_cls.csv', 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            
            # 遍歷所有學號
            for i in range(len(student_id_arr)):
                student_id = student_id_arr[i]
                student_all_class_list = []
                all_class_index = np.where(seq_index[:,:] == student_id)[0].tolist()
                
                # 遍歷所有課程id
                for j in range(len(all_class_index)):
                    student_all_class_list.append(seq_index[all_class_index[j]][1])
                student_all_class_list = np.sort(student_all_class_list)
                
                # 寫入檔案
                temp = []
                for j in range(len(student_all_class_list)):
                    temp.append([student_id, student_all_class_list[j]])
                writer.writerows(temp)
                
                # 更新進度條
                simple_process.update(1)