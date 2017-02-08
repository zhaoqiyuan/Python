#encoding=utf8
import urllib
import re
import httplib
import sys
import time

def run():
  if len(sys.argv)<3:
    return

  username=sys.argv[1]
  password=sys.argv[2]
  for trytime in range(10):
    print('Trial '+str(trytime+1))
    conn=httplib.HTTPConnection('kq.neusoft.com')
    try:
      myheaders={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip,deflate,sdch',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
        'Connection':'keep-alive'}
      conn.request('GET','/',headers=myheaders)
      response=conn.getresponse()
      cookie=response.getheader('set-cookie').split(';')[0]
      html=response.read()

      names=re.compile(r'name="(.*?)"', re.S).findall(html)
      if len(names)!=7:
        print('Error')
        return
      mydata={'login':'true','neusoft_attendance_online':''}
      num=names[3][3:]
      mydata['KEY'+num]=''
      mydata['neusoft_key']='ID'+num+'PWD'+num
      mydata[names[5]]=username
      mydata[names[6]]=password
      mydata=urllib.urlencode(mydata)
      myheaders={'Cache-Control':'max-age=0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip,deflate,sdch',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
        'cookie':cookie,
        'Content-Type':'application/x-www-form-urlencoded',
        'Referer':'http://kq.neusoft.com/',
        'Origin':'http://kq.neusoft.com',
        'Connection':'keep-alive'}
      conn.request('POST','/login.jsp',body=mydata,headers=myheaders)
      response=conn.getresponse()
      html=response.read()

      myheaders={'Cache-Control':'max-age=0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip,deflate,sdch',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
        'cookie':cookie,
        'Referer':'http://kq.neusoft.com/',
        'Connection':'keep-alive'}
      conn.request('GET','/attendance.jsp',headers=myheaders)
      response=conn.getresponse()
      html=response.read()

      tds=re.compile(r'<td>(.*?)</td>', re.S).findall(html)
      print('Before:')
      beforetds=len(tds)
      for i in range(beforetds):
        if i%5==4:
          print('  '+tds[i])
      if len(sys.argv)>3 and sys.argv[3]=='1':
        try:
          input()
        except:
          pass
        break

      empoids=re.compile(r'name="currentempoid" value="(.*?)"', re.S).findall(html)
      mydata={'currentempoid':empoids[0]}
      mydata=urllib.urlencode(mydata)
      myheaders={'Cache-Control':'max-age=0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip,deflate,sdch',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
        'cookie':cookie,
        'Content-Type':'application/x-www-form-urlencoded',
        'Referer':'http://kq.neusoft.com/attendance.jsp',
        'Origin':'http://kq.neusoft.com',
        'Connection':'keep-alive'}
      conn.request('POST','/record.jsp',body=mydata,headers=myheaders)
      response=conn.getresponse()
      html=response.read()

      myheaders={'Cache-Control':'max-age=0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip,deflate,sdch',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
        'cookie':cookie,
        'Referer':'http://kq.neusoft.com/attendance.jsp',
        'Connection':'keep-alive'}
      conn.request('GET','/attendance.jsp',headers=myheaders)
      response=conn.getresponse()
      html=response.read()
      tds=re.compile(r'<td>(.*?)</td>', re.S).findall(html)
      print('After:')
      aftertds=len(tds)
      for i in range(aftertds):
        if i%5==4:
          print('  '+tds[i])
      if aftertds>beforetds:
        if len(sys.argv)>3 and sys.argv[3]=='0':
          try:
            input()
          except:
            pass
        break
      else:
        fuck
    except:
      for i in range(6):
        print('Network is Busy. Try Again After '+str((6-i)*5)+'s')
        time.sleep(5)
    conn.close()

run()
