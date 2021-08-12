# -*- coding:utf-8 -*-

import os
import datetime
import csv
import json
import pandas as pd
import click
import re
import time


# 获取命令行参数
@click.command()
@click.option('--src', prompt='请输入想要转换的文件路径')
@click.option('--dest', prompt='请输入转换输出路径')
# @click.option('--isdir', type=click.BOOL, prompt='是否文件目录')
def hello(src, dest):
    if src == "" or dest == "":
        print("文件路径不能为空")
        return

    if bool(1 - file_exist(src)) or bool(1 - file_exist(dest)):
        print("文件路径不存在，请重新输入...")
        return

    # if isdir != True and isdir != False:
    #    print("isDir输入错误， 请重新输入...")
    rootdir, dir_list, names = read_file(src)
    if len(dir_list) == 0 and len(names) == 0:
        output("目录%s啥也没有 0.0" % rootdir)
        return

    e, f, g = read_file(dest)
    if len(f) != 0 or len(g) != 0:
        h = input("目标路径不为空，是否继续进行(True or False):")
        if h == "False":
            return
    start = datetime.datetime.now()
    click.echo("正在进行文件格式转换...")
    # exp: src = "/root"
    # exp: dest = "/data"

    if len(dir_list) != 0:
        # exp: "/root", "['2020','2021']", ["xxx", "xxx"]"
        for i in dir_list:
            a, b, c = read_file(rootdir + "/" + i)
            if len(c) == 0:
                r = rootdir + "/" + i
                print("目录%s为空, 已跳过" % r)
                break
            # exp: aggregate("root", "2020", "/data")
            directory(rootdir, i, dest)
    if len(names) != 0:
        for i in names:
            single_file(rootdir, i, dest)
    end = datetime.datetime.now()
    print("本次转换结束，共耗时: %.3fs" % (end - start).total_seconds())


def output(text):
    screen_width = 150
    txt_width = len(text) + 12
    box_width = 3
    left_margin = (screen_width - txt_width) // 2
    print()
    print(' ' * left_margin + '+' + '-' * (txt_width) + '+')
    print(' ' * left_margin + '|' + ' ' * (txt_width) + '|')
    print(' ' * left_margin + '|' + ' ' * (box_width) + text + ' ' * (box_width) + '|')
    print(' ' * left_margin + '|' + ' ' * (txt_width) + '|')
    print(' ' * left_margin + '+' + '-' * (txt_width) + '+')
    print()


# 获取目标文件的父目录格式
def get_time(time):
    return str.split(time, "_")[0]


def GetKey(path):
    j = open(path, "r", errors="ignore")
    l = []
    for i in j.readlines():
        data = json.loads(i)
        l.append(list(data.keys()))
    j.close()
    return l


# key的并集
def AndSet(li):
    u = []
    for index in range(len(li)):
        u = list(set(u).union(set(li[index])))
    return u


# 获取每行key集合相对于key并集的差集，返回缺失元素集合的大集合
def Difference_set(and_set, complete_set):
    m = []
    for i in complete_set:
        a = list(set(and_set).difference(set(i)))
        m.append(a)

    return m


def Sort(dic):
    k = {}
    for i in sorted(dic.keys()):
        k[i] = dic[i]
    return k


# 获取转换后的csv文件格式
def get_csvfilename(x):
    return str.split(x, ".")[0]


# 确认文件存在
def file_exist(path):
    if os.path.exists(path):
        return True
    else:
        return False


# 读取目录下的文件以及子目录
def read_file(s):
    for rootdir, dirs, names in os.walk(s):
        return rootdir, dirs, names


# 判断目标目录是否存在
def create_path(time, dest):
    t = dest + "/" + time
    if os.path.exists(t):
        return t
    os.mkdir(t)
    return t


def fetch(file_path):
    # 获取json文件每行数据的key集的大集合
    key = GetKey(file_path)
    # 获取该json文件的key并集
    x = AndSet(key)
    # print(len(x))
    # 获取每行数据的key集合与整个文件key并集的差集合
    b = Difference_set(x, key)
    # print(b)
    return AndSet(b)


def directory(rootdir, dir, dest_path):
    file_path = create_path(dir, dest_path)
    # exp: file_path = "/data/2020"
    # exp: filename = "/data/2020/2020.csv"
    # 读取子目录json文件
    a, b, c = read_file(rootdir + "/" + dir)
    # exp: a, b, c = read_file("/root/2020")
    # exp: c = ["1.json", "2.json"]
    for i in c:
        csvfile = file_path + "/" + get_csvfilename(i) + ".csv"
        j = open(a + "/" + i, "r", errors="ignore")
        # exp: j = open("root/2020/1.json")
        y = fetch(a + "/" + i)
        # print(y)
        c = open(csvfile, "w")
        # exp: c = open("/data/2020/2020.csv")
        writer = csv.writer(c)
        # 创建bool类型变量，避免多次写入表头
        boo = True
        for i in j.readlines():
            if boo:
                data = json.loads(i)
                for x in y:
                    if x not in data.keys():
                        data[x] = ""
                k = {}
                for i in sorted(data.keys()):
                    k[i] = data[i]
                # 获取表头并写入
                l = list(k.keys())
                '''
                # 用下划线替换字段名的非（字母数字下划线）字符
                m = []
                for s in l:
                    r = re.sub('[\W_]', '_', s)
                    m.append(r)
                '''
                writer.writerow(l)
                # 获取字段value并写入
                n = list(k.values())
                writer.writerow(n)
                boo = False
            else:
                data = json.loads(i)
                for x in y:
                    if x not in data.keys():
                        data[x] = ""
                k = {}
                for i in sorted(data.keys()):
                    k[i] = data[i]
                n = list(k.values())
                writer.writerow(n)
        j.close()
        c.close()
        '''
        ################################################
        # 仅转csv时可去掉下面一段
        d = pd.read_csv(csvfile)
        # 新建一个字段，并将时间转化为时间戳
        tm = d["SubmittedDate"]
        m = []
        for i in tm:
            t = str.split(i, "T")
            ti = t[0] + " " + t[1]
            timeArray = time.strptime(ti, "%Y-%m-%d %H:%M:%S")
            x = time.mktime(timeArray)
            m.append(x)
        d["time"] = m
        d.to_csv(csvfile, index=False)
        #################################################
        '''
    print("目录%s已转换完成" % dir)


def single_file(rootdir, file, dest):
    file_path = rootdir + "/" + file
    # exp: file_path = "/data/2020.json"
    csvfile = dest + "/" + get_csvfilename(file) + ".csv"
    # exp: csvfile = "/data/2020.csv"
    j = open(file_path, "r", errors="ignore")
    # exp: j = open("root/2020.json")
    # 返回所有差集合的并集，也就是可能会在某行缺失的字段
    y = fetch(file_path)
    # print(y)
    c = open(csvfile, "w")
    # exp: c = open("/data/2020.csv")
    writer = csv.writer(c)
    # 创建bool类型变量，避免多次写入表头
    boo = True
    for i in j.readlines():
        if boo:
            data = json.loads(i)
            for x in y:
                if x not in data.keys():
                    data[x] = ""
            k = {}
            for i in sorted(data.keys()):
                k[i] = data[i]
            # 获取表头并写入
            l = list(k.keys())
            '''
                # 用下划线替换字段名的非（字母数字下划线）字符
                m = []
                for s in l:
                    r = re.sub('[\W_]', '_', s)
                    m.append(r)
            '''
            writer.writerow(l)
            # 获取字段value并写入
            n = list(k.values())
            writer.writerow(n)
            boo = False
        else:
            data = json.loads(i)
            for x in y:
                if x not in data.keys():
                    data[x] = ""
            k = {}
            for i in sorted(data.keys()):
                k[i] = data[i]
            n = list(k.values())
            writer.writerow(n)
    j.close()
    c.close()
    '''
    # 仅转csv时可去掉下面一段
        ################################################
        
        d = pd.read_csv(csvfile)
        # 新建一个字段，并将时间转化为时间戳
        tm = d["SubmittedDate"]
        m = []
        for i in tm:
            t = str.split(i, "T")
            ti = t[0] + " " + t[1]
            timeArray = time.strptime(ti, "%Y-%m-%d %H:%M:%S")
            x = time.mktime(timeArray)
            m.append(x)
        d["time"] = m
        d.to_csv(csvfile, index=False)
        #################################################
    '''
    print("文件%s已转换完成" % file_path)


if __name__ == "__main__":
    hello()