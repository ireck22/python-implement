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

# print(finsih_result)
# for i in finsih_result:
    # print(i)

df = pd.DataFrame(finsih_result)
finish=df.sort_values(by=['價格']) #價格小到大
finish.to_csv("比價.csv")
print("end")