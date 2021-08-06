
from PIL import ImageFont, ImageDraw, Image
import cv2
import numpy as np
# import moviepy.video.io.ImageSequenceClip
import time
import base64
# from triangulation import measure_triangle, affine_triangle, morph_triangle
def picpath2base64(image_path):
    #image_path = './test_image/test1.jpg'
    img_file = open(image_path, 'rb')
    img_b64encode = base64.b64encode(img_file.read())
    ##bytes 2 string
    return img_b64encode.decode('utf8')
def base64CV(img_raw_base64):
    #string 2 bytes
    img_b64decode = base64.b64decode(img_raw_base64.encode('utf8'))  # base64解码
    img_array = np.fromstring(img_b64decode, np.uint8)  # 转换np序列
    img_opencv = cv2.imdecode(img_array, cv2.IMREAD_COLOR)  # 转换Opencv格式 BGR
    return img_opencv
def landmarkCenter(landmark):
    # height=np.max(landmark[:,1])-np.min(landmark[:,1])
    # width=np.max(landmark[:,0])-np.min(landmark[:,0])
    center=[np.average(landmark[:16,0]),np.average(landmark[:16,1])]#+np.array([width,height])*bias
    scaleX=np.max(landmark[:16,0])-np.min(landmark[:16,0])
    return center,scaleX
def addWeight(fg,bg,ratio,mask=None,gamma=0):
    if mask is not None:

        #result=fg*mask/255*ratio+0*bg*ratio*(1-mask/255)+gamma
        result=fg*(mask/255)*ratio+bg*ratio*(1-mask/255)+gamma
        result=np.clip(result,0,255)
        #result=np.where(mask==255,np.clip(fg*alpha+bg*beta+gamma,0,255),bg)
    else:
        result=fg*ratio*0.5+bg*ratio*0.5+gamma
    return result
def headAngle(landmark):
    noseX=(landmark[30,0]+landmark[29,0])/2
    faceX=(np.sum(landmark[0:3,0])+np.sum(landmark[14:17,0]))/6
    return np.array([(faceX-noseX),0])
def resize(src,ratioX,ratioY,ratio):
    # mask = cv2.resize(mask, (int(src.shape[1] * ratio * ratioX), int(src.shape[0] * ratio * ratioY)))
    src = cv2.resize(src, (int(src.shape[1] * ratio * ratioX), int(src.shape[0] * ratio * ratioY)))
    return src
def mask3Channel(mask,src):
    maskPic = 255 * np.ones(src.shape, src.dtype)
    maskPic[:,:,0]=mask
    maskPic[:,:,1] = mask
    maskPic[:,:,2] = mask
    return maskPic
# def pasteTopLeft(dstLM,srcLM,srcHead,bias=[0,0]):

def pasteCenter(targetCenter,srcCenter,srcHead,bias=[0,0]):
    # targetCenter=landmarkCenter(dstLM)
    # srcCenter=landmarkCenter(srcLM)
    dy=(srcHead.shape[0]/2-srcCenter[1])
    dx=(srcHead.shape[1]/2-srcCenter[0])

    center=(int(targetCenter[0]+dx+bias[0]*srcHead.shape[1]), \
            int(targetCenter[1]+dy+bias[1]*srcHead.shape[0]))#(x,y)
    return center
def gradientMask(maskHead3,lowestValue=126,heightGradientBias=0.5):
    # gradient transparence of the head

    height=maskHead3.shape[0]
    for i in range(height) :
        # the value after linear gradient
        if i/height>heightGradientBias:
            afterGradient=int(255-(255-lowestValue)*(i-heightGradientBias*height)/(height*(1-heightGradientBias)))

            maskHead3[i,:,:] = np.where(maskHead3[i,:,:]==255,afterGradient,0)

    maskHead3=np.array(maskHead3,'uint8')
    maskHead3=np.clip(maskHead3,0,255)
    return maskHead3
def roiDst(dst,dstLM):
    x1=int(min(dstLM[:,0]))
    x2=int(max(dstLM[:,0]))
    y1=int(min(dstLM[:,1]))
    y2=int(max(dstLM[:,1]))
    center=(int((x1+x2)//2),int((y1+y2)//2))
    dstResult=dst[y1:y2,x1:x2,:]
    #fillConvexPoly need timeclock sort of points, -[x1,y1] is the bias of retangle
    points=np.concatenate((dstLM[:17,:],dstLM[17:27,:][::-1]), axis=0)-[x1,y1]#line[::-1]
    points=np.array(points,'int32')
    print('points',points)
    mask=np.zeros(dstResult.shape,dstResult.dtype)
    cv2.fillConvexPoly (mask,points, [255,255,255])
    # cv2.imwrite('img.jpg',im)
    return dstResult,center,mask
def roiHeadBody(srcBody,headLower,neckHeight):

    srcHead=srcBody[:headLower,:,:]
    assert neckHeight>srcHead.shape[0]#head should be smaller than body

    srcBody=srcBody[:neckHeight,:,:]

    return srcBody,srcHead
    # maskBody=maskBody[:neckHeight,:]
    # return srcHead ,maskHead,srcBody,maskBody
def calLandmarkLeftTop(dstLM,srcLMHead,preBias,headAngleBias,AngleBiasRatio=0.15):
    targetCenter,targetScaleX = landmarkCenter(dstLM)

    targetCenter=targetCenter+headAngleBias*AngleBiasRatio+np.array(preBias)*targetScaleX
    srcCenter,srcScaleX = landmarkCenter(srcLMHead)
    leftTop=targetCenter-srcCenter

    # print('targetCenter,srcCenter,leftTop',targetCenter,srcCenter,leftTop)
    return np.array(leftTop,'int32')

def noneZeroIndex(array_2D,axis):
    # array_2D = np.array(
    #     [[0, 0, 2, 3, 0, 4], [0, 0, 0, 0, 0, 0], [1, 0, 2, 3, 4, 0], [1, 0, 2, 3, 4, 9], [0, 0, 0, 0, 0, 0]])
    # axis = 1
    line = np.max(array_2D, axis)
    # print(line)
##
    first = ((line != 0).argmax(axis=0))
    newline = line[::-1]
    #print(newline)
    last =  - 1*(newline != 0).argmax(axis=0)
    return first, last


def roiAreaCheck(src,maskSrc,dst,leftTop):
    rightdown=[leftTop[0]+src.shape[1],leftTop[1]+src.shape[0]]
    #cal the area out of  dst. x1,y1 may ≥0。 x2,y2 may ≤0
    x1=-1*min(0,leftTop[0])
    y1=-1*min(0,leftTop[1])
    x2=min(0,dst.shape[1]-(leftTop[0]+src.shape[1]))
    y2=min(0,dst.shape[0]-(leftTop[1]+src.shape[0]))
    ##
    print('x1,x2,y1,y2', x1, x2, y1, y2)

    ##cut out the black area of mask
    temp=maskSrc[y1:y2+maskSrc.shape[0],x1:x2+maskSrc.shape[1]]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    temp = cv2.morphologyEx(temp, cv2.MORPH_OPEN, kernel)
    colFirst,colLast=noneZeroIndex(temp,0)
    rowFirst,rowLast=noneZeroIndex(temp,1)
    #cv2.imwrite('temp.jpg',temp)
    print('colFirst,colLast',colFirst,colLast)
    #
    x1+=colFirst
    x2+=colLast
    y1+=rowFirst
    y2+=rowLast
    #
    leftTop=np.array([x1+leftTop[0],y1+leftTop[1]])
    rightdown=np.array([rightdown[0]+x2,rightdown[1]+y2])

    maskSrc = maskSrc[y1:y2 + maskSrc.shape[0], x1:x2 + maskSrc.shape[1]]
    src=src[y1:y2+src.shape[0],x1:x2+src.shape[1],:]
    #print('x1,x2,y1,y2', x1, x2, y1, y2, src.shape,maskSrc.shape,rightdown-leftTop)
    return src,maskSrc,leftTop,rightdown,x1,x2,y1,y2
def leftTop2Center(leftTop,src):
    center=(int(round (leftTop[0]+src.shape[1]/2)),int(round(leftTop[1]+src.shape[0]/2)))

    return center
def hardPaste(dstOri,newleftTop,newrightDown,maskHead3,srcHead):
    hardPaste1=dstOri[newleftTop[1]:newrightDown[1],newleftTop[0]:newrightDown[0],:]
    hardPaste1=np.where(maskHead3==255,srcHead,hardPaste1)
    dstOri[newleftTop[1]:newrightDown[1],newleftTop[0]:newrightDown[0],:]=hardPaste1
    return dstOri
def flipFace(headAngleBias,sideThreshold,srcLM,srcBody,srcLMHead,srcHead):
    if headAngleBias[0]>sideThreshold:## face to left-hand side
        srcBody=cv2.flip(srcBody,1)
        srcHead = cv2.flip(srcHead, 1)
        srcLM[:,0]=srcBody.shape[1]-srcLM[:,0]
        srcLMHead[:,0]=srcHead.shape[1]-srcLMHead[:,0]
    return srcLM,srcBody,srcLMHead,srcHead
def splitMask(src):
    bgr=src[:,:,:3]
    transparent=src[:,:,3]
    return transparent,bgr
def saveGif(imgList,outputPath,fps=4):
    import imageio
    frames=[cv2.cvtColor(img,cv2.COLOR_BGR2RGB) for img in imgList]
    imageio.mimsave(outputPath+'dt.gif', frames, 'GIF', duration=1/fps)
def combineImg(front,background,pos,flip):
    if flip<2:
        front=cv2.flip(front,flip)
    x,y=pos
    height,width=front.shape[:2]
    mask=np.zeros((front.shape[0],front.shape[1],3),front.dtype)
    mask[:,:,0]=front[:,:,3]
    mask[:,:,1]=front[:,:,3]
    mask[:, :, 2] = front[:, :, 3]
    img=front[:,:,:3]
    result=background.copy()
    x1=max(0,int(x-width/2))
    x2=min(int(x+width/2),background.shape[1])
    y1=max(0,int(y-height/2))
    y2=min(int(y+height/2),background.shape[0])
    print(img[:y2-y1,:x2-x1,:].shape,result[y1:y2,x1:x2,:].shape,mask[:y2-y1,:x2-x1,:].shape)
    result[y1:y2,x1:x2,:]=\
        np.where(mask[:y2-y1,:x2-x1,:]>50,img[:y2-y1,:x2-x1,:],result[y1:y2,x1:x2,:])
    return result


def drawText(img,text,position,fontSize):
    ## Use simsum.ttc to write Chinese.
    fontpath = "resource/kaiu.ttf"  # <== 这里是宋体路径
    # fontpath= u"simsun.ttc"
    font = ImageFont.truetype(fontpath, fontSize)
    img_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(img_pil)
    draw.text(position, text, font=font, fill=(0, 0, 0,0))
    img = np.array(img_pil)
    # cv2.imwrite('drawtext.jpg',img)
    return img

def morph_mouth_close1( src_img, src_points, dst_img, dst_points, alpha=1):
    morph_points = []
    res_img = -1 * np.ones(src_img.shape, src_img.dtype)
    #    cv2.imshow('src_img',src_img)
    #    cv2.imshow('dst_img',dst_img)
    # print('src_img',src_img)
    src_img = src_img.astype(np.float32)
    dst_img = dst_img.astype(np.float32)
    # print('src_imgxx',src_img)

    #    cv2.imshow('src_imgssss',src_img)
    #    cv2.imshow('dst_imgssss',dst_img)
    #    cv2.waitKey(0)

    #        alpha = 0.8
    beginPoint=48#只调嘴
    for i in range(beginPoint, len(src_points)):
        x = (1 - alpha) * src_points[i][0] + alpha * dst_points[i][0]
        y = (1 - alpha) * src_points[i][1] + alpha * dst_points[i][1]
        morph_points.append((x, y))
    ##

    dt = measure_triangle(src_img, morph_points)
    alpha = 0.75
    for i in range(0, len(dt)):
        t1 = []
        t2 = []
        t = []

        for j in range(0, 3):
            t1.append(src_points[dt[i][j]])
            t2.append(dst_points[dt[i][j]])
            t.append(morph_points[dt[i][j]])
        # print( t)
        morph_triangle(src_img, dst_img, res_img, t1, t2, t, alpha)
        ##调试时打开
    #        self.DebugOutput(res_img,src_img,dst_points,src_points)

    mask_img=np.where(res_img==-1,0,255)
    res_img=mask_img.copy()
    res_img=np.array(res_img,dtype='uint8')
    # print('res_img',res_img.shape,np.max(res_img))
    mouthh = int((src_points[56, 1] + src_points[58, 1] - src_points[50, 1] - src_points[52, 1]) /5)
    res_img=cv2.line(res_img,(src_points[48][0],src_points[48][1]),
                     (src_points[54][0],src_points[54][1]),[0,0,0],thickness=mouthh)

    return res_img,mask_img
def morph_mouth_close( src_img, src_points):
    morph_points = []
    res_img =np.array(255*np.ones(src_img.shape), src_img.dtype)
    mask_img=np.zeros(src_img.shape, src_img.dtype)
    # src_img=np.array(src_img,dtype=np.uint8)[:,:,0]


    mask_img=cv2.fillConvexPoly(mask_img, src_points[48:60,:], (255, 255, 255))
    arr=np.sum(mask_img[:,:,0],axis=1)
    beginH=(arr!=0).argmax(axis=0)
    arr=np.flipud(arr)
    endH=len(arr)-(arr!=0).argmax(axis=0)
    mouthh = int((endH-beginH)/4)
    # cv2.imwrite(str(mouthh)+'res_img.jpg', res_img)
    res_img=cv2.line(res_img,(src_points[48][0],src_points[48][1]),
                     (src_points[54][0],src_points[54][1]),[0,0,0],thickness=mouthh)
    # cv2.imwrite('res_img1.jpg', res_img)
    res_img=np.where(mask_img>0,res_img,src_img)
    return res_img,mask_img
def roiChoice(landmarks,img,perspect_size):
    if img.shape[0] >= 256 and img.shape[1] >= 256:
        area = []
        mid_x = []
        mid_y = []
        width = []
        height = []
        for ii, landmark in enumerate(landmarks):
            landmark_array = np.array(landmark)
            width.append(np.max(landmark_array[:, 0]) - np.min(landmark_array[:, 0]))
            height.append(np.max(landmark_array[:, 1]) - np.min(landmark_array[:, 1]))
            mid_x.append(int((np.max(landmark_array[:, 0]) + np.min(landmark_array[:, 0])) / 2))
            mid_y.append(int((np.max(landmark_array[:, 1]) + np.min(landmark_array[:, 1])) / 2))
            area.append(width[ii] * height[ii])
        index = area.index(max(area))
        ratio = 256 / 3 / width[index]  ## 1/3 width of pic may seen look better
        roi_img = cv2.resize(img, (0, 0), fx=ratio, fy=ratio)
        landmark = landmarks[index]
        mid_x = mid_x[index]
        mid_y = mid_y[index]
        x_begin = max(0, int(ratio * mid_x - 128))
        x_end = min(roi_img.shape[1], int(perspect_size - (ratio * mid_x - x_begin) + ratio * mid_x))
        y_begin = max(0, int(ratio * mid_y - 128))
        y_end = min(roi_img.shape[0], int(perspect_size - (ratio * mid_y - y_begin) + ratio * mid_y))
        roi_img = roi_img[y_begin:y_end, x_begin:x_end, :]
    else:
        roi_img = cv2.resize(img, (256, int(img.shape[0] * 256 / img.shape[1])))
    return roi_img

def makeMovie(imgList,outputPath='',fps=4):

    clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(imgList, fps=fps)
    path=outputPath+'video'+str(time.time())+'.mp4'
    clip.write_videofile(path)
    return path