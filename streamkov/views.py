# -*- coding: utf-8 -*-
"""
    views
    ~~~~~

    How to handle http endpoints
"""
import asyncio
from aiohttp import web
from uuid import uuid4
from streamkov import models, markov, metamarkov
from utils import rollback_on_error


@asyncio.coroutine
def readurl(request):
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


@asyncio.coroutine
def draw(request):
    mk = request.app['mk']
    text = mk.draw()
    return web.json_response(text)
#     web.Response(body=text.encode('utf-8'))


@asyncio.coroutine
@rollback_on_error
def persist(request):
    name = request.match_info.get('name', "Anonymous")
    mk = request.app['mk']
    session = request.app['sa_session']
    chain = models.Chain(state=mk.to_dict(), name=name)
    session.add(chain)
    session.commit()
    text = 'Success'
    return web.Response(body=text.encode('utf-8'))


@asyncio.coroutine
def chains(request):
    print('got a request')
    print(request.headers)
    session = request.app['sa_session']
    chains = session.query(models.Chain).all()
    return web.json_response([
        dict(name=x.name, id=x.id)
        for x in chains])


@asyncio.coroutine
@rollback_on_error
def load(request):
    session = request.app['sa_session']
    _id = request.match_info.get('id', "Anonymous")
    print('handling request for model %s' % _id)
    chain = session.query(models.Chain).filter_by(id=_id).first()
    mk = markov.MarkovGenerator.from_dict(chain.state)
    print(mk.draw())
    request.app['mk'].set_chain(mk)
    return web.json_response(True)


@asyncio.coroutine
@rollback_on_error
def blend(request):
    session = request.app['sa_session']
    chain_ids = map(int, request.match_info.get('ids', '').split(','))
    chains = (
        session.query(models.Chain)
        .filter(models.Chain.id.in_(chain_ids))
        .all()
    )
    component_generators = [
        markov.MarkovGenerator.from_dict(chain.state)
        for chain in chains
    ]
    mk = metamarkov.MetaMarkov(*component_generators)
    print(mk.draw())
    request.app['mk'].set_chain(mk)
    return web.json_response([dict(name=chain.name, id=chain.id) for chain in chains])


@asyncio.coroutine
def store_txt_handler(request):
    data = yield from request.post()
    file_queue = request.app['file_queue']
    txt = data['txt']
    # .file contains the actual file data that needs to be stored somewhere.
    txt_file = data['txt'].file
    content = txt_file.read()

    local_name = str(uuid4())
    local_path = 'static/' + local_name
    with open(local_path, 'wb') as f:
        f.write(content)
    file_queue.put_nowait(local_path)
    return web.Response(body='Upload success!'.encode('utf-8'))
