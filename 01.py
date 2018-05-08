import urllib
import xml.etree.ElementTree as etree


class GetFullData:
    key = 'YwqDV590HcVx3fgfqBuuDeKB%2F8QsYQuRx2QYmJNnPU6MI99RlPoisyViCa%2B74IM5mX8OC3pe1N2922JS085wQg%3D%3D'
    url = 'http://apis.data.go.kr/B552657/ErmctInsttInfoInqireService/getParmacyFullDown?serviceKey=' \
           + key + \
           '&pageNo=1&startPage=1&numOfRows=10&pageSize=10'

    def main(self):
        data = urllib.request.urlopen(self.url).read()
        f = open("sample1.xml","wb")
        f.write(data)
        f.close()


def main():
    tree = etree.parse('sample1.xml')
    root = tree.getroot()

    for i in root.findall('body'):
        print(i.tag, i.text)
        print(i[0].tag, i[0].text)
        print(i[0][0].tag, i[0][0].text)
        print(i[0][0][0].tag, i[0][0][0].text)
        print(i[0][0][1].tag, i[0][0][1].text)
        print(i[0][0][2].tag, i[0][0][2].text)
        print(i[0][0][3].tag, i[0][0][3].text)

#getData = GetFullData()
#getData.main()

main()