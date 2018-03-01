#!/usr/bin/python
#-*- coding=utf-8 -*-

import os
import pdb
import time
from shutil import copyfile


def getFollowingTwo(lineNum, file):
    # lines = []
    lines = ''
    with open(file, 'r') as infile:
        for num, line in enumerate(infile, 1):
            if lineNum <= num <= lineNum + 2:
                lines += line.strip()
                # lines.append(line.strip())
    infile.close()
    return lines


def search2(followingTwo, final_file):
    with open(final_file, 'r') as fFile:
        contents = fFile.read()
        if followingTwo in contents:
            return False
    fFile.close()
    return True


def search(lookup, followingTwo, final_file):
    with open(final_file, 'r') as fFile:
        for num, line in enumerate(fFile, 1):
            if line.strip() == lookup:  # 第一句相同，找后面两句，与followingTwo对比
                keep = False
                largestFollowingTwo = getFollowingTwo(num, final_file)
                if len(largestFollowingTwo) < 3:
                    continue
                for sentenceA, sentenceB in zip(followingTwo, largestFollowingTwo):
                    if sentenceA != sentenceB:
                        keep = True
                if keep is False:
                    return False
    fFile.close()
    return True


def merge(dir_path):
    # dir_path = "C:\Users\huangziwen\PycharmProjects\untitled_27\OPUS"
    objects = os.listdir(dir_path)

    largest_name = ""
    largest_size = 0
    for item in objects:
        size = os.path.getsize(os.path.join(dir_path, item))
        if size > largest_size:
            largest_size = size
            largest_name = item

    objects.remove(largest_name)
    largest_name = os.path.join(dir_path, largest_name)
    final_name = os.path.join(dir_path, 'final.txt')
    copyfile(largest_name, final_name)

    with open(os.path.join(dir_path, 'log.txt'), 'a') as log_file:
        for item in objects:
            with open(final_name, 'a') as final_file:
                log_file.write(item+'\n')
                log_file.flush()
                this_file = os.path.join(dir_path, item)
                with open(this_file, 'r') as infile:
                    for lineNum, line in enumerate(infile, 1):
                        log_file.write(str(lineNum)+'\n')
                        log_file.flush()
                        if line.strip() == '':
                            continue
                        time1 = time.time()
                        followingTwo = getFollowingTwo(lineNum, this_file)
                        time2 = time.time()
                        keep = search2(followingTwo, final_name)
                        time3 = time.time()
                        if keep is True:
                            final_file.write(line+'\n')
                            final_file.flush()
                        time4 = time.time()
                        print time2 - time1
                        print time3 - time2
                        print time4 - time3
            final_file.close()


import sys
from optparse import OptionParser
def run(args):
    parser = OptionParser(usage="%prog -p DIRECTORY", version="%prog 1.0",
                          epilog=u'此工具用于将一个文件夹下的文件内容去重')
    parser.add_option("-p", "--path", dest="path", metavar="DIRECTORY", help=u'输入文件夹路径，路径有空格时必须用双引号')

    if len(args) <= 1:
        parser.print_help()
        return

    (opt, args) = parser.parse_args(args)
    # import pdb;pdb.set_trace()
    if not opt.path:
        print('error: option(s) missing..')
        sys.exit()
    if not os.path.isdir(opt.path):
        print('error: no input directory')
        sys.exit()

    merge(opt.path)


if __name__ == '__main__':
    run(sys.argv)
    # dir_path = "C:\Users\huangziwen\PycharmProjects\untitled_27\OPUS"
    # merge(dir_path)