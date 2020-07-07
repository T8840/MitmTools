# -*- coding: utf-8 -*-
"""
    :author: T8840
    :tag: Thinking is a good thing!
          纸上得来终觉浅，绝知此事要躬行！
    :description: 用来统计埋点数据出现个数
"""

from pprint import pprint
def count(f):
    Count = {}
    with open(f,'r',encoding='utf-8') as file:
        for line in file.readlines():
            Count[line] = Count.get(line,1) +1
    pprint(Count)

count('./upload_record.txt')
count('./upload_record_type.txt')