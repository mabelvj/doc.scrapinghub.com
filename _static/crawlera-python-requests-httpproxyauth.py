import requests

url = "https://twitter.com"
proxy_host = "proxy.crawlera.com"
proxy_port = "8010"
proxy_auth = "<APIKEY>:"
proxies = {"https": "https://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port)}

r = requests.get(url, proxies=proxies, verify='/path/to/crawlera-ca.crt')

print("""
Requesting [{}]
through proxy [{}]

Request Headers:
{}

Response Time: {}
Response Code: {}
Response Headers:
{}
""".format(url, proxy_host, r.request.headers, r.elapsed.total_seconds(),
           r.status_code, r.headers, r.text))
