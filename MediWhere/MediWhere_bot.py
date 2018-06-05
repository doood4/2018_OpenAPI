#!/usr/bin/python
# coding=utf-8

import time
import sqlite3
import telepot
from pprint import pprint
from datetime import date, datetime, timedelta
import noti

# addr1, addr2, addr3, type='', page=1
def replyAptData( user, addr1, addr2, addr3, type='', page=1):
    print(user, addr1, addr2, addr3, type, page)
    res_list = noti.getData(addr1, addr2, addr3, type, page)
    msg = ''
    for r in res_list:
        print( str(datetime.now()).split('.')[0], r )
        if len(r+msg)+1>noti.MAX_MSG_LENGTH:
            noti.sendMessage( user, msg )
            msg = r+'\n'
        else:
            msg += r+'\n'
    if msg:
        noti.sendMessage( user, msg )
    else:
        noti.sendMessage( user, "해당하는 데이터가 없습니다." )

def save( user, loc_param ):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, location TEXT, PRIMARY KEY(user, location) )')
    try:
        cursor.execute('INSERT INTO users(user, location) VALUES ("%s", "%s")' % (user, loc_param))
    except sqlite3.IntegrityError:
        noti.sendMessage( user, '이미 해당 정보가 저장되어 있습니다.' )
        return
    else:
        noti.sendMessage( user, '저장되었습니다.' )
        conn.commit()

def check( user ):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, location TEXT, PRIMARY KEY(user, location) )')
    cursor.execute('SELECT * from users WHERE user="%s"' % user)
    for data in cursor.fetchall():
        row = 'id:' + str(data[0]) + ', location:' + data[1]
        noti.sendMessage( user, row )


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type != 'text':
        noti.sendMessage(chat_id, '난 텍스트 이외의 메시지는 처리하지 못해요.')
        return

    text = msg['text']
    args = text.split(' ')
    #  ex) 검색 서울시 양천구 목동 치과
    # args [0]  [1]    [2]  [3]  [4]
    if text.startswith('!검색') and len(args) > 1:
        print('try to !검색', args[1])
        replyAptData(chat_id,args[1], args[2],args[3],args[4])
    elif text.startswith('!확인'):
        print('try to !확인')
        check( chat_id )
    else:
        noti.sendMessage(chat_id, """
                        모르는 명령어입니다.
                        \n ↓↓↓ 사용가능 명령어 ↓↓↓
                        \n!검색 [시/도] [시/구/군] [동] [병원종류]
                        \nex) !검색 서울특별시 양천구 목동 종합병원
                        \n<병원종류>
                        \n- 종합병원, 한반병원, 한의원, 보건소, 내과, 정신과, 피부과, 소아과, 이비인후과, 안과, 치과, 산부인과, 비뇨기과, 정형외과 
                        """)

def main():
    today = date.today()
    current_month = today.strftime('%Y%m')

    print('[', today, ']received token :', noti.TOKEN)

    bot = telepot.Bot(noti.TOKEN)
    pprint(bot.getMe())

    bot.message_loop(handle)

    print('Listening...')

    while 1:
        time.sleep(10)

if __name__ == '__main__':
    main()

