from spider import login_ccnu
from aiohttp.web import Response, json_response, Application
from jsoncensor import JsonCensor

api = Application()

async def login_ccnu_luck(request):
    standard = {
        "sid": "str",
        "password": "str"
    }
    jc = JsonCensor(standard, await request.json())
    result = jc.check()
    if result.get('statu') is not True:
        return json_response({"msg": "JSON FORMAT ERROR"}, status = 400)


    info = await request.json()
    sid = info['sid']
    password = info['password']
    data = await login_ccnu(sid, password)
    
    if data.get("msg") == "failed":
        return json_response(data, status = 401)
    if data.get("name") == "":
        return json_response(data, status = 404)

    return json_response(data)

api.router.add_route('POST', '/api/loginccnu/', login_ccnu_luck, name = 'login_ccnu_luck')
