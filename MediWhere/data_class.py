class Hospital_data():
    def __init__(self,name,type,addr,tel,url,xpos,ypos):
        self.name = name
        self.type = type
        self.addr = addr
        self.tel = tel
        self.url = url
        self.xpos = xpos
        self.ypos = ypos

    def __str__(self):
        if '(' in self.addr:
            addr1 = self.addr.split('(')[0]
            addr2 = '(' + self.addr.split('(')[1]
            return '<   ' + self.name + '   >' + '\n' + self.type + '\n' + addr1 + '\n' + addr2\
                    + '\n' + '☎: ' + self.tel + '\n' +self.url


        else:
            return '<   ' +self.name + '   >'+ '\n' + self.type + '\n' + self.addr\
                   + '\n' + '☎: ' + self.tel + '\n' + self.url



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