# -*- coding: utf-8 -*-

import os
import cv2
import oss

import mysql
import random

import randoms
import strings
import asyncio
import logging

from queue import Queue
from userbot import UserBot
from task import Task, task1, task2

from img_generate import ImgGenerator
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from typing import Dict, List, Optional, Union
from wechaty_puppet import FileBox, ScanStatus, file_box

from wechaty import Wechaty, Contact, Friendship
from wechaty.user import Message, Room, tag


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
logging.getLogger('transitions').setLevel(logging.INFO)

SLEEP_TIME = 5
TABLE_USERS = 'users'
TABLE_BOTTLES = 'bottles'
BOTTLES_DIRNAME = 'bottles/'


class MyBot(Wechaty):
    """
    listen wechaty event with inherited functions, which is more friendly for
    oop developer
    """

    def __init__(self):
        super().__init__()
        # 机器人的状态，`work: 工作`，`night: 休息`
        self.state: str = 'work'
        # 是否有用户正在玩漂流瓶接力游戏
        self.on_bottles_relay: bool = False
        # 接力漂流瓶
        self.TABLE_BOTTLES_RELAY = 'bottles_relay_1'
        # 群聊
        self.room: Optional[Room] = None
        # 群聊任务
        self.room_task: Optional[Task] = None
        # 所有用户的userbot
        self.userbots: List[UserBot] = []
        # 所有开发者的contact
        self.developers: List[Contact] = []
        # 预加载任务的队列
        self.preloaded_tasks = Queue(maxsize=8)
        self.preloaded_tasks.put(task1)
        self.preloaded_tasks.put(task2)
        # 创建调度器
        self.scheduler_time = AsyncIOScheduler()
        self.scheduler_task = AsyncIOScheduler()
        self.scheduler_task.add_job(
            func=self.release_task,
            trigger='cron',
            args=('timing', ),
            hour='8-22',
            minute='20'
        )
        # 获取云数据库
        self.db = mysql.MySQL(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_DATABASE')
        )
        # 创建用户表
        self.db.create_users_table(table=TABLE_USERS, is_show=True)
        # 创建漂流瓶表
        self.db.create_bottles_table(table=TABLE_BOTTLES, is_show=True)
        # 创建接力漂流瓶表
        self.db.create_bottles_relay_table(table=self.TABLE_BOTTLES_RELAY, is_show=True)
        # 获取云存储
        self.bucket = oss.OSS(
            access_key_id=os.getenv('ACCESS_KEY_ID'),
            access_key_secret=os.getenv('ACCESS_KEY_SECRET'),
            bucket_name=os.getenv('OSS_BUCKET_NAME'),
            endpoint=os.getenv('OSS_ENDPOINT')
        )
        # 图像处理
        self.imgs = ImgGenerator()

    async def on_message(self, msg: Message):
        """
        listen for message event
        """
        from_contact = msg.talker()
        is_self = msg.is_self()
        text = msg.text()
        type = msg.type()
        room = msg.room()
        # 获取用户的userbot
        userbot = await self.find_user(user_name=from_contact.name)

        # 执行群聊任务
        if room == self.room:
            # 不接收机器人自己的消息
            if not is_self:
                if self.room_task:
                    if type == Message.Type.MESSAGE_TYPE_IMAGE:
                        await self.execute_room_task(task=self.room_task, room=self.room, msg=msg)
            
        # 不处理群消息
        if room is None:
            # 不接收机器人自己的消息
            if not is_self:
                if text == '#加载用户':
                    await self.load_users()

                # 打招呼
                if text == '#hi' or text == '#你好':
                    if not userbot.state == 'night':
                        await self.say_hello(userbot=userbot)
                        
                # 晚安
                if userbot.state == 'night':
                    await self.say_something(conversation=from_contact, content='晚安咯😴')

                # [漂流瓶]-只发送文本信息
                if '不' in text and userbot.state == 'send_bottle_get_img':
                    await self.send_bottle(
                        userbot=userbot,
                        msg=msg,
                        on_img=False
                    )

                # [漂流瓶接力]-查看接力漂流瓶的所有信息
                if self.on_bottles_relay and userbot.state == 'on_bottles_relay':
                    if type == Message.Type.MESSAGE_TYPE_TEXT:
                        await self.say_something(conversation=from_contact, content='好的👌，正在准备发送您的接力信息......')
                        self.db.relay(table=self.TABLE_BOTTLES_RELAY, owner=userbot.name, message=text)
                        await self.say_something(conversation=from_contact, content='接力成功🎉🎉🎉')
                        self.on_bottles_relay = False
                        userbot.free()
                
                # 处理图片信息
                if type == Message.Type.MESSAGE_TYPE_IMAGE:
                    # [漂流瓶]-发送文本和图片信息
                    if userbot.state == 'send_bottle_get_img':
                        await self.send_bottle(
                            userbot=userbot,
                            msg=msg,
                            on_img=True
                        )

                    # 执行任务
                    elif userbot.task:
                        if userbot.state == 'free':
                            await self.execute_task(task=userbot.task, userbot=userbot, msg=msg)

                    # 识别图中的外星物种
                    elif userbot.score >= userbot.grade_rule['黄金']:
                        if userbot.state == 'free':
                            await self.scan_img(userbot=userbot, msg=msg)

                # [漂流瓶]-接收用户编辑的文本信息
                if userbot.state == 'send_bottle_get_msg':
                    if type == Message.Type.MESSAGE_TYPE_TEXT:
                        userbot.send_bottle_get_img()
                        userbot.send_bottle_msg = text
                        await self.say_something(conversation=from_contact, content='配上一张精美的图片🖼️可以更好的表达此刻的心情哦😉，如不需要请回复不用了。')

                # [漂流瓶]-发送太空漂流瓶
                if text == '1' and userbot.score >= userbot.grade_rule['青铜']:
                    if userbot.state == 'free':
                        userbot.send_bottle_get_msg()
                        await self.say_something(conversation=from_contact, content='请编辑一条您要发送的信息📝')

                # [漂流瓶]-接收太空漂流瓶
                if text == '2' and userbot.score >= userbot.grade_rule['白银']:
                    if userbot.state == 'free':
                        await self.get_bottle(userbot=userbot)

                # [漂流瓶接力]-查看接力漂流瓶的所有信息
                if text == '接力':
                    if self.on_bottles_relay:
                        await self.say_something(conversation=from_contact, content='有用户正在玩漂流瓶接力，请稍等一会儿哦😉')
                    else:
                        self.on_bottles_relay = True
                        userbot.on_bottles_relay()
                        messages = self.db.get_bottles_relay(table=self.TABLE_BOTTLES_RELAY, is_show=True)
                        if messages:
                            await self.say_something(conversation=from_contact, content='欢迎参加漂流瓶接力游戏(*^▽^*)，漂流瓶的所有信息如下：')
                            await self.say_something(conversation=from_contact, content='\n\n'.join(messages))
                            await self.say_something(conversation=from_contact, content='接下来该你咯，请编辑一条您要发送的信息📝')
                        else:
                            await self.say_something(conversation=from_contact, content='欢迎参加漂流瓶接力游戏(*^▽^*)，您是漂流瓶接力的第一个人哦😉，请编辑一条您要发送的信息📝')
                
                # [开发者]-添加开发者
                if text == os.getenv('DEVELOPERS'):
                    if from_contact in self.developers:
                        await self.say_something(conversation=from_contact, content='您已经是开发者了，无须重复添加哦😉')
                    else:
                        self.developers.append(from_contact)
                        await self.say_something(conversation=from_contact, content='您已被添加为开发者，机器人的相关信息会及时向您汇报😁')
                    await self.say_something(conversation=from_contact, content='开发者的特殊功能如下：\n• 早安\n• 晚安\n• 发布任务\n• 预存任务\n• 注册用户\n• 所有用户\n• 删除用户\n• 发布群聊任务\n• 取消群聊任务\n• 开启定时任务\n• 关闭定时任务\n• 修改用户积分\n• 释放接力漂流瓶\n• 给所有用户发信息\n• 重新打开一个接力漂流瓶\n• 删除缓存图片')

                # [开发者]-开发者的信息
                if from_contact in self.developers:
                    # [开发者]-发布任务
                    if userbot.state == 'release_task':
                        try:
                            task = await self.parse_task(text=text)
                            userbot.free()
                            await self.release_task(run_type='now', task=task)
                        except Exception as e:
                            userbot.free()
                            await self.report(content=f'发布任务失败😭\n{repr(e)}')

                    # [开发者]-预存任务
                    if userbot.state == 'preload_task':
                        try:
                            task = await self.parse_task(text=text)
                            self.preloaded_tasks.put(task)
                            userbot.free()
                            await self.report(content='成功添加一个预加载任务🎉🎉🎉')
                        except Exception as e:
                            userbot.free()
                            await self.report(content=f'预存任务失败😭\n{repr(e)}')

                    # [开发者]-注册用户
                    if userbot.state == 'on_sign_up':
                        texts = text.split('<br/>')
                        user_name = texts[1]
                        user = await self.Contact.find(query=user_name)
                        userbot.free()
                        await self.accept(conversation=user)
                        
                    # [开发者]-删除用户
                    if userbot.state == 'on_delete_user':
                        try:
                            texts = text.split('<br/>')
                            user_name = texts[1]
                            _userbot = await self.find_user(user_name=user_name)
                            self.userbots.remove(_userbot)
                            _userbot.delete_user()
                            userbot.free()
                            await self.report(content=f'删除用户【{user_name}】成功🎉🎉🎉')
                        except Exception as e:
                            userbot.free()
                            await self.report(content=f'删除用户【{user_name}】失败😭\n{repr(e)}')
                    
                    # [开发者]-发布群聊任务
                    if userbot.state == 'release_room_task':
                        try:
                            task = await self.parse_room_task(text=text)
                            self.room_task = task
                            print('self.room:', self.room)
                            room_name = await self.room.topic()
                            userbot.free()
                            await self.say_something(conversation=self.room, content=f'收到一个求助任务ヾ(≧▽≦*)o\n【{task.name}】\n提示：{task.info}')
                            await self.report(content=f'发布群聊任务成功🎉🎉🎉\n任务类型：{task.big_type}，{task.little_type}\n任务名称：{task.name}\n提示信息：{task.info}\n群聊名称：{room_name}')
                        except Exception as e:
                            userbot.free()
                            await self.report(content=f'发布群聊任务失败😭\n{repr(e)}')
                    
                    # [开发者]-修改用户积分
                    if userbot.state == 'on_change_score':
                        try:
                            texts = text.split('<br/>')
                            user_name = texts[1]
                            new_score = int(texts[3])
                            _userbot = await self.find_user(user_name=user_name)
                            _userbot.change_score(new_score=new_score)
                            userbot.free()
                            await self.report(content=f'用户积分修改成功🎉🎉🎉\n用户【{user_name}】积分为{new_score} ⭐')
                        except Exception as e:
                            userbot.free()
                            await self.report(content=f'修改用户【{user_name}】积分失败😭\n{repr(e)}')
                        
                    # [开发者]-给所有用户发信息
                    if userbot.state == 'say_to_all':
                        if type == Message.Type.MESSAGE_TYPE_TEXT:
                            await self.say_to_all_users(content=text, sleep_time=1)
                            userbot.free()
                            await self.report(content='发送成功🎉🎉🎉')
                        elif type == Message.Type.MESSAGE_TYPE_IMAGE:
                            file_box = await msg.to_file_box()
                            await self.say_to_all_users(content=file_box, sleep_time=1)
                            userbot.free()
                            await self.report(content='发送成功🎉🎉🎉')
                            
                    if text == '早安':
                        self.state = 'work'
                        for _userbot in self.userbots:
                            _userbot.free()
                        await self.report(content='早安鸭😉\n机器人开始工作咯')
                    
                    if text == '晚安':
                        self.state = 'night'
                        for _userbot in self.userbots:
                            _userbot.night()
                        await self.report(content='晚安咯😴\n机器人休息了')
                    
                    if text == '发布任务':
                        userbot.release_task()
                        await self.how_to_write_task(conversation=from_contact)

                    if text == '预存任务':
                        userbot.preload_task()
                        await self.how_to_write_task(conversation=from_contact)

                    if text == '注册用户':
                        userbot.on_sign_up()
                        await self.say_something(conversation=from_contact, content=f'请按照如下示例指明用户')
                        await self.say_something(conversation=from_contact, content='【用户昵称】\n细菌')
                    
                    if text == '所有用户':
                        user_names = '\n• '.join([_userbot.name for _userbot in self.userbots])
                        await self.say_something(conversation=from_contact, content=f'所有用户如下\n• {user_names}')                    
                    
                    if text == '删除用户':
                        userbot.on_delete_user()
                        await self.say_something(conversation=from_contact, content=f'请按照如下示例指明用户')
                        await self.say_something(conversation=from_contact, content='【用户昵称】\n细菌')
                    
                    if text == '发布群聊任务':
                        userbot.release_room_task()
                        await self.how_to_write_room_task(conversation=from_contact)
                    
                    if text == '取消群聊任务':
                        self.room = None
                        self.room_task = None
                        await self.report(content='取消群聊任务成功🎉🎉🎉')
                    
                    if text == '开启定时任务':
                        try:
                            self.scheduler_task.start()
                            await self.report(content='开启定时任务成功🎉🎉🎉')
                        except Exception as e:
                            await self.report(content=f'开启定时任务失败😭\n{repr(e)}')

                    if text == '关闭定时任务':
                        try:
                            self.scheduler_task.shutdown(wait=False)
                            await self.report(content='关闭定时任务成功🎉🎉🎉')
                        except Exception as e:
                            await self.report(content=f'关闭定时任务失败😭\n{repr(e)}')
                    
                    if text == '修改用户积分':
                        userbot.on_change_score()
                        await self.say_something(conversation=from_contact, content=f'请按照如下示例指明用户以及新的积分\n注：等级规则如下\n• 青铜：0<=score<{UserBot.grade_rule["青铜"]}\n• 白银：{UserBot.grade_rule["青铜"]}<=score<{UserBot.grade_rule["白银"]}\n• 黄金：{UserBot.grade_rule["白银"]}<=score<{UserBot.grade_rule["黄金"]}\n• 钻石：{UserBot.grade_rule["黄金"]}<=score<{UserBot.grade_rule["钻石"]}')
                        await self.say_something(conversation=from_contact, content='【用户昵称】\n细菌\n【新积分】\n0')
                    
                    if text == '释放接力漂流瓶':
                        self.on_bottles_relay = False
                        await self.report(content=f'释放接力漂流瓶成功🎉🎉🎉\n当前数据表为{self.TABLE_BOTTLES_RELAY}')
                    
                    if text == '给所有用户发信息':
                        userbot.say_to_all()
                        await self.say_something(conversation=from_contact, content='请编辑一条您要发送的信息📝\n文字或图片都可以')
                    
                    if text == '重新打开一个接力漂流瓶':
                        bottles_relay_id = int(self.TABLE_BOTTLES_RELAY.split('_')[-1])
                        self.TABLE_BOTTLES_RELAY = 'bottles_relay_' + str(bottles_relay_id + 1)
                        self.db.create_bottles_relay_table(table=self.TABLE_BOTTLES_RELAY, is_show=True)
                        await self.report(content=f'重新打开一个接力漂流瓶成功🎉🎉🎉\n当前数据表为{self.TABLE_BOTTLES_RELAY}')
                    
                    if text == '删除缓存图片':
                        for _userbot in self.userbots:
                            filename = _userbot.filename
                            if os.path.exists(path=filename):
                                os.remove(path=filename)

                        await self.report(content='删除缓存图片成功🎉🎉🎉')

    async def say_hello(self, userbot: UserBot):
        """
        机器人的自我介绍
        """
        userbot.say_hello()
        conversation = userbot.contact
        await self.say_something(conversation=conversation, content='开发不易，开源不易，你们的点赞和支持就是我们最大的动力<img class="qqemoji qqemoji54" text="[可怜]_web" src="/zh_CN/htmledition><img class="qqemoji qqemoji63" text="[玫瑰]_web" src="/zh_CN/htmledition>\nGitHub链接：\nhttps://github.com/kevinfu1717/SuperInterstellarTerminal\nAI Studio链接：\nhttps://aistudio.baidu.com/aistudio/projectdetail/2230251\nbilibili链接：\nhttps://www.bilibili.com/video/BV1hL411E79M')
        file_box_intro = FileBox.from_file(path='static/test.mp4')
        await self.say_something(conversation=conversation, content=file_box_intro)
        userbot.free()
        if userbot.grade == '青铜':
            await self.say_something(conversation=conversation, content=f'当前等级：青铜\n请查收您的等级徽章\n\n注：距离晋升到下一个等级还差{userbot.grade_rule[userbot.grade] - userbot.score} ⭐', sleep_time=40)
            file_box_medal = FileBox.from_file(path='static/medal/bronze.jpg')
            await self.say_something(conversation=conversation, content=file_box_medal)
            await asyncio.sleep(SLEEP_TIME)
            await self.release_task(
                run_type='now',
                task=userbot.hello_task,
                start_msg='叮咚！有一个新用户专享任务等您去完成，完成任务即可解锁更多功能哦',
                timeout_msg='任务已超时，很遗憾你没有成功解锁更多功能😭，下次可要加油哦(ง •_•)ง'
            )
    
    async def grade_up(self, userbot: UserBot, score: int, grade: str):
        """
        等级晋升时执行此函数
        :param userbot: 用户的userbot
        :param score: 用户积分
        :param grade: 用户等级

        """
        conversation = userbot.contact
        if grade == '钻石':
            await self.say_something(conversation=conversation, content=f'恭喜您晋升到{grade}  🎉🎉🎉\n请查收您的等级徽章\n\n注：您已达到最高等级<img class="qqemoji qqemoji13" text="[呲牙]_web" src="/zh_CN/htmledition><img class="qqemoji qqemoji13" text="[呲牙]_web" src="/zh_CN/htmledition>')
        else:
            await self.say_something(conversation=conversation, content=f'恭喜您晋升到{grade}  🎉🎉🎉\n请查收您的等级徽章\n\n注：距离晋升到下一个等级还差{userbot.grade_rule[grade] - score} ⭐')
        await self.show_grade(conversation=conversation, grade=grade)
        
        if grade == '白银':
            await self.say_something(conversation=conversation, content=f'【解锁一项新技能】\n  • 向太空发送漂流信息\n\n【已解锁技能】\n  • 向太空发送漂流信息\n\n【未解锁技能】\n  • 接收太空中的漂流信息\n  • 随时识别图片中的外星物种\n\n回复{strings.symbolize(1)}开启你的太空漂流之旅吧😉\n\n注：完成任务可以增加积分，解锁更多功能')
        elif grade == '黄金':
            await self.say_something(conversation=conversation, content=f'【解锁一项新技能】\n  • 接收太空中的漂流信息\n\n【已解锁技能】\n  • 向太空发送漂流信息\n  • 接收太空中的漂流信息\n\n【未解锁技能】\n  • 随时识别图片中的外星物种\n\n回复{strings.symbolize(2)}接收神秘的太空漂流信息吧😉\n\n注：完成任务可以增加积分，解锁更多功能')
        elif grade == '钻石':
            await self.say_something(conversation=conversation, content=f'【解锁一项新技能】\n  • 随时识别图片中的外星物种\n\n【已解锁技能】\n  • 向太空发送漂流信息\n  • 接收太空中的漂流信息\n  • 随时识别图片中的外星物种\n\n【已解锁全部技能🎉🎉🎉】\n\n发送一张图片开启你的星际穿越之旅吧😉')

    async def send_bottle(self, userbot: UserBot, msg: Message, on_img: bool):
        """
        发送太空漂流瓶
        :param userbot: 用户的userbot
        :param msg: Message
        :param on_img: 是否发送图片

        用法 ::

            >>> # 只发送文本信息
            >>> await self.send_bottle(userbot=userbot, msg=msg, on_img=False)
            >>> # 发送文本和图片信息
            >>> await self.send_bottle(userbot=userbot, msg=msg, on_img=True)

        """
        userbot.send_bottle()
        conversation = userbot.contact
        await self.say_something(conversation=conversation, content='好的👌，正在准备发送太空漂流信息🛸......')
        filename = self.db.insert(
            table=TABLE_BOTTLES,
            owner=conversation.name,
            message=userbot.send_bottle_msg,
            on_img=on_img
        )
        if on_img:
            file_box = await msg.to_file_box()
            await file_box.to_file(file_path=filename, overwrite=True)
            self.bucket.upload_img(dirname=BOTTLES_DIRNAME, filename=filename)
            os.remove(path=filename)

        await self.say_something(conversation=conversation, content='发送成功🎉🎉🎉')
        userbot.free()
        await self.report(content='有一个用户成功发送了太空漂流信息')

    async def get_bottle(self, userbot: UserBot):
        """
        接收太空漂流瓶
        """
        userbot.get_bottle()
        conversation = userbot.contact
        await self.say_something(conversation=conversation, content='正在尝试接收📡太空漂流信息🛸，请稍等.......')
        # 50%的概率接收不到太空漂流瓶
        if randoms.probability(ratio=5):
            await self.say_something(conversation=conversation, content='十分抱歉😭，当前位置暂未收到太空漂流信息🛸，可以换个地方再尝试哦😉')
            userbot.free()
            await self.report(content='有一个用户接收太空漂流信息失败😭')
        else:
            bottle_msg, bottle_img = self.db.get_bottle(table=TABLE_BOTTLES, is_show=True)
            await self.say_something(conversation=conversation, content='接收到一个太空漂流信息🛸')
            await self.say_something(conversation=conversation, content=f'类型：\n文本消息 {"✅" if bottle_msg else "❎"}\n图片消息 {"✅" if bottle_img else "❎"}')
            if bottle_msg:
                await self.say_something(conversation=conversation, content=bottle_msg)
                userbot.free()
            if bottle_img:
                if 'http' in bottle_img:
                    file_box = FileBox.from_url(url=bottle_img)
                    await self.say_something(conversation=conversation, content=file_box, sleep_time=1)
                else:
                    self.bucket.download_img(dirname=BOTTLES_DIRNAME, filename=bottle_img)
                    file_box = FileBox.from_file(path=bottle_img)
                    await self.say_something(conversation=conversation, content=file_box, sleep_time=1)
                    os.remove(path=bottle_img)

            userbot.free()
            await self.report(content='有一个用户接收太空漂流信息成功😊')

    async def scan_img(self, userbot: UserBot, msg: Message):
        """
        识别用户发来的图片中是否有外星物种
        """
        userbot.scan_img()
        conversation = userbot.contact
        await self.say_something(conversation=conversation, content='正在分析扫描中......')
        file_box = await msg.to_file_box()
        filename = userbot.filename
        await file_box.to_file(file_path=filename, overwrite=True)
        big_type = random.choice(self.imgs.task_types)
        res = self.imgs.run(img_path=filename, big_type=big_type)
        code = res['code']
        err = res['err']
        img = res['img']
        info = res['info']
        print('res:', res)
        if code == 200 and info:
            cv2.imwrite(filename, img)
            file_box = FileBox.from_file(path=filename)
            await self.say_something(conversation=conversation, content=f'你当前环境中发现：{info["name"]}')
            await self.say_something(conversation=conversation, content=file_box)
            description = random.choice(info['descriptions'])
            await self.say_something(conversation=conversation, content=description)

        else:
            await self.say_something(conversation=conversation, content='扫描完成，暂未识别到外星物种😳')
            print('图片处理失败或者没识别到外星物种:', err)

        userbot.free()

    async def execute_task(self, task: Task, userbot: UserBot, msg: Message):
        """
        执行任务
        """
        userbot.exec_task()
        conversation = userbot.contact
        await self.say_something(conversation=conversation, content='正在识别并与任务数据进行比对......')
        file_box = await msg.to_file_box()
        filename = userbot.filename
        await file_box.to_file(file_path=filename, overwrite=True)
        res = self.imgs.run(
            img_path=filename,
            big_type=task.big_type,
            little_type=task.little_type
        )
        print('收到回传数据')
        code = res['code']
        err = res['err']
        img = res['img']
        info = res['info']
        print('res:', res)

        if code == 200 and info:
            cv2.imwrite(filename, img)
            file_box = FileBox.from_file(path=filename)
            # 如果任务没有被其他人完成且没有超时
            if userbot.task:
                # 取消任务
                if task.run_type == 'one':
                    await self.cancel_task(task=userbot.task, content='')
                elif task.run_type == 'all':
                    await self.cancel_task(task=userbot.task, content='任务已被其他人完成了，下次要加油哦(ง •_•)ง', without=conversation)
                
                res = self.db.award(
                    table=TABLE_USERS,
                    user_name=conversation.name,
                    score=task.score
                )
                is_grade_up = res['is_grade_up']
                score = res['score']
                grade = res['grade']
                await self.say_something(conversation=conversation, content=f'任务成功完成，相关信息已同步到银河星际移民局，当前积分提升{task.score} ⭐，已达到{score} ⭐  🎉🎉🎉')
                await self.say_something(conversation=conversation, content=file_box)
                description = random.choice(info['descriptions'])
                await conversation.say(f'{info["name"]}\n\n{description}')

                # 如果用户等级提升
                if is_grade_up:
                    await self.grade_up(userbot=userbot, score=score, grade=grade)

        else:
            userbot.free()
            await self.say_something(conversation=conversation, content='当前环境中未找到😭，可以换个地方再次尝试哦😉')
            print('图片处理失败或者没识别到外星物种:', err)

    async def execute_room_task(self, task: Task, room: Room, msg: Message):
        """
        执行任务
        """
        conversation = room
        await self.say_something(conversation=conversation, content='正在识别并与任务数据进行比对......')
        file_box = await msg.to_file_box()
        filename = str(random.randint(10000, 99999)) + '.jpg'
        await file_box.to_file(file_path=filename, overwrite=True)
        res = self.imgs.run(
            img_path=filename,
            big_type=task.big_type,
            little_type=task.little_type
        )
        print('收到回传数据')
        code = res['code']
        err = res['err']
        img = res['img']
        info = res['info']
        print('res:', res)

        if code == 200 and info:
            cv2.imwrite(filename, img)
            file_box = FileBox.from_file(path=filename)
            await self.say_something(conversation=conversation, content=f'任务成功完成🎉🎉🎉，给你一个小星星⭐')
            await self.say_something(conversation=conversation, content=file_box)
            description = random.choice(info['descriptions'])
            await conversation.say(f'{info["name"]}\n\n{description}')

        else:
            await self.say_something(conversation=conversation, content='当前环境中未找到😭，可以换个地方再次尝试哦😉')
            print('图片处理失败或者没识别到外星物种:', err)
    
    async def cancel_task(self, task: Task, content: str, without: Optional[Contact] = None):
        """
        取消任务
        :param run_type: 任务运行类型，`timing: 定时任务`，`now: 立刻任务`
        :param content: 给用户发的信息
        :param without: 成功完成任务的用户

        """
        if task.run_type == 'one':
            userbot: UserBot = task.owner
            if userbot.task:
                userbot.task = None
                userbot.free()
                try:
                    self.scheduler_time.remove_job(job_id=task.id)
                except Exception as e:
                    print(repr(e))
                if content:
                    await self.say_something(conversation=userbot.contact, content=content, sleep_time=0)
        
        elif task.run_type == 'all':
            for userbot in self.userbots:
                if userbot.task and userbot.task.id == task.id:
                    userbot.task = None
                    userbot.free()
                    try:
                        self.scheduler_time.remove_job(job_id=task.id)
                    except Exception as e:
                        print(repr(e))
                    if not userbot.contact == without:
                        await self.say_something(conversation=userbot.contact, content=content, sleep_time=0)

    async def release_task(self, run_type: str, task: Optional[Task] = None, start_msg: str = '', timeout_msg: str = ''):
        """
        发布一个任务
        :param run_type: 任务运行类型，`timing: 定时任务`，`now: 立刻任务`
        :param task: 要发布的任务
        :param start_msg: 发布任务时发送的信息
        :param timeout_msg: 任务超时给用户发的的信息

        """
        # 如果是定时任务就从预加载任务里面加载一个
        if run_type == 'timing':
            task = self.preloaded_tasks.get()
            
        if not start_msg:
            start_msg = '收到一个求助任务ヾ(≧▽≦*)o'
        
        if not timeout_msg:
            timeout_msg = '任务已超时，请等待下一次任务'

        # 任务规定的时间结束以后执行`self.cancel_task`函数
        self.scheduler_time.add_job(
            func=self.cancel_task,
            trigger='interval',
            args=(task, timeout_msg),
            minutes=task.time,
            id=task.id
        )
        try:
            self.scheduler_time.start()
        except Exception as e:
            print(repr(e))

        if task.run_type == 'one':
            userbot: UserBot = task.owner
            task_owner = userbot.name
            userbot.task = task
            await self.say_something(conversation=userbot.contact, content=f'{start_msg}\n【{task.name}】\n• 奖励：{task.score} ⭐\n• 时间：{task.time}分钟\n• 提示：{task.info}', sleep_time=0)
        
        elif task.run_type == 'all':
            task_owner = 'None'
            for userbot in self.userbots:
                if not userbot.task:
                    userbot.task = task
                    await self.say_something(conversation=userbot.contact, content=f'{start_msg}\n【{task.name}】\n• 奖励：{task.score} ⭐\n• 时间：{task.time}分钟\n• 提示：{task.info}', sleep_time=0)

        await self.report(content=f'成功发布了一项任务🎉🎉🎉\n任务类型：{task.big_type}，{task.little_type}\n任务名称：{task.name}\n提示信息：{task.info}\n执行时间：{task.time}分钟\n任务奖励：{task.score} ⭐\n任务运行类型：{task.run_type}\n指定用户：{task_owner}')
    
    async def parse_task(self, text: str) -> Task:
        """
        从文本中解析出任务
        """
        texts = text.split('<br/>')
        task_big_type = texts[1]
        task_little_type = None if texts[3] == 'all' else texts[3]
        task_name = texts[5]
        task_info = texts[7]
        task_time = int(texts[9])
        task_score = int(texts[11])
        task_run_type = texts[13]
        task_owner = texts[15]
        if not task_owner == 'None':
            task_owner = await self.find_user(user_name=task_owner)

        task = Task(
            name=task_name,
            big_type=task_big_type,
            little_type=task_little_type,
            info=task_info,
            time=task_time,
            score=task_score,
            run_type=task_run_type,
            owner=task_owner
        )

        return task

    async def parse_room_task(self, text: str) -> Task:
        """
        从文本中解析出群聊任务
        """
        texts = text.split('<br/>')
        task_big_type = texts[1]
        task_little_type = None if texts[3] == 'all' else texts[3]
        task_name = texts[5]
        task_info = texts[7]
        room_name = texts[9]
        self.room = await self.Room.find(query=room_name)

        task = Task(
            name=task_name,
            big_type=task_big_type,
            little_type=task_little_type,
            info=task_info,
            time=None,
            score=None,
            run_type=None,
            owner=None
        )

        return task
    
    async def how_to_write_task(self, conversation: Contact):
        """
        教开发者如何编写任务
        """
        msg_alien_type = '\n  • '.join(list(self.imgs.alien_types.keys()))
        msg_vegetable_type = '\n  • '.join(list(self.imgs.vegetable_types.keys()))
        msg_pet_type = '\n  • '.join(list(self.imgs.pet_types.keys()))
        await self.say_something(conversation=conversation, content=f'请按照如下示例指明任务\n注：任务类型（大类）可选\n• alien\n• pet\n• vegetable\n• environment\n注：任务类型（小类）可选\n• alien\n  • all\n  • {msg_alien_type}\n• pet\n  • all\n  • {msg_pet_type}\n• vegetable\n  • all\n  • {msg_vegetable_type}\n• environment\n  • all\n  • 无\n注：任务时间为整数，单位是分钟\n注：任务奖励为整数\n注：任务运行类型可选\n• all\n• one\n注：指定用户可选\n• None\n• 某一个用户的昵称')
        await self.say_something(conversation=conversation, content='【任务类型（大类）】\nalien\n【任务类型（小类）】\n格鲁特星人\n【任务名称】\n寻找隐藏在地球人中的格鲁特星人\n【提示信息】\n拍摄可疑人物的正脸给我，我来扫描确认\n【任务时间】\n3\n【任务奖励】\n20\n【任务运行类型】\nall\n【指定用户】\nNone')

    async def how_to_write_room_task(self, conversation: Contact):
        """
        教开发者如何编写群聊任务
        """
        msg_alien_type = '\n  • '.join(list(self.imgs.alien_types.keys()))
        msg_vegetable_type = '\n  • '.join(list(self.imgs.vegetable_types.keys()))
        msg_pet_type = '\n  • '.join(list(self.imgs.pet_types.keys()))
        await self.say_something(conversation=conversation, content=f'请按照如下示例指明任务\n注：任务类型（大类）可选\n• alien\n• pet\n• vegetable\n• environment\n注：任务类型（小类）可选\n• alien\n  • all\n  • {msg_alien_type}\n• pet\n  • all\n  • {msg_pet_type}\n• vegetable\n  • all\n  • {msg_vegetable_type}\n• environment\n  • all\n  • 无')
        await self.say_something(conversation=conversation, content='【任务类型（大类）】\nalien\n【任务类型（小类）】\n格鲁特星人\n【任务名称】\n寻找隐藏在地球人中的格鲁特星人\n【提示信息】\n拍摄可疑人物的正脸给我，我来扫描确认\n【指定群聊】\n星际终端-微信漂流瓶版PokemonGo')
    
    async def say_something(self, conversation: Contact, content: Union[str, FileBox], sleep_time: int = SLEEP_TIME):
        """
        给用户发信息
        """
        await conversation.ready()
        await asyncio.sleep(sleep_time)
        await conversation.say(content)

    async def say_to_all_users(self, content: Union[str, FileBox], without: Optional[Contact] = None, sleep_time: int = SLEEP_TIME):
        """
        给所有用户发信息
        :param content: 信息内容
        :param without: 不给其中一个用户发信息

        """
        for userbot in self.userbots:
            if userbot.contact == without:
                continue
            else:
                conversation = userbot.contact
                await self.say_something(conversation=conversation, content=content, sleep_time=sleep_time)

    async def show_grade(self, conversation: Contact, grade: str):
        """
        展示用户的等级徽章
        """
        grade_filename = {
            '青铜': 'bronze.jpg',
            '白银': 'silver.jpg',
            '黄金': 'gold.jpg',
            '钻石': 'diamond.jpg'
        }
        filename = grade_filename[grade]
        filepath = 'static/medal/' + filename
        file_box = FileBox.from_file(path=filepath)
        await self.say_something(conversation=conversation, content=file_box)

    async def find_user(self, user_name: str) -> UserBot:
        """
        根据昵称查找用户userbot
        """
        for userbot in self.userbots:
            if userbot.name == user_name:
                return userbot
    
    async def accept(self, conversation: Contact):
        userbot = UserBot(contact=conversation)
        userbot.sign_up()
        for _userbot in self.userbots:
            if _userbot.contact == userbot.contact:
                self.userbots.remove(_userbot)
        self.userbots.append(userbot)
        await self.report(content=f'新加入一个用户【{userbot.name}】')
        await self.say_hello(userbot=userbot)
    
    async def load_users(self):
        all_contacts: List[Contact] = await self.Contact.find_all()
        print('len(all_contacts):', len(all_contacts))
        users = [contact for contact in all_contacts if contact.is_friend()]
        for user in users:
            if self.db.is_user(table=TABLE_USERS, user_name=user.name):
                userbot = UserBot(contact=user)
                self.userbots.append(userbot)

        self.db.select_all(table=TABLE_USERS, msg='所有用户如下：', is_show=True)
    
    async def report(self, content: str):
        """
        向开发者报告一些信息
        """
        if self.developers:
            num_users = len(self.userbots)
            num_bottles = len(self.db.select_all(table=TABLE_BOTTLES))
            num_tasks = self.preloaded_tasks.qsize()
            for conversation in self.developers:
                await self.say_something(conversation=conversation, content=f'尊敬的开发者，您有一条信息📝\n-------------------------------------------------\n{content}\n-------------------------------------------------\n目前用户的数量：{strings.symbolize(num_users)}\n太空漂流瓶的数量：{strings.symbolize(num_bottles)}\n预加载任务的数量：{strings.symbolize(num_tasks)}')

    async def on_friendship(self, friendship: Friendship):
        if self.state == 'work':
            if friendship.hello() == '星际终端':
                await friendship.accept()
                await self.accept(conversation=friendship.contact())

    async def on_login(self, contact: Contact):
        print(f'user: {contact} has login')

    async def on_scan(self, status: ScanStatus, qr_code: Optional[str] = None, data: Optional[str] = None):
        contact = self.Contact.load(self.contact_id)
        print(f'user <{contact}> scan status: {status.name} , '
              f'qr_code: {qr_code}')


bot: Optional[MyBot] = None


async def main():
    global bot
    bot = MyBot()
    await bot.start()


asyncio.run(main())
