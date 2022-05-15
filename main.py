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
import ruten
import pchome
import momo

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

# print(finsih_result)
for i in finsih_result:
    print(i)
df = pd.DataFrame(finsih_result)
# finish=df.sort_values(by='價格') #價格小到大
df.to_csv("比價.csv")
print("end")
sys.exit()

# sorted(result3,key = lambda f: f[0],reverse = True)
# key2=key.split(' ')
# length=len(key2)
# if length>0:
#     key=key.replace(' ','+')

# url="https://www.ruten.com.tw/find/?q="+key

# options = Options()
# options.add_argument("--disable-notifications")
# driver = webdriver.Chrome('./chromedriver', chrome_options=options)    #讀取已經載好的chromedriver

# driver.maximize_window()
driver = webdriver.Chrome(
    ChromeDriverManager().install())  # 自動抓取最新的chromedriver
driver.get(url)

# ----------------------滾動卷軸到最下面 start----------------------
for i in range(1, 5):
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
time.sleep(1)
# ----------------------滾動卷軸到最下面 end----------------------

d = driver.page_source  # 把動態爬取的程式碼放到d
driver.quit()  # 關閉瀏覽器


soup = BeautifulSoup(d)
# print(soup)
content = soup.find_all('div')
i = 1
for row in content:
    # title=row.find('div',class_="rt-goods-list-item-name")
    # data=row.find('div',class_='spotlight-section-body').text
    data = row.find(
        'div', attrs={"class": ["search-result-container", "top-part"]}).text
    # data_a=data.find('a')['href']
    # data_txt=data_a.find('span').text
    # result=data.split(' ')
    print(data)
    break
    print(i)
    i += 1
    # if i==20:
    #     break

# ========抓兩頁的資料 start===========================
# for i in range(1, 3):
#     res = r.get("https://www.ptt.cc/bbs/Gossiping/index"+str(i)+".html")
#     soup = BeautifulSoup(res.text, 'lxml')

#     result = soup.find_all('div')                   # 先拿全部的div
#     main_url = 'https://www.ptt.cc/'                # 網址前頭設定
#     finish = []                                     # 放最後的結果

#     for row in result:
#         if row.find('div', class_='title'):          # div的class是title再進去
#             title = row.find('div', class_='title')  # 先篩選title
#             if title.find('a'):
#                 title2 = title.find('a').text        # 在進a裡拿文字
#                 href = title.find('a')['href']       # 拿href
#                 url = main_url+href                  # 還原網址

#                 # ======== 把文章裡的內文拿出來 start================
#                 res2 = r.get(url)
#                 soup2 = BeautifulSoup(res2.text, 'lxml')
#                 content = soup2.find('div', id='main-content').text
#                 content2 = content.split("--")[0]  # 不拿回應
#                 # ======== 把文章裡的內文拿出來 end================

#                 finish.append([title2, url, content2])  # 新增到陣列
# # ========抓兩頁的資料 start===========================

# # ========輸出csv start===============================
# rs = pd.DataFrame(finish, columns=['title', 'url', 'content'])
# rs.to_csv('content.csv')
# print("end")
# # ========輸出csv start===============================
