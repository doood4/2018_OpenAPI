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

    def __str__(self):
        return self.name + '\n' + self.type + '\n' + self.addr + '\n' +'------------------------'

def make_Mydatalist(list):
    result = []
    for i in list:
        url = '-'
        telno = '-'
        xpos = '-'
        ypos = '-'

        if i.find('hospUrl'):
            url = i.find('hospUrl').get_text()

        if i.find("telno"):
            telno = i.find('telno').get_text()

        if i.find('XPos'):
            xpos = i.find('XPos').get_text()
            ypos = i.find('YPos').get_text()

        result.append(Hospital_data(i.find('yadmNm').get_text(), i.find('clCdNm').get_text(), i.find('addr').get_text(),
                                    telno, url, xpos, ypos))


    return result