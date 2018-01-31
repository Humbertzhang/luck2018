import aiohttp
import asyncio

loginurl = "http://0.0.0.0:1300/loginccnu/"

result = []

async def test_login(sid, pswd):
    payload = {
        "sid":sid,
        "password":pswd
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(loginurl, json = payload) as resp:
            status = resp.status
            result.append(status)

if __name__ == '__main__':
    TASKNUM = 50
    loop = asyncio.get_event_loop()
    tasks = [asyncio.ensure_future(test_login(2016210942, "")) for i in range(1, TASKNUM)]
    loop.run_until_complete(asyncio.wait(tasks))
    print(result)
    count = 0
    for i in result:
        if i == 200:
            count += 1
    print(count / TASKNUM)
