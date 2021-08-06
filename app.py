from flask import Flask, request, jsonify
import json
# from collections import deque
import time
from ImgGenerateModule import imgGenerator
import CVTools
import cv2
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_MIMETYPE'] = "application/json;charset=utf-8"

picPath='result.jpg'

@app.route("/test")
def index():
    return "Hello Flask"


@app.route("/imgGenerate", methods=["POST", "GET"])
def users():
    # print(request.headers)

    #print(request.form)
    # deviceid = (request.form.get('deviceid'))
    try:
        query = (request.form.get('query'))
    except Exception as e:
        print(e)
    try:
        alienHeadIndex=int(request.form.get('alienHeadIndex'))
    except Exception as e:
        print(e)

    try:
        vegetateIndex=int(request.form.get('vegetateIndex'))
    except Exception as e:
        print(e)

    try:
        environmentIndex = int(request.form.get('environmentIndex'))
    except Exception as e:
        print(e)

    try:
        alienPetIndex=int(request.form.get('alienPetIndex'))
    except Exception as e:
        print(e)


    if query == None :
        print('query is NONE')
        rp={'result_code': {91:'input param fail'},'img':'','param_dicts':[]}
    else:
        #print('query',query[:50])
        try:
            if alienHeadIndex==None:alienHeadIndex = -1
            if vegetateIndex==None:vegetateIndex = -1
            if environmentIndex==None:environmentIndex = -1
            if alienPetIndex==None:alienPetIndex = -1
            base64img=''
            dst=CVTools.base64CV(query)
            #cv2.imwrite('dst.jpg',dst)
            assert len(dst.shape)>2
            print('dst img shape',dst.shape,'begin run IMG',alienHeadIndex,vegetateIndex,environmentIndex,alienPetIndex)
            rc, img, des = imgGenerator.runImg(dst, alienHeadIndex=alienHeadIndex,
                                vegetateIndex=vegetateIndex, environmentIndex=environmentIndex,alienPetIndex=alienPetIndex)
            if list(rc.keys())[0]>=200 and len(img)>0:
                cv2.imwrite(picPath,img)
                base64img=CVTools.picpath2base64(picPath)
            rp= {'result_code':rc,'img':base64img,'param_dicts':des}

        except Exception as e:
            print('poemer error:', e)

            print('文件', e.__traceback__.tb_frame.f_globals['__file__'])
            print('行号', e.__traceback__.tb_lineno)
            rp={'result_code': {92:'pre or after process fail'},'img':'','param_dicts':[]}

    return jsonify(rp)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8001, debug=True)  # 启动app的调试模式