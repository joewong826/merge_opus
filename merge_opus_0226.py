#!/usr/bin/python
#-*- coding=utf-8 -*-

import os
import time


DIR_PATH = '/data2/goime/spider/NLM/NLM2_Portuguese_Brazil/corpus/HC+larbin+wget+OPUS+Subs2/OPUS/pt_br'
larger = 'OpenSubtitles2016.hy-pt_br.pt_br'
smaller = 'OpenSubtitles2016.af-pt_br.pt_br'


def compare_two(larger, smaller):
    with open(os.path.join(DIR_PATH, larger), 'r') as larger_file:
        larger_content = larger_file.read()
        with open(os.path.join(DIR_PATH, smaller), 'r') as smaller_file:
            keep_line_num = []
            i = 1
            while True:
                time1 = time.time()
                line = smaller_file.readline()
                if line == '':  # 因为OPUS文件没有空行
                    break
                print i
                time2 = time.time()
                last_pos = smaller_file.tell()
                theFollowing = line
                new_line = smaller_file.readline()
                theFollowing += new_line
                smaller_file.seek(last_pos)
                time3 = time.time()
                if theFollowing not in larger_content:
                    keep_line_num.append(i)
                time4 = time.time()
                print time2 - time1
                print time3 - time2
                print time4 - time3
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


keep = compare_two(larger, smaller)
delete_lines(smaller, keep)