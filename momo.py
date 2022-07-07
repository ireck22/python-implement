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
    key2_length = len(key2)
    if key2_length > 0:
        key = urllib.parse.quote(key)  # url encode
    # ==============空格處理 end===========

    # 拿mobile版型的
    url = "https://m.momoshop.com.tw/search.momo?_advFirst=N&_advCp=N&curPage=1&searchType=&cateLevel=-1&ent=k&searchKeyword=" + \
        key+"&_advThreeHours=N&_isFuzzy=0&_imgSH=fourCardType"

    # 靜態爬取
    #====================開始爬取 start==========================
    result = []
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')
    content = soup.find_all('ul')  # 商品都在裡面
    for row in content:
        if row.find('div', class_='prdInfoWrap'):
            result_temp = {}
            prod = row.find_all('div', class_='prdInfoWrap')
            for row2 in prod:
                prdName = row2.find('h3').text  # 取文字
                prdName2 = prdName.split('\r\n')  # 商品名子
                if len(prdName2) == 2:
                    prdName3 = prdName2[1].strip()  # 商品名子去左右空白
                    if key2[1] in prdName3:
                        price = row2.find('b', class_='price').text  # 商品價格

                        result_temp = {
                            "name": prdName3,
                            "price": price,
                        }
                        result.append(result_temp)

    #=======================開始爬取 end=============================

    length = len(result)
    if length == 0:
        return ["沒有此商品"]

    df = pd.DataFrame(result)
    min_price = df.min()
    finish_result = {
        "平台": "MOMO",
        "商品名稱": min_price[0],
        "價格": int(min_price[1])
    }

    return finish_result
