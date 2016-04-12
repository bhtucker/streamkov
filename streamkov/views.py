# -*- coding: utf-8 -*-
"""
    views
    ~~~~~

    How to handle http endpoints
"""
from aiohttp import web
from uuid import uuid4


async def readurl(request):
    url = request.match_info.get('url', "Anonymous")
    file_queue = request.app['file_queue']

    if url.startswith('http'):
        file_queue.put_nowait(url)
        success = True
    else:
        success = False

    text = "%s processing URL: %s" % (
        'Success' if success else 'Failed', url
    )
    return web.Response(body=text.encode('utf-8'))


async def draw(request):
    mk = request.app['mk']
    text = mk.draw()
    return web.Response(body=text.encode('utf-8'))


async def store_txt_handler(request):
    data = await request.post()
    file_queue = request.app['file_queue']
    txt = data['txt']
    # .filename contains the name of the file in string format.
    filename = txt.filename
    # .file contains the actual file data that needs to be stored somewhere.
    txt_file = data['txt'].file
    content = txt_file.read()

    local_name = str(uuid4())
    local_path = 'static/' + local_name
    with open(local_path, 'wb') as f:
        f.write(content)
    file_queue.put_nowait(local_path)
    return web.Response(body='Upload success!'.encode('utf-8'))
