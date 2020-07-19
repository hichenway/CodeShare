# Author：hichenway
# 该脚本包括了常用的文件或数据处理的功能函数,方便查找和应用，减少重复造轮子

import os
import time


# 时间计算装饰器
def deco_time(is_deco = True):
    # 可通过 is_deco 参数去设置是否使用该装饰器
    if is_deco:
        def _deco_time(func):
            def time_spent(*args, **kwargs):
                start_time = time.time()
                result = func(*args, **kwargs)
                end_time = time.time()
                spent_time = (end_time - start_time) * 1000
                print("The spend time is: %f ms"%spent_time)    # 这里也可以通过日志去记录
                return result
            return time_spent
    else:
        def _deco_time(func):
            return func
    return _deco_time


# 装饰器测试用例
class Test:
    @deco_time(True)
    def test1(self, n):
        sum_num = 0
        for i in range(n):
            sum_num += 1
        return sum_num


def set_seed(args):
    """
    随机数种子设置，保证实验可重复性
    :param args:
    :return:
    """
    import random
    import numpy as np
    import torch
    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    if args.n_gpu > 0:
        torch.cuda.manual_seed_all(args.seed)


import time
# 另一个计时装饰器
def timing(f):
    """Decorator for timing functions
    Usage:
    @timing
    def function(a):
        pass
    """
    def wrapper(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        end = time.time()
        print('function:%r took: %2.2f sec' % (f.__name__,  end - start))
        return result
    return wrapper


# 把一个文件夹下的所有文件移到另一个文件夹下
import shutil
def move_file(file_path, to_path):
    '''
    :param file_path: 要移动的文件路径
    :param to_path: 要移动到的文件路径
    :return: None
    '''
    file_list = os.listdir(file_path)
    for file_name in file_list:
        file = file_path + "/" + file_name
        shutil.move(file, to_path)


# 在保存文件时加上当前时间
def file_add_time(file_name):
    cur_time = time.strftime("%Y-%m-%d_%H_%M", time.localtime())
    name, form = file_name.split('.')
    return '.'.join([name+cur_time,form])


def plot_text_length(data):
    """
    输出文本列表的长度直方图，方便分析和取padding 的 max_length
    :param data: 文本数据列表，如：["我想吃饭"，"我想吃东西"...]
    :return:
    """
    import matplotlib.pyplot as plt
    from collections import Counter
    data_len = [len(sentence) for sentence in data]
    len_dict = Counter(data_len)
    X = list(len_dict.keys())
    Y = list(len_dict.values())
    plt.bar(X, Y)
    plt.show()


# 删除句末的符号
# string 还有很多格式形式，参见: https://docs.python.org/2/library/string.html
# string.printable 代表 '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c'
# string.printable 没有中文符号
import string
symbol = "，。、！（）,./!~·`"       # 要去除的句尾标点，不包括问号，可加上
def drop_symbol(seq):
    seq = seq.strip()
    seq = seq.rstrip(symbol)
    seq = seq.rstrip(string.printable)
    return seq


# 删除两个特定字符之间的内容，比如微博话题：#新冠疫情#， 一般可以用于文本的清洗
# 这两个特定的字符不限于单个字符，像这样的也可以：-->
# 不同模式匹配下的示例："#除夕夜#万家灯火通明鞭炮齐鸣也是极好的#春节放鞭炮#"，start_char和 end_char都是 '#'
# 最大模式是贪婪匹配，会匹配整句，最小模式下仅匹配：#除夕夜#
def delete_special_two_chars_inner(start_char, end_char, content):
    import re
    # 最大模式匹配：
    pattern = re.compile(r'({})(.*)({})'.format(start_char, end_char))

    # 最小模式匹配：
    # pattern = re.compile(r'({})(.*?)({})'.format(start_char, end_char))

    return pattern.sub(r'', content, count=1)    #这里的count还可以设置替换次数

    # 如果想保留start_char和end_char，则用：
    # return pattern.sub(r'{}{}'.format(start_char, end_char),content)


# 文本清理函数
def clean_function(seq):
    import re
    # 去除超链接
    pattern_url = re.compile(r'http://[a-zA-Z0-9.?/&=:]*',re.S)
    seq = pattern_url.sub(r'',seq)

    # 去除空格
    seq = seq.replace(" ", "")
    return seq


if __name__ == "__main__":
    file_name = "file.csv"
    new_fime_name = file_add_time(file_name)

    a=Test()
    sum_num = a.test1(10000)
    print(sum_num)

    test = "【史上最强悍促销】闹得沸沸扬扬"
    print(delete_special_two_chars_inner('【', '】',test))