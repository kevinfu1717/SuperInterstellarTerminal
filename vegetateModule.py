import cv2
import random
import numpy as np
import os
import sys
from ConfigVegetae import config as configVeg
from ConfigVegetae import resultCode
class vegetateTransClass():
    def __init__(self,picPath='VegPic'):
        self.picPath=picPath
        self.resultCode=resultCode
        self.configDict = configVeg['vgetation']
        self.maskIndex=8# cityscape Index of vegetation
        print('self.configDict',self.configDict)
    def run(self,image,vegetateIndex,mask=[],maskRatio=1):
        return self.process(image,vegetateIndex,mask,maskRatio)

    def process(self,content,vegetateIndex,mask,maskRatio):
        try:
            vegetateIndex=int(vegetateIndex)
            dic={}
            if vegetateIndex==-1:
                return resultCode[1],content, {}
            elif vegetateIndex==0:
                vegetateIndex=random.randint(1,len(self.configDict))
            path=os.path.join(self.picPath,self.configDict[vegetateIndex]['picPath'])
            style=cv2.imread(path)[:,:,:3]
            assert  len(style)>0
            ratio=self.configDict[vegetateIndex]['mixRatio']
            assert (ratio>=0 and ratio<=1)
            style=randomFlip(style)
            
            if len(mask)==0:## without mask
                result=colorTransfer(content, style, ratio=ratio)
            else:
                # mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN,cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))                                   )
                mask=np.where(mask==self.maskIndex,1,0)
                ## has suspect area
                if np.max(mask)>0:
                    rowFirst, rowLast = noneZeroIndex(mask, 1)
                    colFirst, colLast = noneZeroIndex(mask, 0)
                    result = content.copy()
                    #print('rowFirst:rowLast,colFirst:colLast',rowFirst,rowLast,colFirst,colLast)
                    result[rowFirst:rowLast,colFirst:colLast,:]= \
                        colorTransfer(result[rowFirst:rowLast,colFirst:colLast,:], style, ratio=ratio)

                    result[:,:,0]=np.where(mask==1,result[:,:,0],content[:,:,0])
                    result[:,:,1]=np.where(mask==1,result[:,:,1],content[:,:,1])
                    result[:,:,2]=np.where(mask==1,result[:,:,2],content[:,:,2])
                    print('result',result.shape,np.max(result))
                    # cv2.imwrite('roiresult.jpg',result)

                    result=cv2.addWeighted(content,1-maskRatio,result,maskRatio,0)
                    result=np.array(result,'uint8')
                    rcAll = self.resultCode[4]
                    dic=self.configDict[vegetateIndex]
                else:
                    print('no area match vegetate')
                    result=content
                    rcAll=self.resultCode[6]

            return rcAll,result,dic
        except Exception as e:
            print('vegetate error',e)
            print('文件', e.__traceback__.tb_frame.f_globals['__file__'])
            print('行号', e.__traceback__.tb_lineno)
            return self.resultCode[0],content, {}
def noneZeroIndex(array_2D,axis):
    # array_2D = np.array(
    #     [[0, 0, 2, 3, 0, 4], [0, 0, 0, 0, 0, 0], [1, 0, 2, 3, 4, 0], [1, 0, 2, 3, 4, 9], [0, 0, 0, 0, 0, 0]])
    # axis = 1
    line = np.max(array_2D, axis)
    first = ((line != 0).argmax(axis=0))
    newline = line[::-1]
    # print(newline)
    last = len(newline) - 1*(newline != 0).argmax(axis=0)
    return first, last
def randomFlip(src):
    if random.randint(0, 1) ==1:
        src=cv2.flip(src,1)
    return src
def colorTransfer(content,style,ratio=0.5):
    if content.shape[0]>content.shape[1]:
        scaleRatio=content.shape[0]/min(style.shape[:2])
    else:
        scaleRatio=content.shape[1]/min(style.shape[:2])
    #
    style=cv2.resize(style[:,:,:3],None,fx=scaleRatio,fy=scaleRatio)
    print('style.shape,content.shape',style.shape,content.shape)
    style=style[:content.shape[0],:content.shape[1],:]
    assert style.shape==content.shape
    yuv = cv2.cvtColor(np.float32(style), cv2.COLOR_BGR2YUV)
    y, u, v = cv2.split(yuv)
    yuv2 = cv2.cvtColor(np.float32(content), cv2.COLOR_BGR2YUV)
    h, j, k = cv2.split(yuv2)

    hy=np.array((h*ratio+y*(1-ratio)),'uint8')
    #hy=np.clip(hy,0,255)
    content = np.dstack((hy,u,v))
    content = cv2.cvtColor(np.float32(content), cv2.COLOR_YUV2BGR)
    return content
if __name__=='__main__':
    content=cv2.imread('test/input.jpg')
    mask=cv2.imread('test/mask.jpg')
    content=mask
    mask=np.where(mask>100,7,0)[:,:,0]
    style=cv2.imread('testpic/afanda2.jpg')
    vt=vegetateTransClass()
    rc,img,des=vt.run(content,0,mask)

    print(rc)
    if list(rc.keys())[0] >= 200:
        print(des['name'])
        print(des['descriptions'])
        cv2.imwrite( "combine.jpg", img)