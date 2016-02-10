
# coding: utf-8
import requests

splash_server = 'http://192.168.99.100:8050'

with open('crawlera-splash.lua') as lua:
    lua_source = ''.join(lua.readlines())
    splash_url = '{}/execute'.format(splash_server)
    r = requests.post(
            splash_url,
            json={
                'lua_source': lua_source,
                'url': url,
            },
            timeout=100,
    )

    fp = open("crawlera-splash.png", "wb")
    fp.write(r.content)
    fp.close()