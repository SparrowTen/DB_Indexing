import os
import csv
import pprint
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
        raw_blocks = os.listdir(self.source)
        process = tqdm(total=len(raw_blocks), desc='key -> value', ncols=100)
        bucket = {}
        for raw_block in raw_blocks:
            with open(self.source + raw_block, 'r', encoding='utf-8') as csvfile:
                raw_repo = list(csv.reader(csvfile))
                own_value = []
                for key in key_set:
                    for row in raw_repo:
                        if key == row[key_col]:
                            own_value.append(row[0])
                    bucket[key] = own_value
            process.update(1)
        return bucket
    
    def hashfunc(self, key, key_set):
        return int(key) % len(key_set)
    
    def addHashIndex(self, key_value):
        blocks = {}
        key_set = list(key_value.keys())
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

def search(key, data):
    index = hash_index.hashfunc(key, key_set)
    return data[index]

def search(key, key_set, data):
    index = hash_index.hashfunc(key, key_set)
    if data[index]['key'] == key:
        return data[index]
    else:
        while True:
            if data[index]['key'] != key:
                if data[index]['pointer'] == None:
                    return None
                index = data[index]['pointer']
            else:
                return data[index]

if __name__ == '__main__':
    hash_index = HashIndex()
    if not os.path.exists(hash_index.workspace + '\\index\\' + 'hash_key.csv'):
        key_set = hash_index.getKeySet(key_col=1)
        with open(hash_index.workspace + '\\index\\' + 'hash_key.csv', 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for key in key_set:
                writer.writerow([key])
    if not os.path.exists(hash_index.workspace + '\\index\\' + 'hash_index.csv'):
        key_value = hash_index.addValue(key_set, key_col=1)
        blocks = hash_index.addHashIndex(key_value)
        with open(hash_index.workspace + '\\index\\' + 'hash_index.csv', 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for index in blocks:
                writer.writerow([index, blocks[index]['key'], blocks[index]['value'], blocks[index]['pointer']])
    
    key_set = []
    with open(hash_index.workspace + '\\index\\' + 'hash_key.csv', 'r', encoding='utf-8') as csvfile:
        data = csv.reader(csvfile)
        for row in data:
            key_set.append(row)
    
    with open(hash_index.workspace + '\\index\\' + 'hash_index.csv', 'r', encoding='utf-8') as csvfile:
        data = csv.reader(csvfile)
        print(search('2148', key_set, data))