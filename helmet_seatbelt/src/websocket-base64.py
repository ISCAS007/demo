#!/usr/bin/env python3

import asyncio
import websockets
import sys
import json,cv2
import datetime
import base64

@asyncio.coroutine
def hello():
    websocket = yield from websockets.connect('ws://t.qdrise.com.cn:1234/')
    
    try:
        return_dict={}
        return_dict['UID']='unknown'
        return_dict['DEVICE_ID']='unknown'
        return_dict['WARN_TYPE']=warning_type=1
        return_dict['WARN_TIME']=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return_dict['DETAIL_INFO']=result='no detatil'
        imgcv=cv2.imread('/home/yzbx/Pictures/1.jpg')
        return_dict['IMAGE_DATA']=imgcv.tolist()

        name=json.dumps(return_dict)
        yield from websocket.send(name)
        print("> {}".format(name))

        greeting = yield from websocket.recv()
        print("< {}".format(greeting))

    finally:
        yield from websocket.close()

asyncio.get_event_loop().run_until_complete(hello())
