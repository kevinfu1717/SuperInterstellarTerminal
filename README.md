# 星际终端 Super Interstellar Terminal
超级星际终端——A Wechat Social Game with AR and LBS


   - **A. 项目介绍**
   
		整体项目简述

   - **B. 故事背景**

		这个项目/游戏所在的环境背景

   - **C. 技术功能介绍**

		主要的功能点及关键点技术介绍，具体代码较多请Fork后参见项目内脚本

   - **D. 上手及部署**

		快速建立一个轻社交，结合增强现实技术（AR）与位置服务（LBS）的微信聊天小游戏，也可以把外星世界生成器用在别的地方！

   - **E. 总结**


# A. 项目介绍

### A1. 一句话概述：


   - 结合Wechaty与PadddlePaddle的各种AI能力，建立一个基于 微信聊天的 **轻社交，结合增强现实技术（AR）+LBS(暂时只基于图像）的星际漂流瓶游戏。** 重新认识你身边的世界，其实早已与外星生命共存。
     
   - **欢迎小伙伴推荐地点及地点图片或直接加入本项目，可以先star或Fork跟踪更新进度**
   
      aistudio地址：[https://aistudio.baidu.com/aistudio/projectdetail/2230251)
      
  - 样例视频如下：（建议全屏观看）


[![Watch the video](https://raw.github.com/GabLeRoux/WebMole/master/ressources/WebMole_Youtube_Video.png)](https://www.bilibili.com/video/BV1hL411E79M?p=1&share_source=copy_web)

### A2. 太空漂流信息

—— **你可能收到来自一个未知星域发过来的漂流瓶，你也可以把你想抒发的情感发向星际中**

   - 嗨，别来无恙啊，此刻的你是否有些孤独，别怕，此时此刻，在浩瀚宇宙中，总有与你相似的灵魂，你们或许来自不同的星球，有着不同的文明，但你们仍然可以通过太空漂流瓶去表达内心的情感，快来开启你的太空漂流瓶之旅吧......

   - 用户可以在加本官方微信好友后，向本官方微信发出包含文本与图片的漂流瓶。也可以主动接收漂流瓶。

   - 甚至，在一个你意想不到的时刻会收到想象之外的漂流瓶信息。发送与接收漂流瓶都可以提升等级噢！


                              

### A3. 增强现实技术（AR）+位置服务（LBS）的游戏

—— **接收漂流瓶任务，寻找身边潜藏的外星人、外星生物（宠物）、外星植物、外星建筑**

   - 基于微信聊天中的图片及文本聊天。通过文本接受到任务或主动触发。
   
   - 可能是让用户帮忙寻找它丢失的某个外星宠物（外星生物），或者帮它找到急需用于治疗的外星植物，也可能是让你帮忙找到正在被通缉的外星人囚犯。
   
<img src="https://ai-studio-static-online.cdn.bcebos.com/7b46c4366e7c47d1b6dc1f262aad801dc2da33b5d2ce41a3875135b8bdb2b2f3" width="700px" /> 

   
   - **更多的剧本、玩法， 请各位github或aistuido留言，让我们一起创造！记得要先点收藏（star）或 fork，持续关注更新**



# B. 故事背景

 - **地球并不只是人类的天下，其实有数万名外星人及其外星低等生物生活在我们当中，他们有的因为母星被毁有的因为星际战乱而选择到地球避难。**

 - **银河星际移民局则管理并协调着他们在地球的生活。借助超高级科技，他们隐藏原来的外观，装扮成是普通地球人，我们根本分辨不出来，说不定，站在你旁边的就是一位外星友人。**
 
  - **同时，他们也带来了外星的低等生物及外星植物，通过超科技把他们隐藏起来，装扮成地球物种或我们完全看不到。**


![](https://ai-studio-static-online.cdn.bcebos.com/2563c84006554d9eb73d758abac31b5f213213cc59d14ac580ab781dc8f98055)



  - 地球的外星人、在外太空星系的外星人都会通过自己的星际终端发送生活随想、求助、吐槽、愿望等漂流信息到太空中，向太空倾诉他们的心声，不确定谁会收到他们的漂流信息，也大部分是没有回复的。只是抒发他们的情感.更有部分通过这渠道发出他们的求助信息，渴望得到帮助。

  - 这些外星人，可能因为降落地球时失散了他们的外星人同伴，还有的可能失散了他们的外星宠物，这些外星宠物是他们星球的一些低等外星生物。外星人也像地球人爱护他们的宠物一样，非常紧张他们的外星宠物。希望能找回它的爱宠。还有的可能时急于找回一些外星植物，用以治疗他们的某种疾病。扫描这个二维码，打开你的超星际雷达吧！

# C. 项目中的技术功能介绍

## 1.AI寻找你身边的外星生物

###   建立外星人图鉴，让我们看一下AI预测的外星人形象是怎样的

**先看一下AI预测的外星生物矢量图：**

![](https://ai-studio-static-online.cdn.bcebos.com/438b037522e34dfeb968ee7fe74fb8fedda60ebb35e642dabe5d29d35a5298ee)


### A. 训练素材

 - 从百度爬取“外星人”的图片，但因为外星人搜出来的图太杂乱。所以改变思路，用关键词“外星人 矢量”来进行搜索爬取。搜出来的外星人图片相对没那么杂乱。勉强可以用来训练。勉强是有1/5左右是白底，有1/5左右是PS中那种透明图的格子底图或水印的，有1/5是背景各种颜色的图，还有1/5是多个外星元素组成的图。大概数据见下图：
    
![](https://ai-studio-static-online.cdn.bcebos.com/5c9a87a8d9b84f869348f3826e14bff61f374c51c49744a08afaa549f059adb0)

### B. 数据处理与增广

	
 - 尝试过用midars模型或CV来提取单个外星生物，但效果都不是很好。所以，最终只使用水平翻转，增加了一倍的数量。尽管可以爬取来增加这个数量，但越到后面，爬取的图片质量越差。所以还是通过水平翻转来处理。


### C. 模型

 - 训练文件： 见项目中 Train压缩包下 **TrainAlienPet.ipynb**	
 
 - 模型文件： 见项目中 Train压缩包下 **generator0725.params**	
 
 - 搜索了一下GAN的模型，结合可训练性与生成效果，选择了LSGAN。基于项目aistudio上“独楼望天涯”大佬的项目 [https://aistudio.baidu.com/aistudio/projectdetail/1936908?channelType=0&channel=0](http://) 进行修改。
 
 - 在其基础上，每个epoch执行更多的Generation，以及修改了超参数（ 偶尔判别器loss高时，会有些完全不像的图）.

 - 训练过程：**Epoch 0 ~ Epoch 999** 的LOSS及效果见下面动图：


![](https://ai-studio-static-online.cdn.bcebos.com/31a2ac1c84db410e861bdb6560d0666133d80a7600424bb6950c1fca717bfbb2)


 - **具体训练项目地址见**：
 
[Paddle2.0-通过LSGAN让我们看看AI预测的外星人长什么样子](https://aistudio.baidu.com/aistudio/projectdetail/2210138)

 - 不足：
1. 大概在200epochs就已经差不多，再训练到1000epochs反而效果还下降了。LOSS方面，判别器可以达到0.02，但生成器只能到0.8。这方面还可以优化
2. 最终会有不少彩色的杂点
3. 生成的外星生物矢量图有些还保留训练图的方格背景之类的。
4. 生成的外星生物可能有部分过拟合，为有些很向原来的。

### D. 后处理


—— 1. 在叠加到现实图像中做AR效果时，使用cv处理优化这部分（具体见3-d中的描述）

—— 2. 为外星生物配上背景介绍，定义他们出现的位置，建立外星生物图鉴

 - **外星生物图鉴：**


<img src="https://ai-studio-static-online.cdn.bcebos.com/2628476cfe6e4e20b20cfc01994e0065d6abce5bf1e541eb942fb2e07ebc181d" width="550px" />



## 2. 外星人显形  —— alienHeadModule.py

### a 模型

**Paddlehub landmark模型**

landmark的68个人脸关键点模型具体介绍请见官方介绍：

[https://gitee.com/PaddlePaddle/PaddleHub/tree/release/v2.1/modules/image/keypoint_detection/face_landmark_localization](https://gitee.com/PaddlePaddle/PaddleHub/tree/release/v2.1/modules/image/keypoint_detection/face_landmark_localization)

### b 作用

**实现外星人换脸**

### c 步骤

| 序号 | 步骤 | 操作|
| -------- | -------- | -------- |
| A   | 准备     | 1 找到一张外星人正面的照片与侧面的照片，扣出其形象保存图片。   |
|   |        |  2 我们需要手动用labelme的keypoint为其标上68个关键点，大概就好，不用太精确。landmark数据按labelme格式保存到json中。     |
|   |        |  3 配置外星人的人脸参数到ConfigHead.py中。     |


<img src="https://ai-studio-static-online.cdn.bcebos.com/f490f7061253473db493f1b17640d583082464fe8cb04393bfe6d8bd80fe1978" width="800px" /> 


| 序号 | 步骤 | 操作|
| -------- | -------- | -------- |
| B   | 对齐     | 1 对用户发来的图片，利用PaddleHub的landmark模型获取图片中的人脸特征点。   |
|   |        |  2 正脸使用正脸的外星人照片的，侧脸用侧脸的预处理照片。若角度太偏则不进行处理。然后，使用landmark中脸颊的特征点求中点进行人脸图像位置上的对齐。并根据用户图片的人脸对外星人人脸进行大小调整     |
| C   |  融合粘贴   |1. 截取外星人人脸，生成一个上到下的渐透明的遮罩图。用cv2.seamlessCloned 的NORMAL_CLONE复制到原人脸位置，但因为seamlessClone没法调参数的，外星人形象融在背景里面，不太明显不清晰。   |
|    |     |2. 截取外星人人脸及颈部及上半身，生成一个上到下的渐透明的遮罩图。用cv2.addWeight 把外星人脸与1中所述的人脸进行透明度融合   |


<img src="https://ai-studio-static-online.cdn.bcebos.com/0f7aff3f600f472481cf3c4b529e6e87ce3a868b2f8c41fbb31f60474eff1b95" width="700px" /> 


### d 关键技术点

#### d1. 问题分析

直接把外星人脸贴到用户图上边缘会很硬，如上图中的左图。

#### d2. 单方向渐变遮罩

使用从上到下的遮罩，可以有效渐变过度到身体。上到下的渐变mask生成见CVTools.py中的gradientMask（）。只用上到下的渐变
是因为外星人头会比正常人头大，本身过渡要求不高，所以上，左，右方向的融合过渡，依靠seamlessClone则可较好处理。剩下 下 这个方向是连接颈部或身体的需要渐变遮罩过渡。（见下图）

<img src="https://ai-studio-static-online.cdn.bcebos.com/6d784169f2004c948847bb0a76a7a2b4ea094635d1f14f6ca444760ee54cb544" width="120px" />

#### d3. 双重图片叠加融合

 - 只是使用seamlessClone融合，会因为seamlessClone算法影响，把贴上去的外星人图颜色变得较多，算法只为让其融合到附近环境。原图是这样的：

<img src="https://ai-studio-static-online.cdn.bcebos.com/0e204447d9014b50927aa97e01d2a9b9bca19825219d4446ad901d92bfff729a" width="120px" />

  - cv2.seamlessClone没有参数调节，使得整个外星人头的颜色都变了。见下图左。   双重图片叠加融合，效果见下图右。

<img src="https://ai-studio-static-online.cdn.bcebos.com/1a647812cbf5425c839a94d817e12d400c3c5960475c4ede9e57536804b4108a" width="800px" />

![]()



 - 双重图片叠加融合步骤：（具体代码为项目中：**alienHeadModule.py**)
 
| 序号 | 步骤 | 操作|
| -------- | -------- | -------- |
| 1   | 生成head的渐变mask   | 使用d2所述的方法生成头部的渐变遮罩）   |
| 2   | hard paste head   | 使用直接粘贴替换的方式，把外星人的head粘贴到用户的图的适当位置   |
|3  |   生成Body的渐变mask    |  把外星人头及颈部或身体上半部 对齐head的位置，使用d2所述的方法生成mask |
|4  |   seamlessClone Body    |  使用3所述的mask图，把外星人身体上半部seamlessClone到用户的图中，需要保证粘贴后头的位置是跟步骤2一样的 |
| 5 |   合成     |  使用cv2.addWeight实现透明度叠加步骤2与步骤4的图。 cv2.addWeighted(src1, alpha, src2, beta, gamma），根据不同外星人的皮肤深浅调节alpha，beta。最终效果见上图中|



## 3. 识别现场环境  —— CityscapesModule.py

### a.  模型

**PaddleSeg 中基于cityscapes数据集的SOTA模型**

PaddleSeg训练了一个在cityscapes数据集上SOTA的模型。却很低调，只是放在contrib中，仅有个英文的介绍。里面的介绍还主要针对训练的，如果只是想要体验SOTA的cityscapes的效果是怎样的却很麻烦。本项目中化简了相关的代码，一行代码体验cityscapes分割。效果真的对得起SOTA的！ 

### b.  相关文件

   - 目录结构：

		PetModel/

		CityscapesModule.py

   - 想单独使用本模块，只需拷贝上述文件，直接修改CityscapesModule.py中的im_path即可。

   - PetModel 中已包含了模型的yml文件，两个模型文件：pretrain.model文件（https://bj.bcebos.com/paddleseg/dygraph/cityscapes/ocrnet_hrnetw48_mapillary/pretrained.pdparams） ,以及model.pdparams文件（https://bj.bcebos.com/paddleseg/dygraph/cityscapes/mscale_ocr_hrnetw48_cityscapes_autolabel_mapillary/model.pdparams）


### c.  功能/作用


让AI能感知环境里有拿几样物品，同时可以定位到其在图片中的具体位置。
具体识别的物品如下：

( **PS:注意真实返回的ID是从0开始的，所以是trainId-1**,如sky实际返回的id是10 not 11）：

<img src="https://ai-studio-static-online.cdn.bcebos.com/cff349c273434fbd8b09b3df68afdea72b720add38a246ecab3be84c9c3f8f69" width="750px" />


### d.  使用


 - 运行CityscapesModule.py脚本,设好要处理图片的路径，将返回大小于原图片大小一样的二维数组pred，其取值是从0~18。
 
  - 可以拿这个二维数组作为mask，例如用np.where(mask == index ,1,0)来截取自己感兴趣的区域，index取值为上面c.表格中的 trainID -1。 
  
  - CityscapesModule.py中把pred ×10后保存成图片，图片像素的灰度值从0~180,见右下图。


<img src="https://ai-studio-static-online.cdn.bcebos.com/80027212ce424aac88031b60c94d7009aabf5f85914744238722e00d300db2a1" width="600px" />




## 4. 寻找隐藏在环境中的外星生物（外星宠物）  —— alienPetModule.py


<img src="https://ai-studio-static-online.cdn.bcebos.com/cbd8b47bfac94d59bc09efe325d1602bdaeb1f30369349c3845dbd32f89708f8" width="600px" />


### a.  准备

   - 配合LSGAN生成的外星生物的形象，为起配置喜好，所在环境等，写入到ConfigPet.py中。
   - ConfigPet.py中每个dict就是一种外星生物，该外星生物的id就是那个dict的key。
   - ConfigPet.py中的areaIndex对应的就是cityScapes返回的物体ID，例如，areaIndex=10，则代表此生物是出现在天空中。


### b 作用

实现对应位置的叠加AR效果。如：天空中出现飞在天上的外星生物，树丛中会出现喜欢在树上的草食性外星生物。


### c 步骤

| 序号 | 步骤 | 操作|
| -------- | -------- | -------- |
| A   | 准备     | 1 基于LSGAN生成的外星生物矢量图。配置其参数，如：名字、大小、常出现的位置，习性描述、是否需要遮罩等   |
| A   | 选择     | 1 先判断alienIndex是0（随机生成），还是-1（不生成），或者是>0（生成id等于alienIndex的外星生物）。   |
| B  |   定位     |  1 基于分割模型得到的mask区域，按照外星生物可存在的位置判断是否出现外星生物，及其出现位置。具体见关键技术点说明.     |
| C  |   合成     |  1 根据外星生物的特性使用 cv2.seamleClone，参数选用 MIXED_CLONE 或 NORMAL_CLONE 。具体见关键技术点说明.  |


### d 关键技术点


#### d1. cv2.seamlessClone三种图像合成效果


   -  cv2.seamlessClone(src, dst, src_mask, center, cv2.NORMAL_CLONE)

 会把src图的边缘进行模糊化，同时整个src图的色彩融合到dst中==》需要src图较清晰，dst背景较简单，可以接受src图周边边缘模糊的场景
 
 
   -  cv2.seamlessClone(src, dst, src_mask, center, cv2.MIXED_CLONE)

 基于透明度的融合，src图中白色的区域会显得透明度高，看起来叠加的颜色比较透。==》适合dst背景较复杂，但对src图清晰度要求不高，src图背景是白色的场景

 
   -  cv2.seamlessClone(src, dst, src_mask, center, cv2.MONOCHROME_TRANSFER)

 会把src图变成灰度图合成到dst中==》暂时看不到什么好用途
 
 借用别人的图，懒得生成了,左中右分别是：NORMAL_CLONE, MIXED_CLONE,MONOCHROME_TRANSFER ：

**简单背景：**
 
<img src="https://ai-studio-static-online.cdn.bcebos.com/26f3028a7e404c2ca1ac9832ade2bde3a321b49cb0794d408e21ac3211f802b2" width="800px" />

**复杂背景：**


<img src="https://ai-studio-static-online.cdn.bcebos.com/37fecba19fcf4e578a4ea896bac4b4624e652bad0b7649cdb6b0bb17f5d2cd0d" width="800px" />


**效果好坏于背景图dst及前景图src都有关系**



#### d2. 结合mask的优化版seamlesClone图像合成效果—— 代码见alienPetModule.py中的maskOfWhiteBG() ，roiAreaCheck（）


| 步骤 | 步骤 | 说明 | 备注 |
| -------- | -------- | -------- |-------- |
| 1    | 把src的外星生物图转成HSV格式，通过V通道，V>200得到二值化的mask| HSV的V分量可以当作是亮度，在本次LSGAN生成的外星人中基本都是白色底的，可以抠处白色底     | |
| 2    | 二值化的图进行开运算| 去除LSGAN中生成的一些彩色噪声点，得到外星生物的mask，宁愿漏也不要去多了。因为合成时有个渐变，自然就把杂点淡化了     |![](https://ai-studio-static-online.cdn.bcebos.com/20950e724d264f6ca34121dab88ecf58fdfeddbaba1f4a32901c0c199af1565e)  |
| 3    | 把2中的二值化图进行边缘裁切，使mask图的四个边都有白色区域接触| 这可能是seamlessClone的一个bug，若白色区域不接触图像边缘，**其合成时的位置是按白色区域的中心点位置，不是mask图像的中心点位置**，切记！！！  | |
| 4    | 根据裁切后的mask，重新计算中心点左边center=(x,y)| seamlessClone的center参数是src的中心点在dst图中的位置  | |



#### d3. 结合cityScapes分割的AR定位——代码见alienPetModule.py中的erode2LeftTop（），leftTop2Center()


| 步骤 | 步骤 | 说明 | 备注 |
| -------- | -------- | -------- |-------- |
| 1    | 利用cityScapes返回的pred图中，获取画面中某个物品的mask     | 利用np.where(pred==areaIndex,1,0)生成二值化mask | |
| 2    | 根据用户图片dst的大小，及外星宠物的scaleRatio参数，调整外星宠物图片的大小| 大小设置为dst图像长边scaleRatio，再有一个（0.8~1）倍的随机    |  |
| 3    | 对二值化mask图4个边缘的值都设置0| 相当于mask图边缘多了一个黑色的框，方便待会腐蚀时，可以从边缘也腐蚀。否则，贴着边缘值为1的点待会都不会倍腐蚀  | |
| 4    | 以调整后的外星宠物图像的边长d，对二值化mask图像进行opencv的腐蚀操作。腐蚀后，值为1的点则为可选的外星宠物图像进行seamlessClone的center点| 腐蚀相当于我们的卷积，当该点腐蚀后仍为1，则证明其腐蚀前周围值为1的点能组成一个d×d的形状 | ![](https://ai-studio-static-online.cdn.bcebos.com/96098ab6711d49379a2a27725bcd42da0f03f413f0144fcbbbd99f2385bf9d25)|
| 5    | 若腐蚀后，mask图都为0，则缩小腐蚀的kernel为原来的0.6，再重复4的步骤| 步骤4完成后没能找到mask中为1的点则证明，没有足够位置完全把外星宠物图像放进去，我们缩小要求，要求某区域只要有60%的外星宠物的大小则继续融合进去 | |
| 6    | 若4或5步骤后，mask中有值为1的点，则满足条件,可进行图像合成|  | |


#### d4. 前后关系

 - 有外星人又则怎能少了外星飞碟呢。外星飞船要逼真需要又遮挡关系，我们可以利用cityscapesModule识别出的天空区域。
  - 一句代码实现遮挡：
  
【伪代码】 np.where(mask=天空的index,已叠加整个飞船的ar图，原图）

<img src="https://ai-studio-static-online.cdn.bcebos.com/194a64eb13334d778cd86dc6e7b1c39c2448903993ac4a8b8134080285e106d1" width="700px" /> 







## 5. 寻找生长在地球的外星植物  —— vegetateModule.py


<img src="https://ai-studio-static-online.cdn.bcebos.com/e91fac3b96d74180995b8b205ffcf6fc62c62abab03944fc9d5ce6f27ed57491" width="600px" />  

### a.  准备

找了一些外星植物的图片，实现非深度学习的基于**图像技术**的颜色纹理迁移


### b 作用

把环境中的植物变换成外星风格的植物


### c 步骤

| 序号 | 步骤 | 操作|
| -------- | -------- | -------- |
| A   | 准备     |  基于这些外星植物，在ConfigVegetae.py中配置其参数，如：名字、常出现的位置，习性描述等   |
| A   | 选择     |  先判断vegetateIndex是0（随机生成），还是-1（不生成），或者是>0（生成id等于vegetateIndex是0的外星植物）。   |
| B  |   定位     |   基于分割模型得到的mask区域，按照外星生物可存在的位置判断是否出现该外星植物，及其出现位置。    |
| C  |   合成     |   根据外星植物的特性使用yuv颜色通道合成。具体见关键技术点说明.  |


### d 关键技术点


#### d1. YUV颜色区间

   - 比较熟悉CV的同志们可以忽略此节

   - 我们使用CV的方法进行处理时，通常不会再RGB颜色空间处理，而是转到HLS/HSV 也有 YUV颜色空间进行处理。这样作的好处是 其中的H 通道在一定程度上可以表示其颜色。通过这样来选择特定的颜色，S代表饱和度，V代表亮度。而YUV中 Y是亮度，U,V分别是 蓝 红 通道。

   - YUV具体介绍可见： [https://zhuanlan.zhihu.com/p/95952096](https://zhuanlan.zhihu.com/p/95952096)

#### d2. YUV颜色融合

   - 我们也可以通过Y通道融合亮度，保留外星的U,V通道，即保留其颜色。当两个图片融合时，通过调节融合的Y通道的权重，控制合成出来的颜色亮度。

```
##把图片style，content转到yuv空间
    yuv = cv2.cvtColor(np.float32(style), cv2.COLOR_BGR2YUV)
    y, u, v = cv2.split(yuv)
    yuv2 = cv2.cvtColor(np.float32(content), cv2.COLOR_BGR2YUV)
    h, j, k = cv2.split(yuv2)
## 根据ratio这个比例来合成 style 与 content两张图
    hy=np.array((h*ratio+y*(1-ratio)),'uint8')
    #hy=np.clip(hy,0,255)
  ## 两张图进行合成
    content = np.dstack((hy,u,v))
    content = cv2.cvtColor(np.float32(content), cv2.COLOR_YUV2BGR)
```






## 6. 寻找被外星人隐藏起来的外星建筑  —— sandModule.py

<img src="https://ai-studio-static-online.cdn.bcebos.com/a2c9d5811fb64a8a9dfea2759e498e22f8fee5bcc5194c2e823aa28913d7b0c1" width="600px" />


### a.  准备


使用Msgnet迁移训练的沙画模型，实现基于**深度学习**的风格迁移。 大家可以对比一下5中的外星植物的效果，那是基于CV技术的迁移


### b 作用

把环境中的建筑变成像流沙组合起来的建筑


### c 步骤

| 序号 | 步骤 | 操作|
| -------- | -------- | -------- |
| 1  |   定位     |   基于分割模型得到的mask区域，定位areaIndex==2,即building的区域。    |
| 2  |   图像迁移     |  把建筑转成灰度图，然后用msgnet迁移成流沙的风格.  |


## 7. 使用ImgGenerateModule 建立Alien Server或直接调用

### 7.1 直接调用函数

	## ImgGenerateModule可以单独使用或 app.py也可单独建立flask的图像生成服务供其他用途使用
 
 - 1. 初始化函数定义各个模型文件夹及图片素材的位置

```
 imgGenerator = ImgGenerator(debug=False,
 	    ymlPathSeg='PetModel/mscale_ocr_cityscapes_autolabel_mapillary_ms_val.yml',#cityscapes分割模型的yml
 	    modelPathSeg='PetModel/modelCityscape.pdparams',#cityscapes分割模型文件
 	    modelPathSand='msgnet',#沙画模型文件夹
 	    picPathHead='HeadPic/',#外星人头素材
 	    picPathPet='PetPic/',#外星生物素材
 	    picPathVeg='VegPic')#外星植物及外星建筑素材
                   
```
 - 2. 调用函数生成
 
 输入是图片路径：
 
	 rc, img, des = imgGenerator.run(dstPath, alienHeadIndex=0, vegetateIndex=0,environmentIndex=0,  alienPetIndex=0)
 
 输入直接是图片：
 
	 rc, img, des = imgGenerator.runImg(img, alienHeadIndex=0, vegetateIndex=0,environmentIndex=0,  alienPetIndex=0)
  
 - 3. 参数说明
 
 |参数名|必选|类型|说明|
|:----    |:---|:----- |-----   |
|img/dstPath |是  |string |待处理图片或待处理图片的地址   |
|alienHeadIndex |否  |int | 是否进行换外星人头，-1为不处理，0为随机，>0为指定index为该值的外星人    |
|vegetateIndex     |否  |int | 	是否添加外星植物，-1为不处理，0为随机，>0为指定index为该值的外星植物    |
|environmentIndex |否  |int | 	是否生成外星建筑外墙，-1为不处理，>0为生成    |
|alienPetIndex     |否  |int | 	是否进行添加外星生物，-1为不处理，0为随机，>0为指定index为该值的外星生物   |
   
 - 4. 返回说明
 
|参数名|类型|说明|
|:-----  |:---|-----  |
|result_code |dict|{ 返回结果代号 ：返回结果描述}，result_code参数具体见代码中说明，200为正常生成 |
|img |numpy array|生成的图片或原图片(没有适合的位置生成时返回原图片) |
|dis |dict|，包含生成外星人/生成外星植物/生成外星建筑/生成外星宠物的参数的字典. 没有进行处理则为空字典 |
 

### 7.2 建server，访问图像生成接口 (本项目中使用的方式）
 
  不确定什么原因，以前wechaty都可以在AIstudio的脚本任务跑，现在好像不可以了，从AIstudio脚本任务无法访问外网的端口了，可以ping通外网。所以，需要另外找自己的主机作深度学习这部分的图片推理生成，因此直接把上述功能再弄到flask中，弄了个接口。

- 1.接口代码见：

      项目中的app.py脚本

- 2. 接口文档说明见showdoc：

[https://www.showdoc.com.cn/1525661816374166/7370335053618085](https://www.showdoc.com.cn/1525661816374166/7370335053618085)

             
 

# 8 识别图像的拍摄位置

## 8.1 前提条件（需同时满足下面条件）
 - 用户是在微信中，用**原图**发送照片给我们
  - 照片拍照时，其拍照设置中打开了**保存地理位置信息** 
  

## 8.2 背景情况介绍

 - 若用户满足上述2条件，则保存的照片里将含有exif信息。该EXIF信息，可在Windows中图片的属性中看到，GPS，拍照日期等信息：
  
<img src="https://ai-studio-static-online.cdn.bcebos.com/e93878056a6b41fbbe4889a7246128ae772d752115a64666ab1e857437a2cfbe" width="700px" />

 
  - EXIF的详细介绍可见，这里不详细叙述了： 
  
  [http://www.360doc.com/content/18/0303/07/7793103_733844932.shtml](http://www.360doc.com/content/18/0303/07/7793103_733844932.shtml)
 
 
## 8.3 获取经纬度—— exifModule.py

 - python中有pip库可以直接获取照片的exif信息， 具体代码可见项目工程中的exifModule.py.
  - 本脚本中提取了最关键的经度与纬度信息，还有拍照日期可供调用
  
  
## 8.3 获取具体位置—— geoModule.py

 - 具体代码可见项目工程中的geoModule.py.
  - 步骤：把获得的经纬度信息去请求开放的地图api，获取具体地址.这个方法的名称为：逆地址编码
  - 横向比较了： 百度，腾讯，高德地图，发现高德给出的个人免费调用量有 3W/日，其他两家只有几k。最终选用了高德的api
 - 高德api获取地址步骤（非常简单）：
 
| 序号 | 高德流程 | 备注|
| -------- | -------- | -------- |
| 1    | 注册     | 需要支付宝扫码实名     |
| 2    | 新建应用     | 按默认点确定即可     |
| 3    | 复制那个应用的key进行调用     | 调用代码见geoModule.py,请使用自己的gaode_key测试    |

详细图文描述可见：
[https://zhuanlan.zhihu.com/p/371682461](https://zhuanlan.zhihu.com/p/371682461)


 

# D.上手及部署指南

## D1. 配置要求

图像部分，因为用了PaddleSeg需要一台6G显存以上的主机，4G显存的没测试过，可以尝试调小 ImgGeneratorModule 中的 inputSize, 在DL处理前先缩小图片。


## D2. 部署方案

建议选择方案一

 - 方案一：一台显存6G，内存16G电脑（部署整个项目）
 - 方案二：一台普通云端服务器（1核2G之类的）+ 一台有外网IP的显存6G，内存16G电脑(部署图像部分：ImgGenerateModule)
 - 方案三：一台有GPU的云端服务器
 

 


## D3. 模型下载

需下载以下模型：

 - 简化后的PadlleSeg的cityscapes的SOTA模型:
 
   （CityscapesModule.py需要）
 
   AIstudio数据页：[https://aistudio.baidu.com/aistudio/datasetdetail/102892](https://aistudio.baidu.com/aistudio/datasetdetail/102892)
 
 
 - 流沙效果/沙画效果模型:
 
   （sandModule.py需要）
 
   AIstudio数据页：[https://aistudio.baidu.com/aistudio/datasetdetail/102698](https://aistudio.baidu.com/aistudio/datasetdetail/102698)

- PaddleSeg:

  （CityscapesModule.py需要）

   AIstudio数据页：[https://aistudio.baidu.com/aistudio/datasetdetail/102136](https://aistudio.baidu.com/aistudio/datasetdetail/102136)
 
  或直接去github： git clone https://github.com/PaddlePaddle/PaddleSeg   
 
  或者去gitee： git clone https://gitee.com/PaddlePaddle/PaddleSeg  

 
 - 生成外星人矢量图模型
 
   ( 非必需，若要自己新增生成外星生物才需要）：
 
   AIstudio数据页：[https://aistudio.baidu.com/aistudio/datasetdetail/103316](https://aistudio.baidu.com/aistudio/datasetdetail/103316)
 


## D4. 部署过程

 

1. 申请Wechaty Token [![Powered by Wechaty](https://img.shields.io/badge/Powered%20By-Wechaty-brightgreen.svg)](https://wechaty.js.org) [![Wechaty in Python](https://img.shields.io/badge/Wechaty-Python-blue)](https://github.com/wechaty/python-wechaty)

   具体请访问Wevhaty官网: [https://wechaty.js.org/](https://wechaty.js.org/)

2. 快速上手

   请参考我的文章: [教你用AI Studio+wechaty+阿里云白嫖一个智能微信机器人](https://aistudio.baidu.com/aistudio/projectdetail/1836012)

3. 云服务器

   - 本项目用到了阿里云的云服务器ECS，链接: [云服务器ECS](https://www.aliyun.com/product/ecs)

   - 购买实例后登录[控制台](https://ecs.console.aliyun.com)，实例名称和主机名可以自行更改，记住**公网IP**

   - 有任何不明白的请访问: [云服务器ECS官方文档](https://help.aliyun.com/product/25365.html)

4. 云数据库

   - 本项目用到了阿里云的云数据库RDS MySQL版，链接: [云数据库RDS MySQL版](https://www.aliyun.com/product/rds)

   - 购买实例后登录[控制台](https://rds.console.aliyun.com)，创建一个数据库，名为`drift-bottle-in-space`

   - 创建一个普通账号，授权数据库填写`drift-bottle-in-space`，权限为读写（DDL+DML），记住**用户名**和**密码**

   - 在左侧**数据库连接**处找到外网地址，小本本记下来
   
   - 设置白名单，将云服务器实例的**公网IP**加入白名单

   - 有任何不明白的请访问: [云数据库RDS官方文档](https://help.aliyun.com/product/26090.html)

5. 云存储

   - 本项目用到了阿里云的对象存储OSS，链接: [对象存储OSS](https://www.aliyun.com/product/oss)

   - 开通后登录[控制台](https://oss.console.aliyun.com)，创建一个Bucket，名为`drift-bottle-in-space`

   - 登录[RAM控制台](https://ram.console.aliyun.com)，创建一个用户，访问方式选择**编程访问**，记住`AccessKey ID`和`AccessKey Secret`

   - 有任何不明白的请访问: [云存储OSS官方文档](https://help.aliyun.com/product/31815.html)

6. 克隆本代码仓库

   以任何一种你喜欢❤的方式远程登陆到云服务器

   ```bash
   $ git clone https://github.com/Lovely-Pig/drift-bottle-in-space.git
   ```

7. 安装MySQL客户端

   ```bash
   $ sudo apt install mysql-client-core-8.0
   ```

8. 设置环境变量

   endpoint的设置可参考: [访问域名（Endpoint）](https://help.aliyun.com/document_detail/31837.html?spm=a2c4g.11186623.6.611.554e6d13isyAAt)
   
   ```bash
   $ export HOST="<your host>"    # 云数据库的外网地址
   $ export USER="<your user name>"    # 云数据库账号的用户名
   $ export PASSWORD="<your password>"    # 云数据库账号的密码
   $ export DATABASE="<your database name>"    # 云数据库的数据库名，填写为drift-bottle-in-space
   $ export ACCESS_KEY_ID="<your AccessKey ID>"    # RAM用户的AccessKey ID
   $ export ACCESS_KEY_SECRET="<your AccessKey Secret>"    # RAM用户的AccessKey Secret
   $ export BUCKET_NAME="<your bucket name>"    # 云存储的Bucket，填写为drift-bottle-in-space
   $ export ENDPOINT="<your endpoint>"    # 云存储的访问域名
   ```

9. 运行

   ```bash
   $ cd drift-bottle-in-space
   $ python3 bot.py
   ```


# E. 总结

## E1. 展望

### 1. 让心在宇宙漂流

此项目结合了轻社交的星际漂流瓶，让大家可以抒发一下想对着太空说的话。也可以惊喜地看到别人写的漂流瓶。

### 2.来个更逼真的LBS+AR游戏

后续希望可以从用户拍的图片获取到地点或经纬度，或者用户发送定位来，从而实现更准确的LBS定位。叠加上AI图像能力，说不定能比PokemonGo更棒噢！

起码**普通伊布是不应该在水面出现的噢 @任天堂**。 

![](https://ai-studio-static-online.cdn.bcebos.com/22967d70f02c475abe8e1e7439ec3c37a8c29fb50aca4fe0b4d5ee9fda029ef1)

看到这个项目，要不要也一起合作来把AI融到游戏里啊 @任天堂 （JUST JOKING.DON`T TAKE IT SERIOUSE)

### 3.来更多脑洞一起创作玩法与剧本吧！

希望更多有兴趣的脑洞，一起想想我们可以怎么玩，让我们玩得更height一点吧！


## E2. 期盼

希望更多小伙伴能贡献一下自己的脑洞，基于此项目，觉得还可以优化的游戏方式或游戏剧本。希望留言或评论。感谢！

希望小伙伴们觉得此项目不错的**点个赞或FORK**。能从头看到这里的很不容易了。非常感谢！！

## E3. Reference/参考内容

- [阿里云官网](https://account.aliyun.com)
- [Wechaty官网](https://wechaty.js.org)
- [python-wechaty](https://github.com/wechaty/python-wechaty)
- [python-wechaty-getting-started](https://github.com/wechaty/python-wechaty-getting-started)
- [教你用AI Studio+wechaty+阿里云白嫖一个智能微信机器人](https://aistudio.baidu.com/aistudio/projectdetail/1836012)
 - [通过LSGAN以及WGAN-GP实现128*128大小的喀纳斯风景图片](http://https://aistudio.baidu.com/aistudio/projectdetail/1936908)
- [Paddle2.0-通过LSGAN让我们看看AI预测的外星人长什么样子](http://https://aistudio.baidu.com/aistudio/projectdetail/2210138)

## E4.致谢

感谢比赛的相关人员

感谢百度爸爸的算力及技术支持

感谢Wechaty与Mixlabs

感谢Reference中列到的所有作者

感谢其中用到的所有开源项目的作者及维护者

感谢Teammate细菌，感谢过程中所有提供鼓励与帮助的百度人员

致敬为拓展人类的宇宙梦而奋斗的所有技术工作者 Respect！!!





