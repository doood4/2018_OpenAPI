# -*- coding: utf-8 -*-
from urllib.request import urlopen, Request,unquote
from urllib.parse import urlencode, quote_plus
from bs4 import BeautifulSoup
import requests


decode_key = unquote('YwqDV590HcVx3fgfqBuuDeKB%2F8QsYQuRx2QYmJNnPU6MI99RlPoisyViCa%2B74IM5mX8OC3pe1N2922JS085wQg%3D%3D')

url = 'http://apis.data.go.kr/B551182/hospInfoService/getHospBasisList'
queryParams = '?' + urlencode({ quote_plus('ServiceKey') : decode_key,
                                quote_plus('pageNo') : '1', quote_plus('numOfRows') : '10',
                                quote_plus('sidoCd') : '110000', quote_plus('sgguCd') : '110019',quote_plus('emdongNm') : '신내동',
                                #quote_plus('zipCd') : '2010', quote_plus('clCd') : '11', quote_plus('dgsbjtCd') : '01'
                                 })

#request = Request(url + queryParams)
#request.get_method = lambda: 'GET'
#response_body = urlopen(request).read()
#print(response_body.decode('utf-8'))

r = requests.get(url + queryParams)
soup = BeautifulSoup(r.text,'html.parser')
#soup = BeautifulSoup(html,'lxml') # 더 빠르다는데?

#print(soup.decode("utf-8")) # 받아온 xml출력

mrr = soup.find_all("yadmnm")  # "" 카테고리 다 찾아서 list화
print(mrr)
for i in mrr:
    print(i.get_text()) # get_text() 해당 내용 문자열 반환
