import os
import math

import cv2
import numpy as np

import paddle
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
import random
from paddleseg import utils
from paddleseg.core import infer
from paddleseg.utils import logger, progbar,visualize,load_entire_model

from paddleseg.transforms import transforms as T
from paddleseg.cvlibs import manager, Config
from PaddleSeg.contrib.CityscapesSOTA.models.mscale_ocrnet import *
import time

try:
	from ConfigCityscapes import resultCode
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
         ]

def preProcess(im,transforms):
	ori_shape = im.shape[:2]
	im, _ = transforms(im)
	im = im[np.newaxis, ...]
	im = paddle.to_tensor(im)
	return im,ori_shape

class cistyScaperClass():
	def __init__(self,
		debug=False,
		cfgModelPath1='PetModel/mscale_ocr_cityscapes_autolabel_mapillary_ms_val.yml',
		model_path1='PetModel/modelCityscape.pdparams',
		
	):
		self.debug=debug
		self.cfg = Config(cfgModelPath1)
		self.segModel=self.cfg.model
		utils.load_entire_model(self.segModel, model_path1)
		self.segModel.eval()
		##
		self.transforms = T.Compose([T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])])

		self.resultCode=resultCode
		
		self.classNums=19 #cityscape class nums

	#return image size chrome pic,pixel value from 0 to 17(class 0~ class7)
	def run(self,image):
		pred=[]
		try:
			t1=time.time()
			im,ori_shape=preProcess(image,self.transforms)
			print('seg time',time.time()-t1)
			t2=time.time()
			with paddle.no_grad():
				pred = infer.inference(
				self.segModel,
				im,
				ori_shape=ori_shape,
				transforms=self.transforms.transforms,)
				pred = paddle.squeeze(pred)
				pred = pred.numpy().astype('uint8')
			
			print('seg time',time.time()-t2)
		except Exception as e:
			print(e)
			return self.resultCode[7],pred
		return  self.resultCode[4],pred


def minimizeInput(img, size):
	ratio = size / max(img.shape[:2])
	img = cv2.resize(img, None, fx=ratio, fy=ratio)
	return img
if __name__=='__main__':
	seg=cistyScaperClass()
	im_path='testpic/jj6.jpg'
	im_path='testpic/test0.jpg'
	im=cv2.imread(im_path)
	im=minimizeInput(im, 800)
	rc,pred=seg.run(im)
	cv2.imwrite('pred.jpg',pred*10)
