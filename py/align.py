#!/usr/local/bin/python3
# -*- coding: UTF-8 -*- 
import re
import numpy as np
# 对齐函数，参数1：多行字符串，必须字符串相等的列。参数2：tab代表多少空格。参数3：需要在返回结果的首列加多少个tab
def align(str_many,ts_conut,ints):
    line_list_conut = [] 
    line_list = []
    for line in str_many.splitlines():                                          #提取字符单词并存入a数组
        line_list.append(re.findall('\S+',line))
    a = np.array(line_list,dtype=object)
    col_same = np.where(np.all(a == a[0,...],axis=0))                           #获取所有元素相同的列
    col_same = np.asarray(col_same,dtype=np.int8)
    if a.shape[1]-1 in col_same:
        a = np.insert(a,a.shape[1],'',axis=1)
    for col in col_same[0]:
        a[...,col+1] = a[...,col] + ' ' + a[...,col+1]               #合并到下一列 
    a = np.delete(a,col_same,axis=1)
    str_len=np.char.str_len(np.asarray(a,dtype=np.str))//ts_conut               #计算字符单词占用tas的个数
    a=np.asarray(a,dtype=[('strs','O'),('tab','O')])
    str_len=np.amax(str_len,axis=0)+1-str_len                                   #每个单词后面需要补多少个tas才对齐
    a['tab'] = str_len
    a['strs'] = a['strs'] + a['tab']*'\t'
    a['strs'][...,-1] =np.vectorize(lambda s: s[:-1])(a['strs'][...,-1])      #删除最后一列元素的最后一个字符:\t
    astr = a['strs']
    tstr = ints * '\t'
    astr = np.insert(astr,0,tstr,axis=1)
    astr = np.insert(astr,astr.shape[1],'\n',axis=1)
    astr = astr.reshape(-1)
    astr = np.delete(astr,-1)
    str_r = ''
    str_r = ''.join(str(i) for i in astr)
    return str_r
