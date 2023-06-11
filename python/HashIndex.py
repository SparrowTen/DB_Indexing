import os
import csv
import json
import sys
from pprint import pprint
from tqdm import tqdm

class HashBucket:
    def __init__(self, source='repository\\raw_block\\') -> None:
        self.workspace = os.path.dirname(__file__).split('python')[0]
        self.source = self.workspace + source
        self.dir = 'repository\\hash_index_block\\'
        if not os.path.exists(self.workspace + self.dir):
            os.makedirs(self.workspace + self.dir)
    
    def getKeySet(self, key_col=0):
        raw_blocks = os.listdir(self.source)
        process = tqdm(total=len(raw_blocks), desc='raw_block -> key_set', ncols=100)
        key_set = set()
        for raw_block in raw_blocks:
            with open(self.source + raw_block, 'r', encoding='utf-8') as csvfile:
                raw_repo = list(csv.reader(csvfile))
                for key in raw_repo[1:]:
                    key_set.add(key[key_col])
            process.update(1)
        return key_set
    
    def addValue(self, key_set, key_col=0):
        # 資料扁平化
        raw_blocks = os.listdir(self.source)
        process = tqdm(total=len(raw_blocks), desc='key -> value', ncols=100)
        bucket = {}
        for raw_block in raw_blocks:
            with open(self.source + raw_block, 'r', encoding='utf-8') as csvfile:
                raw_repo = list(csv.reader(csvfile))
                for key in key_set:
                    if bucket.get(key) == None:
                        own_value = []
                    else:
                        own_value = bucket[key]
                    
                    for row in raw_repo:
                        if key == row[key_col]:
                            own_value.append(row[0])
                    bucket[key] = own_value
            process.update(1)
        return bucket
    
    def hashfunc(self, key, hash_space):
        # load factor = 1, suggest 0.8
        return int(key) % hash_space
    
    def addHashIndex(self, key_value, hash_space):
        # 建立 hash index
        blocks = {}
        key_set = key_value.keys()
        process = tqdm(total=len(key_set), desc='key -> hash_index', ncols=100)
        for key in key_set:
            hash_index = self.hashfunc(key, hash_space)
            # key, value, pointer
            bucket = [key, key_value[key], None]
            if blocks.get(hash_index) != None:
                print('conflict')
                linked_index = self.fixConflict(hash_index, hash_space)
                blocks[hash_index][2] = linked_index
                blocks[linked_index] = bucket
            else: 
                blocks[hash_index] = bucket
            process.update(1)
        return blocks
    
    def fixConflict(self, index, hash_space):
        # 平行探測 [+-1, +-2, +-3, ...]
        # 線性探測 [1, 2, 3, ...]
        hash_indexs = []
        index = int(index)
        with open(self.workspace + '\\index\\' + 'hash_index.csv', 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                hash_indexs.append(str(row[0]))

        while True:
            index += 1
            if index >= hash_space:
                index = 0
            
            if str(index) not in hash_indexs:
                break
            
        with open(self.workspace + '\\index\\' + 'hash_index.csv', 'a', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([index])
        
        if index == '':
            print('hash index is full')
            
        
        return index
    
def getKeySet():
    key_set = []
    with open(hash_bucket.workspace + '\\index\\' + 'hash_key.csv', 'r', encoding='utf-8') as csvfile:
        data = csv.reader(csvfile)
        for row in data:
            key_set.append(row[0])
    return key_set

def search(key, key_set):
    index = str(hash_bucket.hashfunc(key, key_set))
    result = []
    while True:
        key = str(key)
        filename = f'block{index}.csv'
        with open(hash_bucket.workspace + hash_bucket.dir + filename) as csvfile:
            reader = csv.reader(csvfile)
            for bucket in reader:
                if bucket[0] == key:
                    result.append(bucket[1])
            if bucket[2] == '':
                return result
            else:
                index = bucket[2]

if __name__ == '__main__':
    hash_bucket = HashBucket()
    
    key_set = getKeySet()
    
    hash_space = len(key_set) * 6
    
    # 取得所有 key
    if not os.path.exists(hash_bucket.workspace + '\\index\\' + 'hash_key.csv'):
        key_set = hash_bucket.getKeySet(key_col=1)
        with open(hash_bucket.workspace + '\\index\\' + 'hash_key.csv', 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for key in key_set:
                writer.writerow([key])
    
    # 建立 hash_index_block
    if len(os.listdir(hash_bucket.workspace + hash_bucket.dir)) == 0:
        key_value = hash_bucket.addValue(key_set, key_col=1)
        blocks = hash_bucket.addHashIndex(key_value, hash_space)
        
        # 創建 bucket
        for index in blocks:
            filename = f'block{index}.csv'
            with open(hash_bucket.workspace + hash_bucket.dir + filename, 'w', encoding='utf-8', newline='') as csvfile:
                writer = csv.writer(csvfile)
                for value in blocks[index][1]:
                    writer.writerow([blocks[index][0], value, blocks[index][2]])
        
        # 創建 hash_index
        hash_indexs = []
        with open(hash_bucket.workspace + '\\index\\' + 'hash_index.csv', 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for index in blocks:
                hash_indexs.append(index)
                writer.writerow([index])
        
        # 分割 bucket 至資料限制大小
        size_limit = 8 * 1024
        buckets = os.listdir(hash_bucket.workspace + hash_bucket.dir)
        process = tqdm(total=len(buckets), desc='split bucket', ncols=100)
        
        for bucket in buckets:
            size = os.path.getsize(hash_bucket.workspace + hash_bucket.dir + bucket)
            if size > size_limit:
                # 讀取未分割的 bucket
                raw_bucket = []
                with open(hash_bucket.workspace + hash_bucket.dir + bucket, 'r', encoding='utf-8') as csvfile:
                    reader = csv.reader(csvfile)
                    for row in reader:
                        raw_bucket.append(row)
                
                index = bucket.split('.')[0].replace('block', '')
                insert_index = hash_bucket.fixConflict(index, hash_space)
                pointer = raw_bucket[0][2]
                
                # 刪除未分割的 bucket
                os.remove(hash_bucket.workspace + hash_bucket.dir + bucket)
                
                bucket = f'block{index}.csv'
                
                # 分割 bucket
                buffer = 0
                temp = []
                for row in raw_bucket:
                    buffer += len(str(row).encode('utf-8'))
                    if buffer > size_limit:
                        with open(hash_bucket.workspace + hash_bucket.dir + bucket, 'w', encoding='utf-8', newline='') as csvfile:
                            writer = csv.writer(csvfile)
                            for row in temp:
                                row[2] = insert_index
                                writer.writerow(row)
                        index = insert_index
                        insert_index = hash_bucket.fixConflict(index, hash_space)
                        buffer = 0
                        temp = []
                        bucket = f'block{index}.csv'
                        # print(bucket)
                    temp.append(row)
                
                with open(hash_bucket.workspace + hash_bucket.dir + bucket, 'w', encoding='utf-8', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    for row in temp:
                        row[2] = pointer
                        writer.writerow(row)
                
            process.update(1)
        
        print(f'load factor: {len(hash_indexs) / hash_space}')
        

    print('請輸入學號:')
    key = input()
    result = search(key, hash_space)
    print(result)
    print(f'共有 {len(result)} 選修此課程')