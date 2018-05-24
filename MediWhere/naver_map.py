import os
import sys
from urllib.request import urlopen, Request,quote, unquote
from urllib.parse import urlencode, quote_plus

client_id = "79PmkNlKqz1lR4JFEos4"
client_secret = "TJa8CVZIfO"
encText = quote("127.1141382,37.3599968")
#url = "https://openapi.naver.com/v1/map/geocode?query=" + encText # json 결과
url = "https://openapi.naver.com/v1/map/geocode.xml?query=" + encText # xml 결과
request = Request(url)
request.add_header("X-Naver-Client-Id",client_id)
request.add_header("X-Naver-Client-Secret",client_secret)
response = urlopen(request)
rescode = response.getcode()
if(rescode==200):
    response_body = response.read()
    print(response_body.decode('utf-8'))
else:
    print("Error Code:" + rescode)