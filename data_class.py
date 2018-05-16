class Hospital_data():
    def __init__(self,name,type,addr,tel,url,xpos,ypos):
        self.name = name
        self.type = type
        self.addr = addr
        self.tel = tel
        self.url = url
        self.xpos = xpos
        self.ypos = ypos

    def print(self):
        print("-----------------------------")
        print(self.name)
        print("<",self.type,'>')
        print(self.addr)
        print("Tel:",self.tel)
        print(self.url)
        print("-----------------------------")


def make_Mydatalist(list):
    result = []
    for i in list:
        if i.find('hospUrl'):
            result.append(Hospital_data(i.find('yadmNm').get_text(),i.find('clCdNm').get_text(),i.find('addr').get_text(),
                                        i.find('telno').get_text(),i.find('hospUrl').get_text(),
                                        i.find('XPos').get_text(),i.find('YPos').get_text()))
        else:
            result.append(
                Hospital_data(i.find('yadmNm').get_text(), i.find('clCdNm').get_text(), i.find('addr').get_text(),
                              i.find('telno').get_text(), '-',
                              i.find('XPos').get_text(), i.find('YPos').get_text()))

    return result