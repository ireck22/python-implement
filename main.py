#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
import sys
import json
import requests
from bs4 import BeautifulSoup
import lxml
import pandas as pd
import numpy as np
import codecs
import re
import ssl
import time
import pchome
import momo
import shopee
import pymysql

key = input("請輸入要找的商品:")
finsih_result = []

# =======爬momo的商品 start===============
result_momo = momo.get_prods(key)
if len(result_momo) > 1:
    finsih_result.append(result_momo)
# =======爬momo的商品 end=================

# =======爬pchome的商品 start=============
result_pchome = pchome.get_prods(key)
if len(result_pchome) > 1:
    finsih_result.append(result_pchome)
# =======爬pchome的商品 end===============

# =======爬shopee的商品 start=============
result_shopee = shopee.get_prods(key)
if len(result_shopee) > 1:
    finsih_result.append(result_shopee)
# =======爬shopee的商品 end===============

df = pd.DataFrame(finsih_result)
finish = df.sort_values(by=['價格'])  # 價格小到大
finish.to_csv("比價.csv")

#連接sql
db_setting={
    "host": "127.0.0.1",
    "port": 3306,
    "user": "sa",
    "password": "abc123",
    "db": "parity",
    # "charset": "utf8mb4"
}

try:
    db=pymysql.connect(**db_setting)
    # print("資料庫連結成功")
    #使用cursor()方法創建一個游標對象cursor
    cursor=db.cursor()
    sql="insert into content(platform,prod_name,price)VALUES (%s,%s,%s)"

    for key,value in finish.iterrows():
        print(value.平台,value.商品名稱,value.價格)
        cursor.execute(sql,(value.平台,value.商品名稱,value.價格)) #執行sql語法
    
    db.commit()     #資料庫提交
        
except Exception as ex:
    print(ex)


print("sql 統整完")
db.close()      #資料庫關閉
print("end")
