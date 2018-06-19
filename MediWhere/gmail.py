
# smtp 정보
host = "smtp.gmail.com" # Gmail SMTP 서버 주소.
port = "587"

def MakeHtmlDoc(bookMark_List):
    from xml.dom.minidom import getDOMImplementation
    # get Dom Implementation
    impl = getDOMImplementation()

    newdoc = impl.createDocument(None, "html", None)  # DOM 객체 생성
    top_element = newdoc.documentElement
    header = newdoc.createElement('header')
    top_element.appendChild(header)

    # Body 엘리먼트 생성.
    body = newdoc.createElement('body')

    for item in bookMark_List:
        # create bold element
        b = newdoc.createElement('b')
        # create text node
        ibsnText = newdoc.createTextNode("< " + item.name + " >") # < 병원명 >
        b.appendChild(ibsnText)

        body.appendChild(b)

        # BR 태그 (엘리먼트) 생성.
        br = newdoc.createElement('br')
        body.appendChild(br)

        # create title Element
        p = newdoc.createElement('p')
        titleText = newdoc.createTextNode("- " + item.type + " -")
        p.appendChild(titleText)
        body.appendChild(p)

        p = newdoc.createElement('p')
        titleText = newdoc.createTextNode("주소: " + item.addr)
        p.appendChild(titleText)
        body.appendChild(p)

        p = newdoc.createElement('p')
        titleText = newdoc.createTextNode('☎: ' + item.tel)
        p.appendChild(titleText)
        body.appendChild(p)

        p = newdoc.createElement('p')
        titleText = newdoc.createTextNode('HomePage: ' + item.url)
        p.appendChild(titleText)
        body.appendChild(p)

        p = newdoc.createElement('p')
        titleText = newdoc.createTextNode("-----------------------------------------------------------------------")
        p.appendChild(titleText)
        body.appendChild(p)

        body.appendChild(br)  # line end

    # append Body
    top_element.appendChild(body)

    return newdoc.toxml()


def sendMail(addr, html):
    global host, port
    senderAddr = "doood444@gmail.com"
    recipientAddr = addr
    msgtext = ''

    import mysmtplib
    # MIMEMultipart의 MIME을 생성합니다.
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    # Message container를 생성합니다.
    msg = MIMEMultipart('alternative')

    # set message
    msg['Subject'] = "*** MediWhere 북마크 입니다. ***"
    msg['From'] = senderAddr
    msg['To'] = recipientAddr

    msgPart = MIMEText(msgtext, 'plain')
    bookPart = MIMEText(html, 'html', _charset='UTF-8')

    # 메세지에 생성한 MIME 문서를 첨부합니다.
    msg.attach(msgPart)
    msg.attach(bookPart)

    print("connect smtp server ... ")
    s = mysmtplib.MySMTP(host, port)
    # s.set_debuglevel(1)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login("doood444@gmail.com", "")  # 로긴을 합니다.
    #s.sendmail(senderAddr, [recipientAddr], msg.as_string())

    try:
        s.sendmail(senderAddr, [recipientAddr], msg.as_string())
    except:
        print("사망각")
        s.close()
        return False
    else:
        print("Mail sending complete!!!")
        s.close()
        return True


