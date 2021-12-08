
import os
import math

import cv2
import numpy as np
import paddle
import random
# from CityscapesModule import cistyScaperClass
from ConfigPet import config as configAlienPet

paddle.disable_static()
try:
    from ConfigPet import resultCode
except:
    resultCode=[{99:'运行报错'},
         {100:'dst发送的图片异常'},
         {101:'dst发送的图片太小'},
         {102:'图片人脸角度太偏'},
         {200: 'success'},
         {98: 'charterIndex越界'},
         {98: 'charterIndex越界'},         
         {103:'分割失败'},        
         {104:'没有试合区域存在alien'},
         {201: '没有试合区域存在alien pet'},
         ]

class alienPetClass():
    def __init__(self,
    petPicPath,
    areaThreshold=10000,
    configAlienPet=configAlienPet,
    debug=False):

        self.debug=debug
        self.alienDict=configAlienPet['alien']        
        self.resultCode=resultCode
        self.petPicPath=petPicPath
        self.areaThreshold=10000 # pixel of the area, area should be large enough, 
        # print('petPicPath:',petPicPath,'alienDict,',(self.alienDict))

    def checkClassArea(self,pred,classNums):
        ##检查cityscape的分割结果是否可以满足某个 classID的外星生物出现
        classArea=[]
        classOkArea={}
        
        for index in range(classNums):
            temp=np.argwhere(pred==index)
            classArea.append(temp)
            if len(temp)>self.areaThreshold:##  pixel number of area is large enough? 符合出现的区域要足够大

                classOkArea[index]=temp
        #生成key为外星生物id，value为可该外星生物可出现的区域的dict
        return classOkArea

    def chooseCheckAlien(self,alienIndex,classOkArea):
        #根据alienIndex，及可出现的外星生物区域dict， 选择出现的外星生物

        #print(type(classOkArea),classOkArea.keys())
        #list of the index of area in the image
        imgAreaList=np.array(list(classOkArea.keys()),'uint8')
        print('imgAreaList',imgAreaList)
        alienIndexList=[]
        ## alienindex=0 则 random alien pet 
        if alienIndex==0:          
            alienIndexList=list(self.alienDict.keys())
            random.shuffle(alienIndexList)
        ##specified index of alien pet   
        else:
            alienIndexList=[alienIndex]
        # find the match alien in the area:
        print('alienIndexList=',alienIndexList)
        for al in alienIndexList:
            areaIndex=self.alienDict[al]['areaIndex']
            #print('self.alienDict[al][',self.alienDict[al]['areaIndex'])
            if areaIndex in imgAreaList:
                return al,areaIndex
        return -1,-1

    def process(self,image,pred,classNums,alienIndex):
        #
        #rc,pred=self.seg.run(image)
        # print(list(rc.keys())[0],'begin add pet',alienIndex)
        try:
            classOkArea=self.checkClassArea(pred,classNums)
            #print('classOkArea',list(classOkArea.keys()))
            alienIndex,areaIndex=self.chooseCheckAlien(alienIndex,classOkArea)
            print('alienIndex,areaIndex',alienIndex,areaIndex)
            if alienIndex>0:
                print('alienIndex:',self.alienDict[alienIndex])
                print('read pic:',os.path.join(self.petPicPath,self.alienDict[alienIndex]['picPath']))
                src=cv2.imread(os.path.join(self.petPicPath,self.alienDict[alienIndex]['picPath']))
                ## random flip
                src=randomFlip(src)
                scaleRatio=float(self.alienDict[alienIndex]['scaleRatio'])
                assert len(src.shape)>2
                assert scaleRatio>0
                assert scaleRatio<1
                # 是否用mixclone，which seamlessclone method to use
                mixclone=self.alienDict[alienIndex]['mixTimes']

                # adjust the size of src(alien) depend on the user`s image
                if src.shape[0]<src.shape[1]:

                    srcRatio=min(image.shape[:2])*scaleRatio/src.shape[0]
                else:
                    srcRatio=min(image.shape[:2])*scaleRatio/src.shape[1]
                ## 随机大小 0.8~1
                srcRatio*=random.uniform(0.8, 1)
                ## 对src图片进行缩放
                src=cv2.resize(src,None,fx=srcRatio,fy=srcRatio)
                print('mix_clone =',mixclone,'src newsize',src.shape)
                
                #可根据实际效果调整dilateratio的值
                dilateRatio=0.1
                if mixclone==1:
                    dilateRatio+=0.1
                # 
                leftTop=cloneLeftTop(pred,src,areaIndex,dilateRatio)

                #
                if len(leftTop)>0:
                    print('leftTop',leftTop)
                    #
                    if mixclone>0:
                        # src（外星pet图像）整个复制，复制进去将是一个正方形或长方形的图用于粘贴到底图
                        maskSrc=255*np.ones(src.shape,src.dtype)
                    else:
                        # src图像（外星pet图像）中，亮度超过threshold的会变透明,其他非透明部分会用于粘贴到底图
                        maskSrc=maskOfWhiteBG(src,threshold=240)
                    #maskSrc=255*np.ones(src.shape,src.dtype)
                    print('maskSrc',maskSrc.shape)
                    src,maskSrc,leftTop,rightdown,x1,x2,y1,y2=roiAreaCheck(src,maskSrc,image,leftTop)

                    center=leftTop2Center(leftTop,src)
                    if self.debug:
                        cv2.imwrite('src.jpg',src)
                        cv2.imwrite('maskSrc.jpg',maskSrc)
                    print('center',center,'maskSrc',maskSrc.shape)

                    #print(src.dtype,image.dtype,maskSrc.dtype)
                    if mixclone>0:

                        #combine=cv2.seamlessClone(maskSrc,image,maskSrc,center,cv2.NORMAL_CLONE)
                        combine=cv2.seamlessClone(src,image,maskSrc,center,cv2.MIXED_CLONE)

                    else:

                        combine=cv2.seamlessClone(src,image,maskSrc,center,cv2.NORMAL_CLONE)


                    if self.debug:
                        cv2.imwrite('combine.jpg',combine)
                        cv2.imwrite('mask'+str(areaIndex)+'.jpg',np.where(pred==areaIndex,255,0))
                    if self.alienDict[alienIndex]['mask']==1:
                        print('combine',combine.shape,image.shape)
                        # 根据pred 图像中的index，符合出现的areaindex的像素点，则用合成图combine的颜色 否则用image图的颜色
                        combine[:,:,0]=np.where(pred==areaIndex,combine[:,:,0],image[:,:,0])
                        combine[:,:,1]=np.where(pred==areaIndex,combine[:,:,1],image[:,:,1])
                        combine[:,:,2]=np.where(pred==areaIndex,combine[:,:,2],image[:,:,2])

                    return self.resultCode[4],combine,self.alienDict[alienIndex]

            return self.resultCode[8],image,{}
        except Exception as e:
            print('alien pet module error:',e)
            print('文件', e.__traceback__.tb_frame.f_globals['__file__'])
            print('行号', e.__traceback__.tb_lineno)
        
            return self.resultCode[0],image,{}
            
    def run(self,image,classMask,classNums,alienIndex=0):      #index=0 is random
        image=np.array(image,'uint8')
        if alienIndex<0 or alienIndex>len(self.alienDict):
            print('alienIndex not correct',alienIndex)
            return self.resultCode[5],image,{}
        
        return self.process(image,classMask,classNums, alienIndex)

def leftTop2Center(leftTop,src):
    # 根据左上角点，换算回中心点
    center=(int(round(leftTop[0]+src.shape[1]/2)),int(round(leftTop[1]+src.shape[0]/2)))

    return center
def randomFlip(src):
    if random.randint(0, 1) ==1:
        src=cv2.flip(src,1)
    return src
def erode2LeftTop(srcSize,pred,areaIndex,ratio=1):
    leftTop=[]
    ## erode核，看效果定义ratio
    kernel=np.ones((int(ratio*srcSize[0]),int(ratio*srcSize[1])),np.uint8)
    ##
    if kernel.shape[0]%2==0:
        kernel=kernel[:kernel.shape[0]-1,:]
    if kernel.shape[1]%2==0:
        kernel=kernel[:,:kernel.shape[1]-1]
    predMask=np.where(pred==areaIndex,1,0)
    #
    predMask[:,0]=0
    predMask[:,-1]=0
    predMask[0,:]=0
    predMask[-1,:]=0
    predMask=np.array(predMask,'uint8')
    
    print(predMask.shape,kernel.shape)
    # erode后的作为mask
    stay=cv2.erode(predMask,kernel)

    predStay=np.argwhere(stay==1)#[y,x]
    print('predStay',len(predStay))
    if len(predStay)>0:
        
        ars=predStay[random.randint(0,len(predStay)-1)]
        leftTop=np.array([ars[1]-srcSize[1],ars[0]-srcSize[0]],'int32')# [x,y]
    return leftTop

def dilate(predMask,areaIndex,ratio=1):
    # 封装dilate，确保dilate的kernel是奇数，防止报错
    kernel=np.ones((int(ratio*predMask.shape[0]),int(ratio*predMask.shape[1])),np.uint8)
    ##
    if kernel.shape[0]%2==0:
        kernel=kernel[:kernel.shape[0]-1,:]
    if kernel.shape[1]%2==0:
        kernel=kernel[:,:kernel.shape[1]-1]
    return cv2.dilate(predMask,kernel)

def cloneLeftTop(pred,src,areaIndex,dilateRatio=0.1): 
    #
    leftTop=[]
    #print('srcSize',src.shape)
    srcSize=np.array(src.shape[:2],'int32')


    leftTop=erode2LeftTop(srcSize,pred,areaIndex,ratio=1)
    if len(leftTop)==0:
        pred2=dilate(pred,areaIndex,ratio=dilateRatio)
        leftTop=erode2LeftTop(srcSize,pred2,areaIndex,ratio=1)
    return leftTop

def maskOfWhiteBG(img,threshold=240):
    maskResult=np.zeros(img.shape,img.dtype)
    #转到hsv空间检测亮度
    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    vv=hsv[:,:,2]
    r1=max(vv.shape[0]//60,1)
    r2=r1+vv.shape[0]//4
    if r1//2==0:r1+=1
    if r2//2==0:r2-=1
    #bl为亮度超过threshold的mask图像
    ret,bl=cv2.threshold(vv,threshold,255,cv2.THRESH_BINARY_INV)
    print('bl',bl.shape,r1,r2)
    
    # 开闭运算 去除mask中的很小很碎的杂点，根据情况看是否使用
    mask = cv2.morphologyEx(bl, cv2.MORPH_OPEN,
                            cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (r1, r1))
                            )

    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE,
                            cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (r2, r2))
                            )
    maskResult[:,:,0]=mask
    maskResult[:,:,1]=mask
    maskResult[:,:,2]=mask
    print('final mask',mask.shape)
    return np.array(mask,'uint8')

def noneZeroIndex(array_2D,axis):
    # 从图像中截取非0区域的pixel起始，与结束位置
    # array_2D = np.array(
    #     [[0, 0, 2, 3, 0, 4], [0, 0, 0, 0, 0, 0], [1, 0, 2, 3, 4, 0], [1, 0, 2, 3, 4, 9], [0, 0, 0, 0, 0, 0]])
    # axis = 1
    line = np.sum(array_2D, axis)
    first = ((line != 0).argmax(axis=0))
    newline = line[::-1]
    # print(newline)
    last =  - 1*(newline != 0).argmax(axis=0)
    return first, last

def roiAreaCheck(src,maskSrc,dst,leftTop):
    ## 计算外星pet图像粘贴到底图时，超出底图的部分将被裁走
    rightdown=[leftTop[0]+src.shape[1],leftTop[1]+src.shape[0]]
    #cal the area out of  dst. x1,y1 may ≥0。 x2,y2 may ≤0
    x1=-1*min(0,leftTop[0])
    y1=-1*min(0,leftTop[1])
    x2=min(0,dst.shape[1]-(leftTop[0]+src.shape[1]))
    y2=min(0,dst.shape[0]-(leftTop[1]+src.shape[0]))
    ##
    #print('x1,x2,y1,y2', x1, x2, y1, y2)

    ##cut out the black area of mask
    if len(maskSrc.shape)==2:
        temp=maskSrc[y1:y2+maskSrc.shape[0],x1:x2+maskSrc.shape[1]]
    else:
        #print('len(maskSrc),',len(maskSrc))
        temp=maskSrc[y1:y2+maskSrc.shape[0],x1:x2+maskSrc.shape[1],0]
    #print('temp',temp.shape)
    rowFirst,rowLast=noneZeroIndex(temp,1)
    colFirst,colLast=noneZeroIndex(temp,0)
    #
    x1+=colFirst
    x2+=colLast
    y1+=rowFirst
    y2+=rowLast
    #
    leftTop=np.array([x1+leftTop[0],y1+leftTop[1]])
    rightdown=np.array([rightdown[0]+x2,rightdown[1]+y2])
    if len(maskSrc.shape)==2:
        maskSrc = maskSrc[y1:y2 + maskSrc.shape[0], x1:x2 + maskSrc.shape[1]]
    else:
        maskSrc = maskSrc[y1:y2 + maskSrc.shape[0], x1:x2 + maskSrc.shape[1],:]
    src=src[y1:y2+src.shape[0],x1:x2+src.shape[1],:]
    #print('x1,x2,y1,y2', x1, x2, y1, y2, src.shape,maskSrc.shape,rightdown-leftTop)
    return src,maskSrc,leftTop,rightdown,x1,x2,y1,y2

if __name__=='__main__':
    image=cv2.imread('testpic/wyf.jpg')
    mask = cv2.imread('testpic/wyf.jpg')

    mask = cv2.cvtColor(mask,cv2.COLOR_BGR2GRAY)
    if len(mask.shape)==3:
        mask=mask[:,:,0]
    mask = np.where(mask > 100, 11, 0)


    vt=alienPetClass(petPicPath='PetPic/')
    rc,img,des=vt.run(image,mask,18,alienIndex=10)
    print(rc)
    if list(rc.keys())[0]>=200:

        print(des['name'])
        print(des['descriptions'])
        cv2.imwrite( "combine.jpg", img)


