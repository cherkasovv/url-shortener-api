import json
from typing import Union, Callable, Optional
from errors import Api404Error, ApiError
from request import Request
from utils import read_body
import re


class API:
    def __init__(self):
        self.routes = {}

    async def handle_request(self, path: str) -> Callable:
        for path_route, view in self.routes.items():
            args = re.findall(path_route, path)
            if not args:
                continue
            elif path_route in args:
                return view, []
            else:
                return view, args

        raise Api404Error()

    async def send_response(self, status: int, send: Callable, content: Optional[Union[dict, str]] = None):
        headers = [[b'content-type', b'application/json']]
        if status == 301:
            headers.append([b'Location', content.encode('UTF-8')])

        await send({
        'type': 'http.response.start',
        'status': status,
        'headers': headers
        })

        if status == 200 and content:
            await send({
                'type': 'http.response.body',
                'body': json.dumps(content).encode('UTF-8') if type(content) is dict else content.encode('UTF-8'),
                'more_body': True
            })

        await send({
            'type': 'http.response.body',
            'body': b'',
        })

    async def __call__(self, scope, receive, send):
        request = Request(
            scope.get('path'), scope.get('method'), await read_body(receive)
        )
        try:
            view, args = await self.handle_request(request.path)
            response = view(request, *args)
            await self.send_response(response.status, send, response.content)
        except ApiError as e:
            await self.send_response(e.status, send)

    
    def add_route(self, path: str, view: Callable):
        self.routes[path] = view
