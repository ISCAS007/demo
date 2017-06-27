#!/usr/bin/env python3

import asyncio
import websockets
import sys

@asyncio.coroutine
def hello():
    websocket = yield from websockets.connect('ws://t.qdrise.com.cn:1234/')

    try:
        name=sys.argv[1]
        yield from websocket.send(name)
        print("> {}".format(name))

        greeting = yield from websocket.recv()
        print("< {}".format(greeting))

    finally:
        yield from websocket.close()

asyncio.get_event_loop().run_until_complete(hello())
