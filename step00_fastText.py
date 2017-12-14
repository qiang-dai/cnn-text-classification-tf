import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt
import re
from tqdm import tqdm
import time
import os,sys
from collections import Counter
import codecs
import pyIO
import datetime

def get_file_list(file_dir):
    filename_list = []

    if os.path.isfile(file_dir):
        filename_list.append(file_dir)
    else:
        filename_list,_ = pyIO.traversalDir(file_dir)

    filename_list = [e for e in filename_list if e.find('DS_Store') == -1]
    return filename_list

def get_all_list(file_dir, threshold_line_cnt):
    filename_list = get_file_list(file_dir)

    total_list = []
    for index,filename in enumerate(filename_list):
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), index, filename)
        c_list = pyIO.get_content(filename)
        total_list.extend(c_list)

        ###threshold_line_cnt limit
        if len(total_list) > threshold_line_cnt:
            total_list = total_list[:threshold_line_cnt]
            break
    print('len(total_list):', len(total_list))
    return total_list

if __name__ == '__main__':
    threshold_line_cnt = 200*10000
    if len(sys.argv) > 1:
        threshold_line_cnt = int(sys.argv[1])

    dir_list = [
        '/Users/xinmei365/untitled/raw_data/dir_keras',
        '/Users/xinmei365/untitled/raw_data/dir_kika',
        '/Users/xinmei365/untitled/raw_data/dir_news',
        '/Users/xinmei365/untitled/raw_data/dir_twitter',
    ]

    new_list = []
    for i,file_dir in enumerate(dir_list):
        res_list = get_all_list(file_dir, threshold_line_cnt)
        label = '__label__%d , '%i
        for res in res_list:
            tmp = label + res
            #tmp = tmp.replace('"', '')
            new_list.append(tmp)

    dst_filename = '/Users/xinmei365/untitled/raw_data/all.txt'
    pyIO.save_to_file('\n'.join(new_list), dst_filename)




