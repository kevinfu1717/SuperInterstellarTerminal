import paddlehub as hub
import cv2
import numpy as np
import os
#os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
##
resultCode=[{99:'运行报错'},
         {100:'dst发送的图片异常'},
         {101:'dst发送的图片太小'},
         {102:'图片人脸角度太偏'},
         {200: 'success'},
         {98: 'charterIndex越界'},
         {103: 'mask图片异常'},
         {201: '不用处理'},
         ]
##
class sandClass():
    def __init__(self,stylePath='VegPic/sand.jpg',modelPath='msgnet',inputGray=True):
        self.model = hub.Module(name='msgnet')
        self.model = hub.Module(directory=modelPath)
        self.stylePath=stylePath
        self.environmentDict={'name':'沙兽族建筑',
                             'descriptions':['沙兽族居住在流沙建造的建筑中，他们通过技术把这些建筑隐藏成普通的人类房子。他们也很少走出他们的房子。'],
                             }
        self.inputGray =inputGray
        self.resultCode=resultCode
        self.maskIndex=2#building in cityscape
    def run(self,image,mask=[]):
        return self.process(image,mask)
        
    def process(self,image,mask=[]):
        try:
            image=np.array(image,'uint8')
            dic={}

            result = image.copy()
            if self.inputGray:
                content = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                content = cv2.cvtColor(content, cv2.COLOR_GRAY2BGR)


            ## mask process
            if len(mask)==0:
                rowFirst=0
                rowLast = content.shape[0]+1
                colFirst=0
                colLast = content.shape[1]+1
            else:
                if len(mask.shape)==3:
                    rowFirst, rowLast = noneZeroIndex(mask[:,:,0], 1)
                    colFirst, colLast = noneZeroIndex(mask[:,:,0], 0)
                    mask=mask[:,:,0]
                    mask = np.where(mask == self.maskIndex, 1, 0)
                elif len(mask.shape)==2:
                    rowFirst, rowLast = noneZeroIndex(mask, 1)
                    colFirst, colLast = noneZeroIndex(mask, 0)
                    mask = np.where(mask == self.maskIndex, 1, 0)
                else:
                    return resultCode[7],image,[]
            ## area match
            #cv2.imwrite(str(np.sum(mask))+'testmask.jpg',mask*255)
            if np.sum(mask)>0:
                print('content,mask',content.shape,mask.shape,rowFirst,rowLast,colFirst,colLast)
                #
                data = self.model.predict([content[rowFirst:rowLast,colFirst:colLast,:]], style=self.stylePath, visualization=False)[0]
                
                #print('enviro process',data.shape,mask.shape)
                #由正方形输出拉回原来图像比例
                result[rowFirst:rowLast,colFirst:colLast,:]=cv2.resize(data,(colLast-colFirst,rowLast-rowFirst),3)
                print('result',result.shape)
                if len(mask)>0:
                    result[:, :, 0] = np.where(mask == 1, result[:, :, 0], image[:, :, 0])
                    result[:, :, 1] = np.where(mask == 1, result[:, :, 1], image[:, :, 1])
                    result[:, :, 2] = np.where(mask == 1, result[:, :, 2], image[:, :, 2])
                rcAll=self.resultCode[4]
                dic=self.environmentDict
            else:
                print('area not match for sand')
                rcAll=self.resultCode[7]
            return rcAll,result,dic
        except Exception as e:
            print(e)
            print('文件', e.__traceback__.tb_frame.f_globals['__file__'])
            print('行号', e.__traceback__.tb_lineno)
            return resultCode[0],[], {}
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
if __name__=='__main__':
    testImgPath = 'test/input.jpg'
    mask=cv2.imread('test/mask.jpg')
    image = cv2.imread(testImgPath)
    image=mask
    mask=np.where(mask>100,2,0)

    sc=sandClass()
    rc,result,des=sc.run(image,mask)
    if list(rc.keys())[0]>=200:
        print(rc)
        print(des['name'])
        print(des['descriptions'])
        cv2.imwrite('result.jpg',result)
