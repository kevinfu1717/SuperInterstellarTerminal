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
         {201: '没有合适的area来处理'},
         ]
##
config={
    'vgetation':{
        1:{
            'name':'光母花',
            'descriptions':['光母花,该植物体内的叶绿素可以发出紫绿色的光,是一种自发光植物',
                           '光母花,该植物在月圆之夜会发出类似女高音的歌声的梵音'],
            'picPath':'afanda1.jpg',
            'mixRatio':0.5,
        },
        2: {
            'name': '荧光光球菇',
            'descriptions': ['荧光光球菇,该植物可通过四种酶的代谢循环产生光。两种酶将咖啡酸转化成发光的前体，然后被第三种酶氧化产生光子。'],
            'picPath': 'afanda2.jpg',
            'mixRatio': 0.5,
        },
        3: {
            'name': '数码绿藤',
            'descriptions': ['数码绿藤.该植物不时会发光，属藤曼类，生长迅速','绿蝇虫最喜欢吃该植物。收割后煎炸来吃味道也不错'],
            'picPath': 'heikediguo.jpg',
            'mixRatio': 0.5,
        },
        4: {
            'name': '红蓝肉肉',
            'descriptions': ['红蓝肉肉.类似地球的多肉植物，在外星遍布广泛，但不是很适应地球环境'],
            'picPath': 'duorou.jpg',
            'mixRatio': 0.5,
        },
        5: {
            'name': '玛娜之花',
            'descriptions': ['玛娜之花喜欢靠近人类，不过并不会主动攻击人类。只有在人类极度削弱的情况下，才会被吸走生命源质，所以也要小心注意。'],
            'picPath': 'manazhihua.jpg',
            'mixRatio': 0.5,
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