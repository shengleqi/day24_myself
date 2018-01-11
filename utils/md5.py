# -*- coding: utf-8 -*-
__author__ = 'ShengLeQi'

import hashlib

def md5(text):
    m = hashlib.md5()
    m.update(text.encode('utf-8'))
    return m.hexdigest()


if __name__ == '__main__':
    text = "alex"
    v = md5(text)
    print(v)

print(md5("123456"))