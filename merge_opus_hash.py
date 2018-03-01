#!/usr/bin/python
#-*- coding=utf-8 -*-

import os
import time
import datetime
import numpy as np


DIR_PATH = '/data2/goime/spider/NLM/NLM2_Vietnamese/corpus/HC+larbin+wgets+Subs2+OPUS/OPUS/vi'
larger = 'OpenSubtitles2018.en-vi.vi'
smaller = 'OpenSubtitles2018.es-vi.vi'
logfile = open(os.path.join(DIR_PATH, 'log.txt'), 'w')


def compare_two(larger, smaller):
    with open(os.path.join(DIR_PATH, larger), 'r') as larger_file:
        lines = larger_file.readlines()
        length = len(lines)
        hashing_lines = map(hash, lines)
        hashing_lines = np.array(hashing_lines)
        with open(os.path.join(DIR_PATH, smaller), 'r') as smaller_file:
            keep_line_num = []
            i = 1
            start_time = datetime.datetime.now()
            while True:
                # time1 = time.time()
                if i % 1000 == 0:
                    now_time = datetime.datetime.now()
                    delta = now_time-start_time
                    start_time = datetime.datetime.now()
                    logfile.write(str(i)+'/'+str(length)+'  '+str(delta.seconds/60)+'  '+str(delta.seconds%60)+'\n')
                    logfile.flush()
                line = smaller_file.readline()
                if line == '':  # 因为OPUS文件没有空行
                    break
                # print i
                # time2 = time.time()
                thislineshash = hash(line)
                # time3 = time.time()
                if thislineshash not in hashing_lines:
                    keep_line_num.append(i)
                else:
                    # print 'inside'
                    occurences = np.where(hashing_lines == thislineshash)[0]
                    last_pos = smaller_file.tell()
                    new_line = smaller_file.readline()
                    smaller_file.seek(last_pos)
                    next_lines = []
                    for oc in occurences:
                        next_lines.append(lines[oc+1])
                    if new_line not in next_lines:
                        keep_line_num.append(i)
                # time4 = time.time()
                # print time2 - time1
                # print time3 - time2
                # print time4 - time3
                i += 1
        smaller_file.close()
    larger_file.close()
    return keep_line_num


def delete_lines(filename, keep_line_num):
    contents = ''
    with open(os.path.join(DIR_PATH, filename), 'r') as in_file:
        for num, line in enumerate(in_file, 1):
            if num in keep_line_num:
                contents += line
    in_file.close()
    os.remove(os.path.join(DIR_PATH, filename))
    with open(os.path.join(DIR_PATH, filename), 'w') as new_file:
        new_file.write(contents)
    new_file.close()


time1 = datetime.datetime.now()
keep = compare_two(larger, smaller)
delete_lines(smaller, keep)
time2 = datetime.datetime.now()
delta = time2-time1
logfile.write(str(delta.seconds/60))
logfile.flush()