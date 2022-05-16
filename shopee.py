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
import ast


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

    # url = "https://shopee.tw/search?keyword="+key
    url = "https://shopee.tw/api/v4/search/search_items?by=relevancy&keyword="+key + \
        "&limit=10&newest=0&order=asc&page_type=search&scenario=PAGE_GLOBAL_SEARCH&version=2"

    # 靜態爬取
    result = []
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')
    content = soup.find('p').text  # 商品都在裡面
    content2 = json.loads(content)

    length = len(content2['items'])
    if length == 0:
        return ["沒有此商品"]

    # ==============整理爬下來的資料 start===========
    result = []
    for row in content2['items']:
        item_name = row['item_basic']['name']            # 商品名子
        item_price = row['item_basic']['price']          # 商品直購價
        item_price_min = row['item_basic']['price_min']  # 商品最低價格
        item_price_max = row['item_basic']['price_max']  # 商品最高價格

        x = 0
        for d in key2:
            if d in item_name:
                x += 1

        if x == key2_length:
            result.append({
                "name": item_name,
                "price": item_price,
                "price_min": item_price_min,
                "price_max": item_price_max,
            })
    # ==============整理爬下來的資料 end===========
    if len(result)==0:
        return ["沒有此商品"]
    
    # ===========找出最低價格的key值 start===========
    df = pd.DataFrame(result)
    min_price = df['price'].min()
    for key, value in df['price'].items():
        if value == min_price:
            min_key = key
            break
    # ===========找出最低價格的key值 end============

    # ===========整理價格 start=====================
    price = min_price/100000
    # ===========整理價格 end=======================

    finish_result = {
        "平台": "SHOPEE",
        "商品名稱": df['name'][min_key],
        "價格": int(price)
    }

    return finish_result
