# -*- coding: utf-8 -*-

import sys
import chardet
from util import is_chinese

''' 
    循环
        1.如果第一行有字,

        2.第二行是空行.

        2.a第三行不是空行，
            .a第一行结尾不是标点符号
                则第一行的尾部空格或者换行符应该取消
                第二行应该删除，第三行(去掉开头空格)传给下一步
            .b第一行结尾是标点符号
                第一行原封保存，第二行原封保存，第三行传给下一步

        2.b第三行是空行，则第一行保存，第二行保存。后续寻找非空行。寻找不到，就是文件末尾
        3.将所得行作为第一行，回到步骤1
    情况二
        2.第二行不是空行.
            .a第一行是标点符号结尾，原封保存
            .b第一行结尾不是标点符号，去除换行符
        3.将第二行创给步骤1
    跳出循环
    '''
'''
    Q1.如何判断一行是一行，而不是非正常截断
        1.末尾是中文。并且该行不是标题。
            标题判断：TODO
                1.前面大片空格。去掉后，该行不为空
                2.包含特殊符号格式。比如（1或一）或者第×章
'''
def change(filepath):
    f = open(filepath, 'r', encoding=testDecode(filepath))
    fnew = open(filepath[:-4] + '_new.txt', 'w+', encoding="utf-8")  # 将结果存入新的文本中
    fristLine = None
    secondLine = ""
    tempLine = ""


    while True:
        if not fristLine:#fristline为空则读取
            fristLine = f.readline()

        if not fristLine:
            break

        newLine = fristLine.strip()
        # print(newLine)
        if len(newLine) != 0:#第一行有字
            secondLine = f.readline()

            if len(secondLine.strip()) != 0:#第二行非空，使用情况2
                if (not is_chinese(newLine[-1])):  # 末尾不是中文
                    fnew.write(fristLine)
                else:  # 末尾是中文
                    fnew.write(fristLine.rstrip())
                fristLine = secondLine #第二行传给第一行
                continue
            tempLine = f.readline()
            temp = tempLine.strip()
            if len(temp) != 0:#第三行不是空
                if(not is_chinese(newLine[-1])):  # 末尾不是中文
                    fnew.write(fristLine.rstrip())  # 保存第一行
                    fnew.write(secondLine)  # 保存空行
                    fristLine = tempLine
                    continue
                else:#末尾是中文
                    fnew.write(fristLine.rstrip())# 保存第一行
                    fristLine = tempLine.lstrip()
                # print(fristLine)
            else:  #第三行是空
                fnew.write(fristLine)  # 保存第一行
                fnew.write(secondLine)  # 保存第二行
                tempLine = f.readline()
                # print(fristLine)
                while len(tempLine.strip()) == 0:#寻找非空的行
                    tempLine = f.readline()
                    if not tempLine:
                        break
                fristLine = tempLine
        else:  # 第一行为空，重读
            fristLine = f.readline()
    f.close()
    fnew.close()
def testcChinese():
    for str in "我1.。a":  # 只有“我”是true
        print("%s is chinese:%r"%(str,is_chinese(str)))
    pass
def testDecode(filepath):
    tt = open(filepath, 'rb')
    ff = tt.read(200)  # 这里试着换成read(5)也可以，但是换成readlines()后报错
    enc = chardet.detect(ff)
    tt.close()
    print("可信度:%d 编码:%s 语言:%s" % (enc["confidence"], enc['encoding'], enc["language"]))
    ret = enc['encoding']
    if ret.upper() == "gb2312".upper():
        ret = "gbk"
    return ret

if __name__ == '__main__':
    file = u"/home/torahli/下载/ceshi.txt"
    change(file)
    # print(testDecode(file))
    # testcChinese()
