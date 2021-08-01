import paddlehub as hub
import numpy as np
## https://gitee.com/PaddlePaddle/PaddleHub/tree/release/v2.1/modules/image/keypoint_detection/face_landmark_localization
class landmarker():
    def __init__(self,debug=False):
        self.face_landmark = hub.Module(name="face_landmark_localization")
        self.debug=debug
    def run(self, img):
        landmarks = []
        # print('begin baidu landmark')
        results = self.face_landmark.keypoint_detection(images=[img],
                                                        paths=None,
                                                        batch_size=1,
                                                        use_gpu=False,
                                                        output_dir='face_landmark_output',
                                                        visualization=self.debug)
        # print('emoi baidu landmark',landmarks)
        for result in results:
            landmarks = result['data']
            break  # one pic one result
        # print('emoi baidu landmark', landmarks[0], len(landmarks[0]))
        return landmarks
    def heightestFace(self, img):
        if self.debug:
            print(img.shape)
        landmarks=self.run(img)
        tempHeight=0
        tempIndex=0
        for index,la in enumerate(landmarks):
           la=np.array(la)
           height=np.max(la[:,1])-np.min(la[:,1])
           if height>tempHeight:
               tempHeight=height
               tempIndex=index
        #print(landmarks,tempIndex)
        #print('tempIndex:',landmarks[tempIndex])
        if len(landmarks)>0:
            
            return np.array(landmarks[tempIndex]),tempHeight
        else:
            return [],tempHeight