from spider import login_ccnu
from aiohttp.web import Response, json_response, Application

api = Application()

async def login_ccnu_luck(request):
    info = await request.json()
    sid = info['sid']
    password = info['password']
    data = await login_ccnu(sid, password)
    return json_response(data)

api.router.add_route('POST', '/loginccnu/', login_ccnu_luck, name = 'login_ccnu_luck')
