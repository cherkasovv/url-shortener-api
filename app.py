from response import Response
from api import API
from errors import Api404Error, Api422Error
import string
import random 
import json


app = API()


SHORT_LINKS = {}


def create_short_url(request) -> Response:
    if not request.body or not request.body.get('url'):
        raise Api422Error()
    short_url_id = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
    SHORT_LINKS[short_url_id] = request.body['url']
    return Response(status=200, content=f'/url/{short_url_id}')


def redirect_short_url(request, data) -> Response:
    print(SHORT_LINKS)
    if data in SHORT_LINKS:
        return Response(status=301, content=SHORT_LINKS[data])
    raise Api404Error()


app.add_route('/url/create', create_short_url)
app.add_route("/url/([\w\-\.]+)", redirect_short_url)
