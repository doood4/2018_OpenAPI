#!/usr/bin/python
# coding=utf-8

import sys
import time
import sqlite3
import telepot
from pprint import pprint
from xml_data import *
import re
from datetime import date, datetime, timedelta
import traceback


TOKEN = '617897602:AAHopbkhRVnUsRtX-kBSNcyDbns73gfIZxA'
MAX_MSG_LENGTH = 300
bot = telepot.Bot(TOKEN)

def getData(addr1, addr2, addr3, type='', page=1):
    from xml_data import decode_key, url
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

    res_list = []
    hospital_class_list = []
    xml_data = soup.find_all("item")
    hospital_class_list = make_Mydatalist(xml_data)
    for i in hospital_class_list:
        res_list.append(i.__str__() + "\n" )

    return res_list



def sendMessage(user, msg):
    try:
        bot.sendMessage(user, msg)
    except:
        traceback.print_exc(file=sys.stdout)

def run(date_param, param='11710'):
    conn = sqlite3.connect('logs.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS logs( user TEXT, log TEXT, PRIMARY KEY(user, log) )')
    conn.commit()

    user_cursor = sqlite3.connect('users.db').cursor()
    user_cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, location TEXT, PRIMARY KEY(user, location) )')
    user_cursor.execute('SELECT * from users')

    for data in user_cursor.fetchall():
        user, param = data[0], data[1]
        print(user, date_param, param)
        res_list = getData( param, date_param )
        msg = ''
        for r in res_list:
            try:
                cursor.execute('INSERT INTO logs (user,log) VALUES ("%s", "%s")'%(user,r))
            except sqlite3.IntegrityError:
                # 이미 해당 데이터가 있다는 것을 의미합니다.
                pass
            else:
                print( str(datetime.now()).split('.')[0], r )
                if len(r+msg)+1>MAX_MSG_LENGTH:
                    sendMessage( user, msg )
                    msg = r+'\n'
                else:
                    msg += r+'\n'
        if msg:
            sendMessage( user, msg )
    conn.commit()

if __name__=='__main__':
    today = date.today()
    current_month = today.strftime('%Y%m')

    print( '[',today,']received token :', TOKEN )

    pprint( bot.getMe() )

    run(current_month)
