# -*- coding: utf-8 -*-
import urllib.request
from xml.dom.minidom import parse, parseString
import xml.etree.ElementTree as etree

def str_to_utf(str1):
    a = str1.encode('utf-8')
    a = str(a)
    a = a.replace(a[0],'',1)
    a = a.replace("'",'')
    a = a.replace("\\x",'%')
    a = a.upper()
    return a

class GetData:
    def __init__(self,add1,add2):
        self.Q0 = str_to_utf(add1) # 시도
        self.Q1 = str_to_utf(add2) # 시군구
        self.key = 'YwqDV590HcVx3fgfqBuuDeKB%2F8QsYQuRx2QYmJNnPU6MI99RlPoisyViCa%2B74IM5mX8OC3pe1N2922JS085wQg%3D%3D'
        self.url = ''

    def makeXML(self):
        self.url = 'http://apis.data.go.kr/B552657/ErmctInsttInfoInqireService/getParmacyListInfoInqire?' \
              'serviceKey=' + self.key + \
              '&Q0=' + self.Q0 + '&Q1=' + self.Q1 + \
              '&pageNo=1&numOfRows=10'

# %EC%84%9C%EC%9A%B8%ED%8A%B9%EB%B3%84%EC%8B%9C  %EA%B0%95%EB%82%A8%EA%B5%AC

        data = urllib.request.urlopen(self.url).read()
        f = open("drug.xml","wb")
        f.write(data)
        f.close()


def main():
    #str1 = input("시,도 를 입력하세요:")
    #str2 = input("시,군,구 를 입력하세요:")
    str1 = "서울특별시"
    str2 = "강남구"
    data = GetData(str1,str2)
    data.makeXML()

    tree = etree.parse('drug.xml')
    root = tree.getroot()

    for i in root.findall('body'):
        print(i.tag, i.text)
        print(i[0].tag, i[0].text)
        print(i[0][0].tag, i[0][0].text)
        print(i[0][0][0].tag, i[0][0][0].text)




#main()
print(str_to_utf("신내동"))

