'''
以上述 repository 為基礎
製作 sequence index 進行選課查詢
輸入學號可以輸出該學號所選的所有課程之課號
輸入課號可以輸出該課號選課的所有學生之學號
'''

import os
import csv
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
        return student_id_list
    
    def getCourseID(self):
        course_id_list = []
        with open(self.workspace + self.dir + self.filename, 'r', encoding='utf-8') as csvfile:
            rows = csv.reader(csvfile)
            for row in rows:
                if row[0][0] != '':
                    course_id_list.append(row[1])
        return course_id_list
    
    def getIndex(self, data):
        output = []
        for i in range(len(data)):
            output.append([data[i], self.blocknum + '_' + str(i)])
        return output

if __name__ == '__main__':
    # 程式資料夾工作區
    workspace = os.path.dirname(__file__).split('python')[0]
    dir = '\\raw_block\\'
    
    # 合併 Block 檔案，並產生 index
    raw_repo_dir = workspace + dir
    files = os.listdir(raw_repo_dir)
    create_block_process = tqdm(total=len(files), desc='合併 block 並產生 index', ncols=100)
    
    student_id_index = []
    course_id_index = []
    
    for i in range(len(files)):
        file = files[i]
        block = Block(dir, file)
        this_student_id_list = block.getStudentID()
        this_course_id_list = block.getCourseID()
        this_course_id_index = block.getIndex(this_course_id_list)
        this_student_id_index = block.getIndex(this_student_id_list)
        
        student_id_index += this_student_id_index
        course_id_index += this_course_id_index
        
        create_block_process.update(1)
    
    # 依照 key 排序
    student_id_index.sort(key = lambda student_id_index: student_id_index[0])
    course_id_index.sort(key = lambda course_id_index: course_id_index[0])
    
    # 輸出檔案
    with open(workspace + '.\index\seq_student_index.csv', 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(student_id_index)
    with open(workspace + '.\index\seq_course_index.csv', 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(course_id_index)