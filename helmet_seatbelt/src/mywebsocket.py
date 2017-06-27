#!/usr/bin/env python2

import websocket
import sys,datetime,json,sys,cv2

def int2byte(number):
    array=[0,0,0,0]
    array[0]=(number>>24) & 0xff
    array[1]=(number>>16) & 0xff
    array[2]=(number>>8) & 0xff
    array[3]=number & 0xff

    return bytearray(array)

def senddata(dicts,imgcv,url="ws://t.qdrise.com.cn:1234"):
    ws=websocket.create_connection(url)
    try:
        img_str = cv2.imencode('.png', imgcv)[1].tostring()
        #img_len=imgcv.size
        img_len=len(img_str)
        USE_SQL=False
        return_dict=dicts
        if USE_SQL:
            return_dict['UID']='unknown'
            return_dict['DEVICE_ID']='unknown'
            return_dict['WARN_TYPE']=warning_type=1
            return_dict['WARN_TIME']=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            return_dict['DETAIL_INFO']=result='no detatil'
        else :
            #return_dict['device']='unknown'
            #return_dict['time']=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            #return_dict['type']=warning_type=1
            #return_dict['detail']=result='no detatil'
            return_dict['image']=img_len
        
        sendstr=json.dumps(return_dict)
        str_len=len(sendstr)
        total_len=str_len+img_len
        
        
        #byte_sendstr=int2byte(total_len)+int2byte(str_len)+bytes(sendstr)+imgcv.tobytes()
        byte_sendstr=int2byte(total_len)+int2byte(str_len)+bytes(sendstr)+bytes(img_str)

        ws.send_binary(byte_sendstr)
        print("> {}".format(byte_sendstr))

        recvstr = ws.recv()
        print("< {}".format(recvstr))

    finally:
        #print("failed!!!")
        ws.close()


def test():
    imgcv=cv2.imread('/home/yzbx/Pictures/1.jpg')
    
    USE_SQL=False
    return_dict={}
    if USE_SQL:
        return_dict['UID']='unknown'
        return_dict['DEVICE_ID']='unknown'
        return_dict['WARN_TYPE']=warning_type=1
        return_dict['WARN_TIME']=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return_dict['DETAIL_INFO']=result='no detatil'
    else :
        return_dict['device']='unknown'
        return_dict['time']=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return_dict['type']=warning_type=1
        return_dict['detail']=result='no detatil'
        #return_dict['image']=img_len
    senddata(return_dict,imgcv)

if __name__ == "__main__":
    test()
