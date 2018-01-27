import requests
from bs4 import BeautifulSoup
import asyncio
import aiohttp

accounturl = "https://account.ccnu.edu.cn/cas/login"
account_jurl = "https://account.ccnu.edu.cn/cas/login;jsessionid="
headers = {
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36"
}

proxylist = ["proxies"]

#login util
async def getjid(setcookie):
    start = setcookie.find("=") + 1
    end = setcookie.find(";")
    return setcookie[start:end]

#login util
async def getltid(html):
    soup = BeautifulSoup(html, "html5lib")
    #内网条件下为
    #ltid = soup.find_all('input')[2]['value']
    #execution = soup.find_all('input')[3]['value']
    ltid = soup.find_all('input')[3]['value']
    execution = soup.find_all('input')[4]['value']
    return ltid, execution

async def login_ccnu(sid, pswd):
    _cookie_jar = None
    async with aiohttp.ClientSession(cookie_jar = aiohttp.CookieJar(unsafe=True), headers = headers,) as session:
        async with session.get(accounturl, timeout = 8) as response:
            ltid, execution = await getltid(await response.text())
            jid = await getjid(response.headers['set-cookie'])
            payload = {
                "username":sid,
                "password":pswd,
                "lt":ltid,
                "execution":execution,
                "_eventId":"submit",
                "submit":"LOGIN"
            }
            async with session.post(account_jurl + jid, data = payload, timeout = 8) as res2:
                if "CASTGC" in res2.cookies:
                    print("Success")
                else:
                    print("Failed")

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(login_ccnu(2016000000, "password"))
    loop.close()
