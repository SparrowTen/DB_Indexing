'''
實作資料 repository:

將原始資料檔案以 block 為單位切割分別儲存
單一 block 最多只能存放一百筆選課資料或上限 8KB 的索引資料
DEMO 時不需要展示分割 repository 的程式
僅需說明 repository 產生的方式即可
'''

import os

if __name__ == '__main__':
    # 讀取原始資料
    raw_data_dir = os.path.dirname(__file__) + 'data'
    if not os.path.exists(raw_data_dir):
        print('沒有原始資料')
        os._exit(0)
    
    # 創建 repository 資料夾
    if not os.path.exists(raw_data_dir + '/repository'):
        os.mkdir(raw_data_dir + '/repository')
        