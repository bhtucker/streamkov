# -*- coding: utf-8 -*-
"""
    app
    ~~~

    Runs simple streaming markov chain app
"""
import asyncio
from aiohttp import web
from aiohttp_index import IndexMiddleware
from streamkov import markov, text, worker, views, models, utils
from sqlalchemy.orm import sessionmaker


if __name__ == '__main__':
    # initialize app-level globals
    bigram_queue = asyncio.Queue()
    file_queue = asyncio.Queue()
    mk = utils.MarkovGeneratorProxy()
    mk.set_chain(markov.MarkovGenerator())
    session = sessionmaker(bind=models.engine)()

    # setup queue consumers
    loop = asyncio.get_event_loop()
    tasks = [
        loop.create_task(worker.receiver(bigram_queue, mk)),
        loop.create_task(worker.dripfeeder(file_queue, bigram_queue))
    ]
    asyncio.wait(tasks)

    # setup http app
    app = web.Application(middlewares=[IndexMiddleware()])

    app.router.add_route('GET', '/draw/', views.draw)
    app.router.add_route('GET', '/read/{url}', views.readurl)
    app.router.add_route('GET', '/chains', views.chains)
    app.router.add_route('GET', '/load/{id}', views.load)
    app.router.add_route('GET', '/blend/{ids}', views.blend)
    app.router.add_route('POST', '/store/txt', views.store_txt_handler)
    app.router.add_route('GET', '/persist/{name}', views.persist)

    app.router.add_static('/', 'static')
    app['mk'] = mk
    app['file_queue'] = file_queue
    app['sa_session'] = session

    web.run_app(app)
