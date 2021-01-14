# !/usr/bin/python3
# -*-coding:utf-8-*-
# Author: Liang Ma
# CreatedDate: 2021/1/7 19:15
# Description:

def rec_merge(d1, d2):
    """
    recursive merge dict d2 to dit d1, just like d1.update(d2)
    :param d1:
    :param d2:
    :return: d1:
    """
    for key, value in d2.items():
        if value:
            if key not in d1.keys():
                d1[key] = value
            else:
                if isinstance(value, dict):
                    rec_merge(d1[key], value)
                else:
                    d1[key] = value
    return d1


if __name__ == '__main__':
    d1 = {'a': {'a': 1, 'b': 2}}
    d2 = {'a': {'c': 3, 'b': 1}}
    c = rec_merge(d1, d2)
    print(c)
