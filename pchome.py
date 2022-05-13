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

    # ==============空格處理 start=========
    key2 = key.split(' ')
    length = len(key2)
    if length > 0:
        key = urllib.parse.quote(key)
    # ==============空格處理 start=========

    url = "https://ecshweb.pchome.com.tw/search/v3.3/all/results?q=" + \
        key+"&page=1&sort=sale/dc"

    # 靜態爬取
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')
    content = soup.find('p').text
    r2 = eval(content)  # 把字串型list轉成list
    length = len(r2)

    if length < 0:
        return "沒有此商品"

    # 放商品名稱和和價格
    result = {
        "平台:": "PCHOME",
        "商品名稱": r2['prods'][0]['name'],
        "價格": r2['prods'][0]['price']
    }

    return result
