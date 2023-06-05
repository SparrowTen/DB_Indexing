import csv
import os
import time

print ('請輸入學號：')
student_id = input()

start = time.process_time()
workspace = os.path.dirname(__file__).split('python')[0]
dir = '\\seq_index_block\\'

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
    with open (workspace + '\\raw_block\\block' + block + '.csv', 'r', encoding='utf-8') as csvfile:
        raw_repo = list(csv.reader(csvfile))
        print (raw_repo[int(row)])
end = time.process_time()

print ('執行時間：' + str(end - start) + ' 秒')
