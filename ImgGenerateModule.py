try:
    from ConfigPet import resultCode
    from alienHeadModule import TransHeadClass

except Exception as e:
    from ConfigHead import resultCode

    print(e)
import os
import numpy as np
import cv2
try:
    from CityscapesModule import *
except Exception as e:
    print(e)
from alienPetModule import alienPetClass

from vegetateModule import vegetateTransClass
from sandModule import sandClass
import paddle

paddle.disable_static()
# paddle.device.set_device("cpu")
def minimizeInput(img,size):

    ratio=size/max(img.shape[:2])
    img=cv2.resize(img,None,fx=ratio,fy=ratio)
    return img
class ImgGenerator():
    def __init__(self, debug=False,
                 ymlPathSeg='PetModel/mscale_ocr_cityscapes_autolabel_mapillary_ms_val.yml',
                 modelPathSeg='PetModel/modelCityscape.pdparams',
                 modelPathSand='msgnet',
                 picPathHead='HeadPic/',
                 picPathPet='PetPic/',
                 picPathVeg='VegPic',
                 inputSize=700,
                 picSizeLimit=500):
        ##ps: pay attention to the pretrained model path in yml file
        self.resultCode = resultCode
        self.inputSize=inputSize
        self.picSizeLimit = picSizeLimit
        ## 环境识别
        try:
            self.seg = cistyScaperClass(
                debug=debug,
                cfgModelPath1=ymlPathSeg,
                model_path1=modelPathSeg)
            print('seg__load___success______')
        except Exception as e:
            class ss():
                def __init__(self):
                    self.classNums=18
                def run(self,dst):
                    mask = cv2.imread('test/mask.jpg')
                    mask = np.where(mask > 100, 8, 0)[:, :, 0]
                    return {200:'success'},mask
            self.seg=ss()
            print(' cityscapes module error', e)

        ## 换头
        try:
            self.transHead = TransHeadClass(debug=debug, sideAngleThreshold=15, picPath=picPathHead)
        except:
            pass

        # 换植物
        try:
            self.vegetation = vegetateTransClass(picPath=picPathVeg)
            print('self.vegetation sucess:',self.vegetation)
            self.sander = sandClass(stylePath=os.path.join(picPathVeg,'sand.jpg'),modelPath=modelPathSand)
            
            print('self.sander sucess:',self.sander)
        except Exception as e:
            print(e)


        # print('ImgGenerator resultCode', resultCode)
        # 换外星动物
        try:
            self.petModule = alienPetClass(picPathPet)
        except Exception as e:
            print(' pet  module error:', e)

    def process(self, dst, alienHeadIndex,  vegetateIndex,enviromentIndex,alienPetIndex):
        img = []
        dic = []

        if dst is None:
            rcAll = self.resultCode[1]
            print('dst img is none')
        else:


            print('dst image shape', dst.shape[:2])
            if np.max(dst.shape[:2]) < self.picSizeLimit:
                ##pic too small
                rcAll = self.resultCode[2]
            else:
                if alienHeadIndex >= 0 or alienPetIndex >= 0 or enviromentIndex >= 0 or vegetateIndex >= 0:
                    dst = minimizeInput(dst,self.inputSize)
                    rcSeg, pred = self.seg.run(dst)
                    if list(rcSeg.keys())[0] < 200:
                        rcAll = self.resultCode[6]
                    else:
                        ## the total result code of whole process
                        rcAll = rcSeg
                        rcHead, img, dicHead = self.alienHeadProcess(alienHeadIndex, dst)
                        ##
                        img, dst, rcAll = self.checkLastResult(img, dst, rcAll, rcHead)
                        rcVeg, img, dicVeg = self.vegetateProcess(vegetateIndex, img, pred)

                        ##
                        img, dst, rcAll = self.checkLastResult(img, dst, rcAll, rcVeg)
                        #print(rcAll,rcPet)
                        rcEnv, img, dicEnv = self.enviromentProcess(enviromentIndex, img, pred)
                        ##
                        img, dst, rcAll = self.checkLastResult(img, dst, rcAll, rcEnv)
                        rcPet, img, dicPet = self.alienPetProcess(alienPetIndex, img, pred, self.seg.classNums)

                        ##
                        dic = [dicHead, dicVeg, dicEnv,dicPet]
                else:
                    ##
                    print('do not ask for generate')
                    rcAll = self.resultCode[4]
                    img = dst
        print('imgGenerate process finish')
        return rcAll, img, dic

    def alienPetProcess(self, alienPetIndex, img,pred,classNums):
        dic = {}
        if alienPetIndex >= 0:
            print(alienPetIndex, len(self.petModule.alienDict))
            if alienPetIndex <= len(self.petModule.alienDict):
                print('begin alien pet module', alienPetIndex)
                rc, img, dic = self.petModule.run(img, pred,classNums,alienPetIndex)
            else:
                rc = self.resultCode[5]
        else:
            print('do ont need add pet')
            rc = self.resultCode[4]

        return rc, img, dic

    def checkLastResult(self, img, dst, rcAll, rc):
        print('check last result',rc)
        if int(list(rc.keys())[0]) >= 200:
            return img, img, rcAll
        else:
            print('ImgGenerator:last process not sucess')
            return dst, dst, rc
    # 
    def alienHeadProcess(self, alienHeadIndex, dst):
        img = dst
        dic = {}
        if alienHeadIndex >= 0:
            if alienHeadIndex <= len(self.transHead.charterDict):
                print('begin trans head module')
                rc, img, dic = self.transHead.run(dst, alienHeadIndex)
            else:
                rc = self.resultCode[5]
        else:
            print('do not need transHead')
            rc = self.resultCode[4]

        return rc, img, dic

    def vegetateProcess(self, index, dst, pred):
        img = dst
        dic = {}
        if index >= 0:

            if self.vegetation is None: return self.resultCode[4],img, dic
            if index <= len(self.vegetation.configDict):
                print('begin veg  module')
                rc, img, dic = self.vegetation.run(dst, index, pred)
            else:
                rc = self.resultCode[5]
        else:
            print('do not need vegetation')
            rc = self.resultCode[4]
        return rc, img, dic

    def enviromentProcess(self, index, dst, pred):

        img = dst
        dic = {}
        if index >= 0:
            print('begin envir process')
            if self.sander is None: rc = self.resultCode[4]
            rc, img, dic = self.sander.run(dst, pred)
        else:
            print('do not need trans enviroment')
            rc = self.resultCode[4]

        return rc, img, dic

    def run(self, dstPath, alienHeadIndex=-1,vegetateIndex=-1, environmentIndex=-1,alienPetIndex=-1):
        try:
            print('dstPath path:', dstPath)
            dst = cv2.imread(dstPath)
            return self.process(dst, alienHeadIndex,  vegetateIndex,alienPetIndex, environmentIndex)
        except Exception as e:
            print(e)
            print('文件', e.__traceback__.tb_frame.f_globals['__file__'])
            print('行号', e.__traceback__.tb_lineno)
            return self.resultCode[0], [], []
    def runImg(self, dst, alienHeadIndex=-1,vegetateIndex=-1, environmentIndex=-1,alienPetIndex=-1):
        try:

            return self.process(dst, alienHeadIndex,  vegetateIndex, environmentIndex,alienPetIndex)
        except Exception as e:
            print(e)
            print('文件', e.__traceback__.tb_frame.f_globals['__file__'])
            print('行号', e.__traceback__.tb_lineno)
            return self.resultCode[0], [], []

imgGenerator = ImgGenerator(debug=False,
                   ymlPathSeg='PetModel/mscale_ocr_cityscapes_autolabel_mapillary_ms_val.yml',
                   modelPathSeg='PetModel/modelCityscape.pdparams',
                   modelPathSand='msgnet',
                   picPathHead='HeadPic/',
                   picPathPet='PetPic/',
                   picPathVeg='VegPic')


if __name__ == '__main__':


    dstPath = 'testpic/jiayuting.jpg'
    dstPath = 'test/input.jpg'


    dstPath = 'testpic/wyf.jpg'
    rc, img, des = imgGenerator.run(dstPath, alienHeadIndex=0, vegetateIndex=0, environmentIndex=0,  alienPetIndex=0)
    dstPath = 'testpic/test0.jpg'
    ## PS!!!: index==-1:do not process, index=0: random choose one, index>0: choose the one id is index
    rc, img, des = imgGenerator.run(dstPath, alienHeadIndex=0, vegetateIndex=0,environmentIndex=0,  alienPetIndex=0)
    # rc={key:value}: key >=200:successs, 100<=key<200: condition not satisfied， key<100:program error
    # img: the return image, may be [] while key <200
    # dis: the descriptions of the alien

    print('rc=',rc)
    if list(rc.keys())[0] >= 200:
        print(cv2.imwrite('result.jpg', img))
