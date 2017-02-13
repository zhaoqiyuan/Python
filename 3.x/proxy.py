import urllib.request
proxy_handler = urllib.request.ProxyHandler({'http':'username:password@proxy:port'})
opener = urllib.request.build_opener(proxy_handler)
urllib.request.install_opener(opener)

resp = urllib.request.urlopen("http://www.baidu.com")
data = resp.read()
print(len(data))
