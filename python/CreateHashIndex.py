import os
import csv
import pprint
from tqdm import tqdm

class HashIndex:
    def __init__(self, source='repository\\raw_block\\') -> None:
        self.workspace = os.path.dirname(__file__).split('python')[0]
        self.source = self.workspace + source
        self.dir = '\\repository\\hash_index_block\\'
    
    def getKeySet(self, key_col=0):
        raw_blocks = os.listdir(self.source)
        process = tqdm(total=len(raw_blocks), desc='從 raw_block 取得 keyset', ncols=100)
        key_set = set()
        for raw_block in raw_blocks:
            with open(self.source + raw_block, 'r', encoding='utf-8') as csvfile:
                raw_repo = list(csv.reader(csvfile))
                for key in raw_repo[1:]:
                    key_set.add(key[key_col])
            process.update(1)
        return key_set
    
    def getChunk(self, key_set, key_col=0):
        raw_blocks = os.listdir(self.source)
        process = tqdm(total=len(key_set) + len(raw_blocks), desc='從 raw_block 取得 chunks', ncols=100)
        chunks = {}
        for raw_block in raw_blocks:
            with open(self.source + raw_block, 'r', encoding='utf-8') as csvfile:
                raw_repo = list(csv.reader(csvfile))
                own_value = []
                for key in key_set:
                    for row in raw_repo:
                        if key == row[key_col]:
                            own_value.append(row)
                    chunks[key] = own_value
            process.update(1)
        return chunks
    
if __name__ == '__main__':
    hash_index = HashIndex()
    key_set = hash_index.getKeySet(key_col=1)
    chunks = hash_index.getChunk(key_set, key_col=1)
    pprint.pprint(chunks['2142'])