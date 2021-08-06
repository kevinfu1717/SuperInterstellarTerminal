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
         {201:'图片人脸角度太偏'},
         {200: 'success'},
         {98: 'charterIndex越界'},
         {202: '没有人脸关键点'},
         ]
##
config={
    'alienHead':{
        1:{
            'name':'胡巴星人',
            'descriptions':['胡巴星人，调皮捣蛋惹人喜爱。生气的时候会缩成萝卜的形状。',
                           '胡巴星人私下一个人的时候会有令人吃惊的完全不同的一面。'],
            'front':{
                'bodyPath':'hubaBody1.png',
                'headLeft': 0,
                'headRight': 272,
                'headLower': 253,
                'scaleRatio': 1.6,
                'ratioX': 1.0,
                'ratioY': 1.1,
                'preBias': [0, -0.35],
                # [x ratio of face,y ratio of face]bias after align at the eyes
                'LMJson':"hubaBody.json",  # [[x,y],,,]
                'NeckHeight':300,
                'lowestValue':10,
                'heightGradientBias': 0.6,
                'heightGradientBiasBody':0.95,#body gradient: where to start gradient
                'addWeightRatio':0.8
            },
            'side': {
                'bodyPath': 'hubaBody1.png',
                'headLeft': 0,
                'headRight': 272,
                'headLower': 253,
                'scaleRatio': 1.6,
                'ratioX': 1.0,
                'ratioY': 1.1,
                'preBias': [0, -0.35],
                # [x ratio of face,y ratio of face]bias after align at the eyes
                'LMJson': "hubaBody.json",  # [[x,y],,,]
                'NeckHeight': 300,
                'lowestValue': 10,
                'heightGradientBias': 0.6,
                'heightGradientBiasBody':0.95,#body gradient: where to start gradient
                'addWeightRatio': 0.8
            }

        },
        2:{
            'name':'格鲁特星人',
            'descriptions':['格鲁特星人，身体虽为树木，但却不怕火。只要没化成灰，即便粉身碎骨，也可以复活。',
                           '格鲁特星人作为花神巨像族的一员，格鲁特拥有高度的智慧和树人特有的生理特征——超强的再生能力，只需一部分树枝存在，浇水施肥便能长成大树；此外还拥有超级力量和防御力，能够通过自我生长长成巨人，并且像橡胶一样自如拉伸自己的身体部位，使树木构成的身体自由延展、攻击敌人，还能够通过散播孢子控制其他植物、治疗他人。'],
            'front':{
                'bodyPath':'geluteBody1.png',

                'headLeft':160,
                'headRight':760,
                'headLower':880,
                'scaleRatio': 1.3,#enlarge ratio of total pic
                'ratioX': 1,#enlarge ratio of x
                'ratioY': 1,#enlarge ratio of y
                'preBias': [-0.01, 0],
                # [x ratio of face,y ratio of face]bias after align at the eyes
                'LMJson':"geluteBody.json",  # [[x,y],,,] landmark files made by labelme
                'NeckHeight':990,#cut of 0~ neckheight from body image
                'lowestValue':10,#face gradient: lowest trancparece
                'heightGradientBias': 0.6,#face gradient: where to start gradient
                'heightGradientBiasBody':0.95,#body gradient: where to start gradient
                'addWeightRatio':0.8 #final combine ratio between seamlessclone and hard paste
            },
            'side':{
                'bodyPath':'gelute3.png',
                'headLeft':8,
                'headRight':360,
                'headLower':490,
                'scaleRatio': 1.5,#enlarge ratio of total pic
                'ratioX': 1,#enlarge ratio of x
                'ratioY': 1,#enlarge ratio of y
                'preBias': [-0.01, 0],
                # [x ratio of face,y ratio of face]bias after align at the eyes
                'LMJson':"gelute3.json",  # [[x,y],,,] landmark files made by labelme
                'NeckHeight':550,#cut of 0~ neckheight from body image
                'lowestValue':10,#face gradient: lowest trancparece
                'heightGradientBias': 0.6,#face gradient: where to start gradient
                'heightGradientBiasBody':0.95,#body gradient: where to start gradient
                'addWeightRatio':0.8 #final combine ratio between seamlessclone and hard paste
            }

        },
    }
}
##
# jsObj = json.dumps(config, indent=4)  # indent参数是换行和缩进
# with open(path,'w') as f:
#     f.write(jsObj)
# ##
# with open(path) as f:
#     config = json.load(f)
#     print(config)