import json
import numpy as np

def readJson(path):
    with open(path, "r") as f:
        json_str = f.read()
    #print(json_str)
    your_dict = json.loads(json_str)
    shapes = your_dict["shapes"]
    length = len(shapes)
    shapes=your_dict['shapes']
    #print(your_dict['shapes'])
    landmarks=[]
    for ss in shapes:

        landmarks.append(ss['points'][0])

    landmarks=np.array(landmarks,'int32')

    return landmarks

if __name__=='__main__':
    landmarks=readJson("pic/hubaHead.json")
    print(landmarks,landmarks.shape)