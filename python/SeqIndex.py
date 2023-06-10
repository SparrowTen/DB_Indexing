'''
以上述 repository 為基礎
製作 sequence index 進行選課查詢
輸入學號可以輸出該學號所選的所有課程之課號
輸入課號可以輸出該課號選課的所有學生之學號
'''

import os
import csv
import time
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

def searchbyStudentID():
    print ('請輸入學號：')
    student_id = input()

    start = time.process_time()
    workspace = os.path.dirname(__file__).split('python')[0]
    dir = '\\repository\\student_seq_index_block\\'

    blocks = os.listdir(workspace + dir)

    index_list = []
    for i in range(len(blocks)):
        block = blocks[i]
        with open (workspace + dir + '\\' + block, 'r', encoding='utf-8') as csvfile:
            seq_index = list(csv.reader(csvfile))
            for j in range(len(seq_index)):
                if seq_index[j][0] == student_id:
                    index_list.append(seq_index[j][1])
    
    for index in range(len(index_list)):
        block = index_list[index].split('_')[0]
        row = index_list[index].split('_')[1]
        with open (workspace + 'repository\\raw_block\\block' + block + '.csv', 'r', encoding='utf-8') as csvfile:
            raw_repo = list(csv.reader(csvfile))
            course_id = raw_repo[int(row)][1]
            course_name = raw_repo[int(row)][2]
            print (course_id + ' ' + course_name)
    print('共 ' + str(len(index_list)) + ' 門課程')
    
    end = time.process_time()
    print ('執行時間：' + str(end - start) + ' 秒')

def searchbyCourseID():
    print ('請輸入課號：')
    course_id = input()

    start = time.process_time()
    workspace = os.path.dirname(__file__).split('python')[0]
    dir = '\\repository\\course_seq_index_block\\'

    blocks = os.listdir(workspace + dir)

    index_list = []
    for i in range(len(blocks)):
        block = blocks[i]
        with open (workspace + dir + '\\' + block, 'r', encoding='utf-8') as csvfile:
            seq_index = list(csv.reader(csvfile))
            for j in range(len(seq_index)):
                if seq_index[j][0] == course_id:
                    index_list.append(seq_index[j][1])

    for index in range(len(index_list)):
        block = index_list[index].split('_')[0]
        row = index_list[index].split('_')[1]
        with open (workspace + 'repository\\raw_block\\block' + block + '.csv', 'r', encoding='utf-8') as csvfile:
            raw_repo = list(csv.reader(csvfile))
            student = raw_repo[int(row)][0]
            print(student)
    print('共 ' + str(len(index_list)) + ' 位學生選修此課程')
    
    end = time.process_time()
    print ('執行時間：' + str(end - start) + ' 秒')

if __name__ == '__main__':
    # 程式資料夾工作區
    workspace = os.path.dirname(__file__).split('python')[0]
    dir = '\\raw_block\\'
    
    if not os.path.exists(workspace + '.\\index\\seq_student_index.csv') and not os.path.exists(workspace + '.\\index\\seq_course_index.csv'):
        
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
        with open(workspace + '.\\index\\seq_student_index.csv', 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(student_id_index)
        with open(workspace + '.\\index\\seq_course_index.csv', 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(course_id_index)
    
    # 輸入學號可以輸出該學號所選的所有課程之課號
    searchbyStudentID()
    # 輸入課號可以輸出該課號選課的所有學生之學號
    searchbyCourseID()