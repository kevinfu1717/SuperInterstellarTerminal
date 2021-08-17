import os
import mysql

from task import Task
from wechaty import Contact
from transitions import Machine

from typing import Optional


TABLE_USERS = 'users'


class UserBot():

    grade_rule = {
        '青铜': 20,    # 0<=score<20
        '白银': 50,    # 20<=score<50
        '黄金': 100,    # 50<=score<100
        '钻石': 1600    # 100<=score<1600
    }

    states = ['free', 'night', 'say_hello', 'send_bottle_get_msg', 'send_bottle_get_img', 'send_bottle', 'get_bottle', 'on_bottles_relay', 'scan_img', 'exec_task', 'release_task', 'release_room_task', 'preload_task', 'on_sign_up', 'on_delete_user', 'on_change_score', 'say_to_all']

    transitions = [
        {
            'trigger': 'free',
            'source': '*',
            'dest': 'free'
        },
        {
            'trigger': 'night',
            'source': '*',
            'dest': 'night'
        },
        {
            'trigger': 'say_hello',
            'source': '*',
            'dest': 'say_hello'
        },
        {
            'trigger': 'send_bottle_get_msg',
            'source': '*',
            'dest': 'send_bottle_get_msg'
        },
        {
            'trigger': 'send_bottle_get_img',
            'source': 'send_bottle_get_msg',
            'dest': 'send_bottle_get_img'
        },
        {
            'trigger': 'send_bottle',
            'source': 'send_bottle_get_img',
            'dest': 'send_bottle'
        },
        {
            'trigger': 'get_bottle',
            'source': '*',
            'dest': 'get_bottle'
        },
        {
            'trigger': 'on_bottles_relay',
            'source': '*',
            'dest': 'on_bottles_relay'
        },
        {
            'trigger': 'scan_img',
            'source': '*',
            'dest': 'scan_img'
        },
        {
            'trigger': 'exec_task',
            'source': '*',
            'dest': 'exec_task'
        },
        {
            'trigger': 'release_task',
            'source': '*',
            'dest': 'release_task'
        },
        {
            'trigger': 'release_room_task',
            'source': '*',
            'dest': 'release_room_task'
        },
        {
            'trigger': 'preload_task',
            'source': '*',
            'dest': 'preload_task'
        },
        {
            'trigger': 'on_sign_up',
            'source': '*',
            'dest': 'on_sign_up'
        },
        {
            'trigger': 'on_delete_user',
            'source': '*',
            'dest': 'on_delete_user'
        },
        {
            'trigger': 'on_change_score',
            'source': '*',
            'dest': 'on_change_score'
        },
        {
            'trigger': 'say_to_all',
            'source': '*',
            'dest': 'say_to_all'
        }
    ]

    def __init__(self, contact: Contact):
        self.contact = contact
        self.name = contact.name
        self.filename = contact.contact_id[:9] + '.jpg'
        self.send_bottle_msg = ''
        # 状态机
        self.machine = Machine(
            model=self,
            states=UserBot.states,
            initial='free',
            transitions=UserBot.transitions
        )
        # 获取云数据库
        self.db = mysql.MySQL(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_DATABASE')
        )
        self.hello_task = Task(
            name='寻找隐藏在地球人中的格鲁特星人',
            big_type='alien',
            little_type='格鲁特星人',
            info='拍摄可疑人物的正脸给我，我来扫描确认',
            time=5,
            score=UserBot.grade_rule['青铜'],
            run_type='one',
            owner=self
        )
        self.task: Optional[Task] = None

    @property
    def grade(self) -> str:
        res = self.db.user_info(table=TABLE_USERS, user_name=self.name)
        return res['grade']

    @property
    def score(self) -> int:
        res = self.db.user_info(table=TABLE_USERS, user_name=self.name)
        return res['score']

    def sign_up(self):
        """
        注册用户
        """
        self.db.sign_up(table=TABLE_USERS, user_name=self.name, is_show=True)

    def delete_user(self):
        """
        删除数据库中的用户
        """
        if self.db.is_user(table=TABLE_USERS, user_name=self.name):
            res = self.db.user_info(table=TABLE_USERS, user_name=self.name)
            self.db.delete(table=TABLE_USERS, condition=f'id={res["id"]}')
    
    def change_score(self, new_score: int):
        """
        改变用户的积分和等级
        """
        for _grade, _score in UserBot.grade_rule.items():
            if new_score < _score:
                new_grade = _grade
                break
        res = self.db.user_info(table=TABLE_USERS, user_name=self.name)
        self.db.update(
            table=TABLE_USERS,
            content=f'score={new_score}, grade="{new_grade}"',
            condition=f'id={res["id"]}',
            is_show=True
        )
