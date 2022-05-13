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

    # url = "https://www.momoshop.com.tw/search/searchShop.jsp?keyword=" + \
        # key+"&searchType=1&curPage=1&_isFuzzy=0&showType=chessboardType"
    # mobile
    url = "https://m.momoshop.com.tw/search.momo?_advFirst=N&_advCp=N&curPage=1&searchType=&cateLevel=-1&ent=k&searchKeyword=" + \
        key+"&_advThreeHours=N&_isFuzzy=0&_imgSH=fourCardType"

    result = []
    # 靜態爬取
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')
    # content = soup.find_all('article',class_="prdListArea")
    content = soup.find_all('ul')
    # return content
    for row in content:
        if row.find('div', class_='prdInfoWrap'):
            result_temp = {}
            prod = row.find_all('div', class_='prdInfoWrap')
            # prdName=prod.find('h3',class_='prdName').text
            for row2 in prod:
                prdName = row2.find('h3').text
                prdName2 = prdName.split('\r\n')
                prdName3 = prdName2[1].strip()
                price = row2.find('b', class_='price').text

                result_temp = {
                    "name": prdName3,
                    "price": price,
                }
                # print(result_temp)
                result.append(result_temp)
    length = len(result)
    if length < 0:
        return "沒有此商品"
    df = pd.DataFrame(result)
    # print(df.sort_values(by='price'))  #價格小到大
    min_price = df.min()
    finish_result = {
        "平台": "MOMO",
        "商品名稱": min_price[0],
        "價格": min_price[1]
    }
    return finish_result
    r2 = eval(content)  # 把字串型list轉成list
    length = len(r2)

    if length < 0:
        return "沒有此商品"

    # 放商品名稱和和價格
    result = {"平台:": "PCHOME",
              "商品名稱": r2['prods'][0]['name'],
              "價格": r2['prods'][0]['price']
              }

    return result


# result = get_prods("jump force")

# df=pd.DataFrame(result)
# # print(df.sort_values(by='price'))  #價格小到大
# min_price=df.min()
# print(min_price)
