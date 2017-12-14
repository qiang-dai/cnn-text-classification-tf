import numpy as np
import re
import itertools
from collections import Counter
import pyIO
import os
import datetime

def clean_str(string):
    """
    Tokenization/string cleaning for all datasets except for SST.
    Original taken from https://github.com/yoonkim/CNN_sentence/blob/master/process_data.py
    """
    string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
    string = re.sub(r"\'s", " \'s", string)
    string = re.sub(r"\'ve", " \'ve", string)
    string = re.sub(r"n\'t", " n\'t", string)
    string = re.sub(r"\'re", " \'re", string)
    string = re.sub(r"\'d", " \'d", string)
    string = re.sub(r"\'ll", " \'ll", string)
    string = re.sub(r",", " , ", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"\(", " \( ", string)
    string = re.sub(r"\)", " \) ", string)
    string = re.sub(r"\?", " \? ", string)
    string = re.sub(r"\s{2,}", " ", string)
    return string.strip().lower()

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

        for c in c_list:
            tmp_list = c.split(' ')
            ###按32进行切分
            for i,e in enumerate(tmp_list):
                tmp = tmp_list[i*32:(i+1)*32]
                total_list.append(' '.join(tmp))
                if (i+1)*32 >= len(tmp_list):
                    break

        ###threshold_line_cnt limit
        if len(total_list) > threshold_line_cnt:
            total_list = total_list[:threshold_line_cnt]
            break
    print('len(total_list):', len(total_list))
    return total_list

def load_data_and_labels(dir_list, label_size, max_pos, threshold_line_cnt):
    dir_list.sort()

    label_list = []
    data_list = []
    for i, file_dir in enumerate(dir_list):
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), i, file_dir)
        total_list = get_all_list(file_dir, threshold_line_cnt)

        label = [0 for _ in range(label_size)]
        if max_pos >= 0:
            label[max_pos] = 1
        else:
            label[i] = 1

        for data in total_list:
            label_list.append(label)
            data_list.append(data)
        print('label_list[:3]:', label_list[-3:])
        print('data_list[:3]:', data_list[-3:])
    return data_list, np.array(label_list)

    """
    Loads MR polarity data from files, splits the data into words and generates labels.
    Returns split sentences and labels.
    """
    # Load data from files
    #positive_examples = list(open(positive_data_file, "r").readlines())
    # positive_examples = pyIO.get_content(positive_data_file)
    # positive_examples = [s.strip() for s in positive_examples]
    #
    # #negative_examples = list(open(negative_data_file, "r").readlines())
    # negative_examples = pyIO.get_content(negative_data_file)
    # negative_examples = [s.strip() for s in negative_examples]
    #
    # glove_examples = pyIO.get_content("/Users/xinmei365/cnn-text-classification-tf/data/rt-polaritydata/1000.glov")
    # glove_examples = [s.strip() for s in glove_examples]
    #
    # print(positive_examples[:3])
    # print(negative_examples[:3])
    # print(glove_examples[:3])
    #
    # # Split by words
    # x_text = positive_examples + negative_examples + glove_examples
    # x_text = [clean_str(sent) for sent in x_text]
    # # Generate labels
    # positive_labels = [[0, 1, 0] for _ in positive_examples]#2
    # negative_labels = [[1, 0, 0] for _ in negative_examples]#1
    # glove_labels    = [[0, 0, 1] for _ in glove_examples]#0
    # y = np.concatenate([positive_labels, negative_labels, glove_labels], 0)
    # return [x_text, y]


def batch_iter(data, batch_size, num_epochs, shuffle=True):
    """
    Generates a batch iterator for a dataset.
    """
    data = np.array(data)
    data_size = len(data)
    num_batches_per_epoch = int((len(data)-1)/batch_size) + 1
    for epoch in range(num_epochs):
        # Shuffle the data at each epoch
        if shuffle:
            shuffle_indices = np.random.permutation(np.arange(data_size))
            shuffled_data = data[shuffle_indices]
        else:
            shuffled_data = data
        for batch_num in range(num_batches_per_epoch):
            start_index = batch_num * batch_size
            end_index = min((batch_num + 1) * batch_size, data_size)
            yield shuffled_data[start_index:end_index]
