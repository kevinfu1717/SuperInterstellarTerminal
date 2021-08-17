import os
import json
import CVTools
import requests

from typing import Dict, List, Optional


class ImgGenerator():
    """
    图像处理

    用法 ::

        >>> import img_generate
        >>> imgs = img_generate.ImgGenerator()

    """

    def __init__(self):
        self.server_host = os.getenv('IMG_SERVER_HOST')
        self.url = 'http://' + self.server_host + ':9001/imgGenerate'
        self.task_types = ['alien', 'vegetable', 'environment', 'pet']
        self.type_dict = {
            'alien': 0,
            'vegetable': 1,
            'environment': 2,
            'pet': 3
        }
        self.alien_types = {
            '胡巴星人': 1,
            '格鲁特星人': 2
        }
        self.vegetable_types = {
            '光母花': 1,
            '荧光光球菇': 2,
            '数码绿藤': 3,
            '红蓝肉肉': 4,
            '玛娜之花': 5
        }
        self.pet_types = {
            '蓝牛族': 1,
            '蓝天族': 2,
            '不明种族飞船': 3,
            '飘飘族': 4,
            '绿团族': 5,
            '单眼蓝兽族': 6,
            '三黄脚族': 7,
            '单眼彩松鼠族': 8,
            '三眼怪鸡族': 9,
            '幽脸族': 10,
            '紫脸族': 11,
            '长泡族': 12,
            '大型星际飞船': 13,
            '光外族': 14
        }

    def run(self, img_path: str, big_type: str, little_type: Optional[str] = None) -> Dict:
        """
        图像处理
        :param img_path: 图片的路径
        :param big_type: 图像处理的模式，可选`alien`, `vegetable`, `environment`, `pet`
        :return: 图像处理的结果

        用法 ::

            >>> res = imgs.run(
                img_path='test.jpg',
                big_type='alien'
            )
            res = {
                'code': 200,
                'err': 'success',
                'img': array([[[ 37,  43,  38],
                               [ 32,  39,  32],
                               [ 30,  37,  30],
                               ...,
                               [ 55,  37,  20],
                               [ 54,  36,  19],
                               [ 54,  36,  19]]], dtype=uint8),
                'info': {
                    'descriptions': [
                        '格鲁特星人，身体虽为树木，但却不怕火。只要没化成灰，即便粉身 碎骨，也可以复活。',
                        '格鲁特星人作为花神巨像族的一员，格鲁特拥有高度的智慧和树人特有的生理特征——超强的再生能力，只需一部分树枝存 在，浇水施肥便能长成大树；此外还拥有超级力量和防御力，能够通过自我生长长成巨人，并且像橡胶一样自如拉伸自己的身体部位，使树木构成 的身体自由延展、攻击敌人，还能够通过散播孢子控制其他植物、治疗他人。'
                    ],
                    'front': {
                        'LMJson': 'geluteBody.json',
                        ...,
                        'scaleRatio': 1.3
                    },
                    'id': 2,
                    'name': '格鲁特星人',
                    'side': {
                        'LMJson': 'gelute3.json',
                        ...,
                        'scaleRatio': 1.5
                    }
                }
            }

        """
        print('big_type:', big_type)
        if little_type:
            alienhead_index = self.alien_types[little_type] if big_type == 'alien' else -1
            vegetable_index = self.vegetable_types[little_type] if big_type == 'vegetable' else -1
            environment_index = 0 if big_type == 'environment' else -1
            alienpet_index = self.pet_types[little_type] if big_type == 'pet' else -1
        else:
            alienhead_index = 0 if big_type == 'alien' else -1
            vegetable_index = 0 if big_type == 'vegetable' else -1
            environment_index = 0 if big_type == 'environment' else -1
            alienpet_index = 0 if big_type == 'pet' else -1
        query = CVTools.picpath2base64(img_path)
        data = {
            'query': query,
            'alienHeadIndex': alienhead_index,
            'vegetateIndex': vegetable_index,
            'environmentIndex': environment_index,
            'alienPetIndex': alienpet_index
        }
        req = requests.post(url=self.url, data=data)
        data: Dict = json.loads(req.text)
        # print('data', data)
        code: int = int(list(data['result_code'].keys())[0])
        err = list(data['result_code'].values())[0]
        if data['img']:
            img = CVTools.base64CV(data['img'])
        else:
            img = None

        if data['param_dicts']:
            infos: List[Dict] = data['param_dicts']
            info: Dict = infos[self.type_dict[big_type]]
        else:
            info = None
        res = {
            'code': code,
            'err': err,
            'img': img,
            'info': info
        }

        return res


if __name__ == '__main__':
    imgs = ImgGenerator()
    res = imgs.run(
        img_path='testpic/wyf.jpg',
        big_type='alien'
    )
    print('res:', res)
