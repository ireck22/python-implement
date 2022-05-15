#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
import sys
import json
import requests
from bs4 import BeautifulSoup
import lxml
import pandas as pd
import numpy as np
import time
import urllib.parse


def get_prods(key):

    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'
    }

    # ==============空格處理 start==================
    key2 = key.split(' ')
    length = len(key2)
    if length > 0:
        key = urllib.parse.quote(key)
    # ==============空格處理 end=====================

    url = "https://ecshweb.pchome.com.tw/search/v3.3/all/results?q=" + \
        key+"&page=1&sort=sale/dc"

    # 靜態爬取
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')
    content = soup.find('p').text
    content2 = eval(content)  # 把字串型list轉成list
    length = len(content2)

    # 沒有資料的話就會退出
    if length == 0:
        return "沒有此商品"

    # ===========整理資料拿出金額最小的 start===========
    df = pd.DataFrame(content2['prods'])
    content3 = df.min().to_dict()  # 找出最小的價格的商品資料轉字典
    # ===========整理資料拿出金額最小的 end=============

    # 放商品名稱和和價格
    result = {
        "平台:": "PCHOME",
        "商品名稱": content3['name'],
        "價格": content3['price']
    }

    return result
