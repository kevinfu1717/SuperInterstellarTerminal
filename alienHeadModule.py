import numpy as np
import cv2
from landmarkModule import landmarker
from labelmeReader import readJson
import random

import os
# import math
# from segModule import segHumanClass
import CVTools
from ConfigHead import config,resultCode
class TransHeadClass():
    def __init__(self,debug=False,sideAngleThreshold=12,picPath='HeadPic/',config=config):
        self.debug=debug
        self.sideAngleThreshold=sideAngleThreshold
        self.fl=landmarker(self.debug)
        self.config=config
        self.picPath=picPath

        self.charterDict=config['alienHead']
        self.picSizeLimit=500
        self.resultCode=resultCode
        #print('charterDict',self.charterDict)
    def run(self,dst,charterIndex):
        charterIndex=int(charterIndex)
        if charterIndex>len(self.charterDict):
            return self.resultCode[5],[], {}
        try:
            return self.process(dst, charterIndex)
        except Exception as e:
            print('tran headmodule error:',e)
            print('文件', e.__traceback__.tb_frame.f_globals['__file__'])
            print('行号', e.__traceback__.tb_lineno)

            return self.resultCode[0],dst, {}
        
    def process(self,dst,charterIndex):
        charterIndex=int(charterIndex)
        if len(dst)<3:
            # resultCode=101
            return self.resultCode[1],[], {}
        if max(dst.shape[0],dst.shape[1])<self.picSizeLimit:
            return self.resultCode[2],dst, {}
        ## random charterIndex
        if charterIndex==0:
            charterIndex=random.randint(1,len(self.charterDict))
        charter=self.charterDict[charterIndex]
        print('dst shape',dst.shape,'charter:',charter,'charterIndex',charterIndex)


        dstOri=dst.copy()
        dstLM,dstHeight=self.fl.heightestFace(dst)
        ## AREA have face
        if len(dstLM)==0:
            print('没有找到人脸关键点')

            return self.resultCode[6],dst, {}

        headAngleBias=CVTools.headAngle(dstLM)
        print('headAngleBias',headAngleBias)
        if np.abs(headAngleBias[0])<self.sideAngleThreshold:
            face='front'
        elif np.abs(headAngleBias[0])<40:
            face='side'
        else:
            # face = 'side'
            print('人脸角度太偏了')

            return self.resultCode[3],dst, {}


        scaleRatio=self.charterDict[charterIndex][face]['scaleRatio']
        ratioX=self.charterDict[charterIndex][face]['ratioX']
        ratioY=self.charterDict[charterIndex][face]['ratioY']
        preBias = self.charterDict[charterIndex][face]['preBias']#[x ratio of face,y ratio of face]bias after align at the eyes

        srcPath2=self.charterDict[charterIndex][face]['bodyPath']
        srcLM = readJson(os.path.join(self.picPath,self.charterDict[charterIndex][face]['LMJson']) )# [[x,y],,,]

        neckHeight=self.charterDict[charterIndex][face]['NeckHeight']
        lowestValue = self.charterDict[charterIndex][face]['lowestValue']
        heightGradientBias = self.charterDict[charterIndex][face]['heightGradientBias']
        heightGradientBiasBody = self.charterDict[charterIndex][face]['heightGradientBiasBody']

        addWeightRatio=self.charterDict[charterIndex][face]['addWeightRatio']

        headLower=self.charterDict[charterIndex][face]['headLower']
        # description=self.charterDict[charterIndex]['description']
    # print('srcLM', srcLM)
    ##
        # print('srcPath2',srcPath2)
        # srcPath2=''
        srcBody=cv2.imread(os.path.join(self.picPath,srcPath2),cv2.IMREAD_UNCHANGED )
        assert  len(srcBody.shape)>2
        # print('srcBody',srcBody.shape)
        #
        targetCenter,targetScaleX = CVTools.landmarkCenter(dstLM)
        srcCenter,srcScaleX =  CVTools.landmarkCenter(srcLM)
        ratio=targetScaleX/srcScaleX*scaleRatio

    #
        srcBody,srcHead= CVTools.roiHeadBody(srcBody,headLower,neckHeight)

        srcBody=CVTools.resize(srcBody,ratioX,ratioY,ratio)
        srcHead=CVTools.resize(srcHead,ratioX,ratioY,ratio)
    #
        srcLMHead = srcLM.copy()
        # srcLMHead[:, 0] = srcLMHead[:, 0] - headLeft
        #print('srcLMHead',srcLMHead)
        srcLMHead = np.array(srcLMHead * ratio, 'int64')
        srcLM = np.array(srcLM * ratio, 'int64')
        #
        srcLM, srcBody, srcLMHead, srcHead=CVTools.flipFace(headAngleBias, self.sideAngleThreshold, srcLM, srcBody, srcLMHead, srcHead)

        maskBody,srcBody=CVTools.splitMask(srcBody)
        maskHead,srcHead=CVTools.splitMask(srcHead)

        if self.debug:
            cv2.imwrite('srcHeadresize.jpg',srcHead)
    ######## caculate body image

        leftTop=CVTools.calLandmarkLeftTop(dstLM, srcLMHead,preBias,headAngleBias)

        srcHead,maskHead,leftTop,rightDown,x1, x2, y1, y2=CVTools.roiAreaCheck(srcHead,maskHead, dst, leftTop)


        ##mask of the head(just head) with 3 channel
        maskHead3 = CVTools.mask3Channel(maskHead,srcHead)
        ##mask of the whole dst picture
        maskDst=np.zeros(dstOri.shape,dstOri.dtype)

        dstOri=CVTools.hardPaste(dstOri,leftTop,rightDown,maskHead3,srcHead)

        #gradient mask
        maskHead3=CVTools.gradientMask(maskHead3, lowestValue, heightGradientBias)
        maskDst[leftTop[1]:rightDown[1],leftTop[0]:rightDown[0],:]=maskHead3

        if self.debug:
            cv2.imwrite('maskHead3.jpg',maskHead3)
            cv2.imwrite('srcBody.jpg',srcBody)
            cv2.imwrite('hardPaste.jpg',dstOri)
            cv2.imwrite('maskDst.jpg',maskDst)
        # ##

        leftTop=CVTools.calLandmarkLeftTop(dstLM, srcLM,preBias,headAngleBias)

        # cv2.imwrite('src1.jpg',srcBody)
        srcBody,maskBody,leftTop,rightDown,x1, x2, y1, y2=CVTools.roiAreaCheck(srcBody,maskBody, dst, leftTop)
        # cv2.imwrite('src2.jpg',srcBody)
        #

        maskBody3=CVTools.mask3Channel(maskBody, srcBody)
        maskBody3=CVTools.gradientMask(maskBody3, lowestValue, heightGradientBiasBody)
        center=CVTools.leftTop2Center(leftTop,srcBody)
        # print('leftTop,rightDown',leftTop,rightDown,center)

        # maskBody3=cv2.cvtColor(srcBody,cv2.COLOR_BGR2GRAY)
        normal_clone = cv2.seamlessClone(srcBody, dst, maskBody3, center, cv2.NORMAL_CLONE)
        # normal_clone =hardPaste(dst,leftTop,rightDown,maskBody3,srcBody)
        result=CVTools.addWeight(dstOri, normal_clone, addWeightRatio, maskDst)
        # result = addWeight(dstOri, normal_clone, addWeightRatio, None)
        if self.debug:
            cv2.imwrite('test/normal_clone0.jpg', normal_clone)
            cv2.imwrite('test/result.jpg',result)
            cv2.imwrite('test/maskBody33.jpg',maskBody3)

        # ##
        # dstFace,center,mask3=CVTools.roiDst(dst,dstLM)
        # # print(dstFace.type(),center.type(),mask3.type(),result.type())
        #
        # result = cv2.seamlessClone(dstFace, normal_clone, mask3, center, cv2.MONOCHROME_TRANSFER)
        # cv2.imwrite('im.jpg',mask3)

        return self.resultCode[4],result,self.charterDict[charterIndex]
if __name__=='__main__':
    dstPath='testpic/jiayuting.jpg'
    # dstPath='testpic/wyf.jpg'

    # dstPath='testpic/leijiayin.jpg'
    # dstPath='testpic/liyanhong.jpg'
    dstPath='testpic/sadamu.jpg'
    dst = cv2.imread(dstPath)
    thc=TransHeadClass(True)
    rc,img,des=thc.run(dst,2)
    print(rc)
    if list(rc.keys())[0]==200:
        print(des['name'])
        print(des['descriptions'])
        print(cv2.imwrite('test/result.jpg',img))
