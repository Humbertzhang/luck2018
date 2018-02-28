from luck import api
from aiohttp import web

app = api

if __name__ == '__main__':
    web.run_app(api, host = '0.0.0.0', port = 1300)
