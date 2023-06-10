import os
import csv
import json
from pprint import pprint
from tqdm import tqdm

class HashIndex:
    def __init__(self, source='repository\\raw_block\\') -> None:
        self.workspace = os.path.dirname(__file__).split('python')[0]
        self.source = self.workspace + source
        self.dir = '\\repository\\hash_index_block\\'
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
    
    def hashfunc(self, key, key_set):
        # load factor = 1, suggest 0.8
        return int(key) % len(key_set)
    
    def addHashIndex(self, key_value):
        blocks = {}
        key_set = key_value.keys()
        for key in key_set:
            hash_index = self.hashfunc(key, key_set)
            bucket = {}
            bucket['key'] = key
            bucket['value'] = key_value[key]
            bucket['pointer'] = None
            if blocks.get(hash_index) != None:
                linked_index = self.fixConflict(hash_index, blocks)
                blocks[hash_index]['pointer'] = linked_index
                blocks[linked_index] = bucket
            elif blocks.get(hash_index) == None:
                blocks[hash_index] = bucket
        return blocks
    
    def fixConflict(self, index, blocks:dict):
        # 平行探測 [+-1, +-2, +-3, ...]
        new_index = 1
        while True:
            if blocks.get(index + new_index) == None:
                index = index + new_index
                break
            if blocks.get(index - new_index) == None:
                index = index - new_index
                break
            index += 1
        return index
    
def getKeySet():
    key_set = []
    with open(hash_index.workspace + '\\index\\' + 'hash_key.csv', 'r', encoding='utf-8') as csvfile:
        data = csv.reader(csvfile)
        for row in data:
            key_set.append(row[0])
    return key_set

def search(key, key_set):
    index = str(hash_index.hashfunc(key, key_set))
    while True:
        key = str(key)
        filename = f'block{index}.json'
        with open(hash_index.workspace + hash_index.dir + filename) as jsonfile:
            bucket = json.load(jsonfile)
            if bucket['key'] == key:
                return bucket['value']
            elif bucket['pointer'] != None:
                index = bucket['pointer']
            else:
                return None

if __name__ == '__main__':
    hash_index = HashIndex()
    if not os.path.exists(hash_index.workspace + '\\index\\' + 'hash_key.csv'):
        key_set = hash_index.getKeySet(key_col=1)
        with open(hash_index.workspace + '\\index\\' + 'hash_key.csv', 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for key in key_set:
                writer.writerow([key])
    
    key_set = getKeySet()
    
    if not os.path.exists(hash_index.workspace + '\\index\\' + 'hash_index.csv'):
        key_value = hash_index.addValue(key_set, key_col=1)
        blocks = hash_index.addHashIndex(key_value)
        with open(hash_index.workspace + '\\index\\' + 'hash_index.csv', 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for index in blocks:
                writer.writerow([index, blocks[index]['key'], blocks[index]['value'], blocks[index]['pointer']])
        
        for index in blocks:
            filename = f'block{index}.json'
            with open(hash_index.workspace + hash_index.dir + filename, 'w', encoding='utf-8') as jsonfile:
                json.dump(blocks[index], jsonfile, indent=4, ensure_ascii=False)
    
    key = 2132
    
    result = search(key, key_set)
    print(result)
    print(f'共有 {len(result)} 選修此課程')