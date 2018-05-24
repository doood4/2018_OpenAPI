# -*- coding: utf-8 -*-
from urllib.request import urlopen, Request, unquote
from urllib.parse import urlencode, quote_plus
from bs4 import BeautifulSoup
import requests
from code_dictionary import *
from data_class import *

decode_key = unquote('YwqDV590HcVx3fgfqBuuDeKB%2F8QsYQuRx2QYmJNnPU6MI99RlPoisyViCa%2B74IM5mX8OC3pe1N2922JS085wQg%3D%3D')

url = 'http://apis.data.go.kr/B551182/hospInfoService/getHospBasisList'


def make_list(addr1, addr2, addr3, type='',page = 1):
    global decode_key, url
    queryParams = '?' + urlencode({quote_plus('ServiceKey'): decode_key,
                                   quote_plus('pageNo'): page, quote_plus('numOfRows'): '20',
                                   quote_plus('sidoCd'): sido_dict[addr1],
                                   quote_plus('sgguCd'): sigugun_dict[sido_dict[addr1]][addr2],
                                   quote_plus('emdongNm'): addr3,
                                   quote_plus('yadmNm'): hos_type[type][0],
                                   quote_plus('zipCd'): hos_type[type][1]
                                   })

    r = requests.get(url + queryParams)
    soup = BeautifulSoup(r.text, 'lxml-xml')

    ## 받아온 data xml형식으로 출력
    #print(soup.decode("utf-8")) # 받아온 xml출력

    xml_data = soup.find_all("item")
    HOSPITAL = []
    HOSPITAL = make_Mydatalist(xml_data)

    total = soup.find('totalCount').get_text()

    return (HOSPITAL,total)




