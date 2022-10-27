import json

async def read_body(receive):
    """
    Read and return the entire body from an incoming ASGI message.
    """
    body = b''
    more_body = True

    while more_body:
        message = await receive()
        print(message)
        body += message.get('body', b'')
        more_body = message.get('more_body', False)
    try:
        return json.loads(body)
    except json.JSONDecodeError:
        return body
