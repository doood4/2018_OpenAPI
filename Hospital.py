# -*- coding: utf-8 -*-
from urllib.request import urlopen, Request,unquote
from urllib.parse import urlencode, quote_plus
from bs4 import BeautifulSoup
import requests
from code_dictionary import *
from data_class import *

addr1 = '서울특별시'
addr2 = '양천구'
addr3 = ''
hos_type = ''

decode_key = unquote('YwqDV590HcVx3fgfqBuuDeKB%2F8QsYQuRx2QYmJNnPU6MI99RlPoisyViCa%2B74IM5mX8OC3pe1N2922JS085wQg%3D%3D')

url = 'http://apis.data.go.kr/B551182/hospInfoService/getHospBasisList'
queryParams = '?' + urlencode({ quote_plus('ServiceKey') : decode_key,
                                quote_plus('pageNo') : '1', quote_plus('numOfRows') : '5',
                                quote_plus('sidoCd') : sido_dict[addr1],
                                quote_plus('sgguCd') : gugun_dict[sido_dict[addr1]][addr2],
                                quote_plus('emdongNm') : addr3,
                                quote_plus('zipCd') : type1[hos_type],
                                # quote_plus('clCd') : '11',
                                #quote_plus('dgsbjtCd') : '14'
                                 })


r = requests.get(url + queryParams)
soup = BeautifulSoup(r.text,'lxml-xml')

## 받아온 data xml형식으로 출력
#print(soup.decode("utf-8")) # 받아온 xml출력

xml_data = soup.find_all("item")  # "" 카테고리 다 찾아서 list화

HOSPITAL = []
HOSPITAL = make_Mydatalist(xml_data)
for i in HOSPITAL:
    i.print()