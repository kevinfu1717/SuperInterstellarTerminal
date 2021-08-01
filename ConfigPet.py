import json
import os
configPath='PetConfigs/'
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
         {98: 'charterIndex越界'},         
         {103:'分割失败'},        
         {104:'没有合适区域存在alien'},         
         {105:'module前处理异常'},
         ]
##
config={
    'alien':{
        1:{
            'name':'蓝牛族',
            'areaIndex': 0,
            'description': ['最喜欢在路上瞎逛，喜欢经常捣腾人类的裤脚。有时，你看动裤脚突然被扯了一下或拉了一下，有可能就是他们干的，他们在能量护罩下，你被弄了还看不到他。'],
            'picPath': '7im.jpg',
            'scaleRatio': 0.18,#from 0 ~1,ratio of the short border of pic
            'mask':0,
            'mixTimes': 0
        },
        2:{
            'name':'蓝天族',
            'areaIndex': 10,
            'description': ['在地球很少能发现，在能量护照隐藏下飞翔于地球各处。不要小看它两个小翅膀，最高飞行速度可以接近音速。'],
            'picPath': 'lantian.jpg',
            'mask':0,
            'scaleRatio': 0.18,#from 0 ~1,ratio of the short border of pic
            'mixTimes': 1
        },       
        3:{
            'name':'不明种族飞船',
            'areaIndex': 10,
            'description': ['可进行星际穿越的飞船，所载种族——未知'],
            'picPath': 'feidie1.jpg',
            'mask':1,
            'scaleRatio': 0.11,#from 0 ~1,ratio of the short border of pic
            'mixTimes': 0
        },  
        4:{
            'name':'飘飘族',
            'areaIndex': 15,
            'description': ['喜欢附在巴士上，以吸收巴士废气为食'],
            'picPath': 'xiaofeidie.jpg',
            'scaleRatio': 0.18,#from 0 ~1,ratio of the short border of pic
            'mask':0,
            'mixTimes': 1
        },
        5:{
            'name':'绿团族',
            'areaIndex': 8,
            'description': ['经常隐藏在绿色树丛或灌木中，去掉隐身就像一团半透明的绿色光团，很难被人发现。为草食性，你家门外的植物莫名枯萎，可能就是被他吸干了。'],
            'picPath': 'lv.jpg',
            'scaleRatio': 0.18,#from 0 ~1,ratio of the short border of pic
            'mask':0,
            'mixTimes': 0
        },
        6:{
            'name':'单眼蓝兽族',
            'areaIndex': 0,
            'description': ['喜欢跟在人后面，不时会发出“嘎嘎”的笑声，若附近没人，你却听到这样的笑声，证明很可能他就在你附近。'],
            'picPath': 'lan.jpg',
            'mask':0,
            'scaleRatio': 0.18,#from 0 ~1,ratio of the short border of pic
            'mixTimes': 1
        },       
        7:{
            'name':'三黄脚族',
            'areaIndex': 13,
            'description': ['在离地几十cm的高度飘来飘去，喜欢追随着小车，喜欢靠近温度在五六十度的东西'],
            'picPath': 'huang.jpg',
            'mask':0,
            'scaleRatio': 0.18,#from 0 ~1,ratio of the short border of pic
            'mixTimes': 0
        },
        8:{
            'name':'单眼彩松鼠族',
            'areaIndex': 1,
            'description': ['在地球较少发现，爱好是在人行道上瞎逛。看店铺各种五颜六色而流连忘返。'],
            'picPath': 'cai.jpg',
            'scaleRatio': 0.18,#from 0 ~1,ratio of the short border of pic
            'mask':0,
            'mixTimes': 0
        },
        9:{
            'name':'三眼怪鸡族',
            'areaIndex': 8,
            'description': ['喜欢跳到树丛或灌木上，偷吃树木上的果实。它很敏感、反应也及其迅速，很难捉到他'],
            'picPath': 'sanyan.jpg',
            'mask':0,
            'scaleRatio': 0.18,#from 0 ~1,ratio of the short border of pic
            'mixTimes': 0
        },       
        10:{
            'name':'幽脸族',
            'areaIndex': 11,
            'description': ['喜欢在人附近飘来飘去，人类坊间描述的幽灵的真身就是它。可以幻化各种外形'],
            'picPath': 'tou.jpg',
            'mask':0,
            'scaleRatio': 0.4,#from 0 ~1,ratio of the short border of pic
            'mixTimes': 0
        },        
        11:{
            'name':'紫脸族',
            'areaIndex': 3,
            'description': ['较少在阳光猛烈的户外出现，多附在墙上。最特别的是它尾巴长在脚上，然后还喜欢模仿摆锤钟一样摆尾巴。'],
            'picPath': '8im.jpg',
            'mask':0,
            'scaleRatio': 0.18,#from 0 ~1,ratio of the short border of pic
            'mixTimes': 1
        },          
        12:{
            'name':'长泡族',
            'areaIndex': 7,
            'description': ['地球上较为少见，经常会靠在交通标志上，把交通标志牌作为靠背，模仿下面汽车行驶的声音'],
            'picPath': '6im.jpg',
            'mask':0,
            'scaleRatio': 0.18,#from 0 ~1,ratio of the short border of pic
            'mixTimes': 1
        },          
        13:{
            'name':'大型星际飞船',
            'areaIndex': 10,
            'description': ['所载乘员未知，最大航速未知，最大航行距离未知。'],
            'picPath': 'feidie2.jpg',
            'mask':1,
            'scaleRatio': 0.2,#from 0 ~1,ratio of the short border of pic
            'mixTimes': 1
        },  
        14:{
            'name':'光外族',
            'areaIndex': 2,
            'description': ['喜欢隐藏在各种建筑或墙壁上，在那里观察人类的活动。或者可能只是在那里发呆'],
            'picPath': '3im.jpg',
            'scaleRatio': 0.18,#from 0 ~1,ratio of the short border of pic
            'mask':0,
            'mixTimes': 1
        },     
    },

}
##
#jsObj = json.dumps(dictObj, indent=4)  # indent参数是换行和缩进
#with open(path,'w') as f:
#    f.write(jsObj)
##
#with open(path) as f:
#    config = json.load(f)
#    print(config)