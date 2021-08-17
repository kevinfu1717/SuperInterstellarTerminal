import random


class Task():
    # 任务类型
    big_types = ['alien', 'pet', 'vegetable', 'environment']

    def __init__(
        self,
        name: str,
        big_type: str,
        little_type: str,
        info: str,
        time: int,
        score: int,
        run_type: str,
        owner = None
    ):
        """
        :param name: 任务名字
        :param big_type: 任务类型（大类），必须是`Task.big_types`里面的一个
        :param little_type: 任务类型（小类），具体参考`img_generate.py`文件
        :param info: 提示信息
        :param time: 任务规定时间
        :param score: 任务完成奖励分数
        :param run_type: 任务运行类型，`one: 指定用户的任务`，`all: 所有用户的任务`
        :param owner: 任务的所属者，`UserBot: 指定用户`，`None: 所有用户`

        """
        self.name = name
        self.big_type = big_type
        self.little_type = little_type
        self.info = info
        self.time = time
        self.score = score
        self.run_type = run_type
        self.owner = owner
        self.id = str(random.randint(10000, 99999))


task1 = Task(
    name='寻找阿布扎丢失的外星宠物-蓝牛族',
    big_type='pet',
    little_type='蓝牛族',
    info='该宠物一般喜欢在街上闲逛，可以拍摄你周围的街道图片，我来扫描确认',
    time=5,
    score=33,
    run_type='all'
)
task2 = Task(
    name='寻找天空中的大型星际飞船',
    big_type='pet',
    little_type='大型星际飞船',
    info='拍摄一张天空图片，我来扫描确认',
    time=5,
    score=46,
    run_type='all'
)
