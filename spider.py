from bs4 import BeautifulSoup
import asyncio
import aiohttp
import random

accounturl = "https://account.ccnu.edu.cn/cas/login"
account_jurl = "https://account.ccnu.edu.cn/cas/login;jsessionid="
info_url = "http://xpcx.ccnu.edu.cn/page.php?cid="

headers = {
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36"
}

proxylist = ["http://79.110:1180", "http://246.73:1180"]

#login util
async def getjid(setcookie):
    start = setcookie.find("=") + 1
    end = setcookie.find(";")
    return setcookie[start:end]

#login util
async def getltid(html):
    soup = BeautifulSoup(html)
    #内网条件下为
    #ltid = soup.find_all('input')[2]['value']
    #execution = soup.find_all('input')[3]['value']
    ltid = soup.find_all('input')[3]['value']
    execution = soup.find_all('input')[4]['value']
    return ltid, execution

async def login_xxmh(sid, pswd, _proxy):
    _cookie_jar = None
    async with aiohttp.ClientSession(cookie_jar = aiohttp.CookieJar(unsafe=True), headers = headers) as session:
        async with session.get(accounturl, timeout = 8, proxy = proxylist[_proxy]) as response:
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
                    return True
                else:
                    return False

async def getinfo(sid, _proxy):
    async with aiohttp.ClientSession(headers = headers) as session:
        async with session.get(info_url + str(sid), timeout = 8, proxy = proxylist[_proxy]) as response:
            html = await response.text()
            soup = BeautifulSoup(html)
            contents = soup.find_all('td', class_ = "cont")
            cont = []
            for item in contents:
                item = item.string
                cont.append(item)
            return (cont[1], cont[2], cont[4])

async def login_ccnu(sid, pswd):
    _proxy = random.randint(0, len(proxylist)-1)
    print(_proxy)
    status = await login_xxmh(sid, pswd, _proxy)
    if status:
        name, gender, college = await getinfo(sid, _proxy)
        return {
            "name":name,
            "gender": gender,
            "college": college,
        }
    else:
        return {
            "msg":"failed"        
        }

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(login_ccnu(2016210, ""))
    loop.close()
