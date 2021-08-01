import json
import os
configPath='configs/'
# if not os.path.exists(configPath):
#     !mkdir configs/
path=configPath+'config0720.txt'
##
resultCode=[{99:'运行报错'},
         {100:'dst发送的图片异常'},
         {101:'dst发送的图片太小'},
         {102:'图片人脸角度太偏'},
         {200: 'success'},
         {98: 'charterIndex越界'},
         ]
##
dictObj={
    'huba':{
        'front':{
            'bodyPath':'pic/hubaBody1.png',
            'headLeft': 0,
            'headRight': 272,
            'headLower': 253,
            'scaleRatio': 1.6,
            'ratioX': 1.0,
            'ratioY': 1.1,
            'preBias': [0, -0.35],
            # [x ratio of face,y ratio of face]bias after align at the eyes
            'LMJson':"pic/hubaBody.json",  # [[x,y],,,]
            'NeckHeight':300,
            'lowestValue':10,
            'heightGradientBias': 0.6,
            'heightGradientBiasBody':0.95,#body gradient: where to start gradient
            'addWeightRatio':0.8
        },
        'side': {
            'bodyPath': 'pic/hubaBody1.png',
            'headLeft': 0,
            'headRight': 272,
            'headLower': 253,
            'scaleRatio': 1.6,
            'ratioX': 1.0,
            'ratioY': 1.1,
            'preBias': [0, -0.35],
            # [x ratio of face,y ratio of face]bias after align at the eyes
            'LMJson': "pic/hubaBody.json",  # [[x,y],,,]
            'NeckHeight': 300,
            'lowestValue': 10,
            'heightGradientBias': 0.6,
            'heightGradientBiasBody':0.95,#body gradient: where to start gradient
            'addWeightRatio': 0.8
        }

    },
    'gelute':{
        'front':{
            'bodyPath':'pic/geluteBody1.png',

            'headLeft':160,
            'headRight':760,
            'headLower':880,
            'scaleRatio': 1.3,#enlarge ratio of total pic
            'ratioX': 1,#enlarge ratio of x
            'ratioY': 1,#enlarge ratio of y
            'preBias': [-0.01, 0],
            # [x ratio of face,y ratio of face]bias after align at the eyes
            'LMJson':"pic/geluteBody.json",  # [[x,y],,,] landmark files made by labelme
            'NeckHeight':950,#cut of 0~ neckheight from body image
            'lowestValue':10,#face gradient: lowest trancparece
            'heightGradientBias': 0.6,#face gradient: where to start gradient
            'heightGradientBiasBody':0.95,#body gradient: where to start gradient
            'addWeightRatio':0.8 #final combine ratio between seamlessclone and hard paste
        },
        'side':{
            'bodyPath':'pic/gelute3.png',
            'headLeft':8,
            'headRight':360,
            'headLower':490,
            'scaleRatio': 1.5,#enlarge ratio of total pic
            'ratioX': 1,#enlarge ratio of x
            'ratioY': 1,#enlarge ratio of y
            'preBias': [-0.01, 0],
            # [x ratio of face,y ratio of face]bias after align at the eyes
            'LMJson':"pic/gelute3.json",  # [[x,y],,,] landmark files made by labelme
            'NeckHeight':550,#cut of 0~ neckheight from body image
            'lowestValue':10,#face gradient: lowest trancparece
            'heightGradientBias': 0.6,#face gradient: where to start gradient
            'heightGradientBiasBody':0.95,#body gradient: where to start gradient
            'addWeightRatio':0.8 #final combine ratio between seamlessclone and hard paste
        }

    },

}
##
jsObj = json.dumps(dictObj, indent=4)  # indent参数是换行和缩进
with open(path,'w') as f:
    f.write(jsObj)
##
with open(path) as f:
    config = json.load(f)
    print(config)