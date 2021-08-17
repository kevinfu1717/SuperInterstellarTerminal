import os
import json
import strings
import requests
import prettytable as pt

from userbot import UserBot
from typing import Dict, List, Optional, Tuple


class MySQL():
    """
    对数据库进行操作

    用法 ::

        >>> import mysql
        >>> db = mysql.MySQL(
                host='<your host>',
                user='<your user>',
                password='<your password>',
                database='<your database>'
            )

    """

    def __init__(self, host: str, user: str, password: str, database: str):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.wrong_msg = '数据库连接失败😭，请检查连接'
        self.grade_rule = UserBot.grade_rule

        # 检查数据库连接是否成功
        server_host = os.getenv('DB_SERVER_HOST')
        url = 'http://' + server_host + ':8000/database/check'
        data = {
            'host': self.host,
            'user': self.user,
            'password': self.password,
            'database': self.database
        }
        req = requests.post(url=url, data=data)
        data = json.loads(req.content.decode())

        # 数据库连接成功
        if data['code'] == 200:
            self.is_connect = True
            print(data['info'])
        else:
            self.is_connect = False
            print(data['info'])
            print(data['err'])

    def _run(self, table: str, sql: str, msg: str = '') -> List[Dict]:
        server_host = os.getenv('DB_SERVER_HOST')
        url = 'http://' + server_host + ':8000/database/run'
        # print('sql:', sql)    # 方便调试
        data = {
            'host': self.host,
            'user': self.user,
            'password': self.password,
            'database': self.database,
            'sql': sql
        }
        req = requests.post(url=url, data=data)
        data = json.loads(req.content.decode())

        # 执行成功
        if data['code'] == 200:
            results = data['results']
            if results:
                # 打印结果
                if msg:
                    tb = pt.PrettyTable()
                    tb.field_names = [field for field, value in results[0].items()]
                    _results = results[:]
                    for i, result in enumerate(results):
                        _results[i] = [value for field, value in result.items()]

                    tb.add_rows(_results)
                    print(msg)
                    print(tb.get_string(title=table))

        # 执行失败
        else:
            print('执行失败')
            print(data['err'])

        return results

    def table_info(self, table: str, msg: str = '', is_show: bool = False):
        """
        查询表的结构
        :param table: 数据表的名称
        :param msg: 运行时打印的提示信息
        :param is_show: 是否打印表格

        用法 ::

            >>> db.table_info(table='bottles')

        """
        if not self.is_connect:
            print(self.wrong_msg)

        else:
            # MySQL语句
            sql = f'''
                DESC {table};
            '''
            if is_show and not msg:
                msg = '数据表的结构如下：'

            self._run(table=table, sql=sql, msg=msg)

    def create_users_table(self, table: str, msg: str = '', is_show: bool = False) -> None:
        """
        创建用户表
        :param table: 数据表的名称
        :param msg: 运行时打印的提示信息
        :param is_show: 是否打印表格

        用法 ::

            >>> db.create_users_table(table='users')

        """
        if not self.is_connect:
            print(self.wrong_msg)

        else:
            # MySQL语句
            sql = f'''
                CREATE TABLE IF NOT EXISTS {table}(
                    id INT UNSIGNED AUTO_INCREMENT,
                    name TINYTEXT NOT NULL COMMENT '用户的昵称',
                    score TINYINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '用户的积分',
                    grade TINYTEXT NOT NULL COMMENT '用户的等级',
                    sign_up_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '用户的注册时间',
                    PRIMARY KEY (id)
                )ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户信息';

            '''
            if is_show and not msg:
                msg = '数据表创建成功😊，表的结构如下：'

            self._run(table=table, sql=sql)
            self.table_info(table=table, msg=msg, is_show=is_show)

    def create_bottles_table(self, table: str, msg: str = '', is_show: bool = False) -> None:
        """
        创建漂流瓶表
        :param table: 数据表的名称
        :param msg: 运行时打印的提示信息
        :param is_show: 是否打印表格

        用法 ::

            >>> db.create_bottles_table(table='bottles')

        """
        if not self.is_connect:
            print(self.wrong_msg)

        else:
            # MySQL语句
            sql = f'''
                CREATE TABLE IF NOT EXISTS {table}(
                    id INT UNSIGNED AUTO_INCREMENT,
                    species TINYTEXT NOT NULL COMMENT 'human or alien',
                    owner TINYTEXT NOT NULL COMMENT 'owner of the bottle',
                    message TEXT, image TEXT COMMENT 'image path',
                    visited TINYINT UNSIGNED NOT NULL DEFAULT 0 COMMENT 'visited times',
                    add_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    last_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    PRIMARY KEY (id)
                )ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='information of drift bottles';
            '''
            if is_show and not msg:
                msg = '数据表创建成功😊，表的结构如下：'

            self._run(table=table, sql=sql)
            self.table_info(table=table, msg=msg, is_show=is_show)

    def create_bottles_relay_table(self, table: str, msg: str = '', is_show: bool = False) -> None:
        """
        创建接力漂流瓶表
        :param table: 数据表的名称
        :param msg: 运行时打印的提示信息
        :param is_show: 是否打印表格

        用法 ::

            >>> db.create_bottles_relay_table(table='bottles_relay')

        """
        if not self.is_connect:
            print(self.wrong_msg)

        else:
            # MySQL语句
            sql = f'''
                CREATE TABLE IF NOT EXISTS {table}(
                    id INT UNSIGNED AUTO_INCREMENT,
                    owner TINYTEXT NOT NULL COMMENT '漂流信息的发送者',
                    message TEXT,
                    add_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (id)
                )ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='漂流瓶接力';
            '''
            if is_show and not msg:
                msg = '数据表创建成功😊，表的结构如下：'

            self._run(table=table, sql=sql)
            self.table_info(table=table, msg=msg, is_show=is_show)
    
    def select_all(self, table: str, msg: str = '', is_show: bool = False) -> List[Dict]:
        """
        查询表的全部数据
        :param table: 数据表的名称
        :param msg: 运行时打印的提示信息
        :param is_show: 是否打印表格
        :return: 查询的结果

        用法 ::

            >>> db.select_all(table='bottles')

        """
        if not self.is_connect:
            print(self.wrong_msg)

        else:
            # MySQL语句
            sql = f'''
                SELECT * FROM {table};
            '''
            if is_show and not msg:
                msg = '数据表查询成功😊，全部数据如下：'

            results = self._run(table=table, sql=sql, msg=msg)

            return results

    def user_info(self, table: str, user_name: str, msg: str = '', is_show: bool = False) -> Dict:
        """
        查询用户信息
        :param table: 数据表的名称
        :param user_name: 用户名
        :param msg: 运行时打印的提示信息
        :param is_show: 是否打印表格
        :return: 用户信息

        用法 ::

            >>> res = db.user_info(table='users', user_name='九月的海风')
            res = {
                'id': 3,
                'name': '九月的海风',
                'score': 10,
                'grade': '青铜'
            }

        """
        if not self.is_connect:
            print(self.wrong_msg)

        else:
            # MySQL语句
            sql = f'''
                SELECT * FROM {table} WHERE BINARY name="{strings.check(user_name)}";
            '''
            if is_show and not msg:
                msg = '用户查询成功😊，全部数据如下：'

            results = self._run(table=table, sql=sql, msg=msg)

            if results:
                res = {
                    'id': results[0]['id'],
                    'name': results[0]['name'],
                    'score': results[0]['score'],
                    'grade': results[0]['grade']
                }

                return res

    def is_user(self, table: str, user_name: str, msg: str = '', is_show: bool = False) -> bool:
        """
        查询用户是否在数据库里
        :param table: 数据表的名称
        :param user_name: 用户名
        :param msg: 运行时打印的提示信息
        :param is_show: 是否打印表格
        :return: 真假

        用法 ::

            >>> res = db.is_user(table='users', user_name='九月的海风')
            >>> print(res)
            True

        """
        if not self.is_connect:
            print(self.wrong_msg)

        else:
            res = self.user_info(table=table, user_name=user_name, msg=msg, is_show=is_show)

            if res:
                return True
            else:
                return False

    def award(self, table: str, user_name: str, score: int, msg: str = '', is_show: bool = False) -> Dict:
        """
        用户完成任务积分增加
        :param table: 数据表的名称
        :param user_name: 用户名
        :param score: 增加的分数
        :param msg: 运行时打印的提示信息
        :param is_show: 是否打印表格
        :return: 用户等级是否提升，用户的等级

        用法 ::

            >>> res = db.award(
                table='users',
                user_name='九月的海风',
                score=10
            )
            res = {
                'is_grade_up': True,
                'score': 20,
                'grade': '钻石'
            }

        """
        if not self.is_connect:
            print(self.wrong_msg)

        else:
            if is_show and not msg:
                msg = '用户积分增加成功😊，信息如下：'

            res = self.user_info(table=table, user_name=user_name)
            user_id = res['id']
            old_score = res['score']
            new_score = old_score + score
            old_grade = res['grade']
            new_grade = ''
            for _grade, _score in self.grade_rule.items():
                if new_score < _score:
                    new_grade = _grade
                    break

            self.update(
                table=table,
                content=f'score={new_score}, grade="{new_grade}"',
                condition=f'id={user_id}'
            )
            is_grade_up = False if new_grade == old_grade else True
            res = {
                'is_grade_up': is_grade_up,
                'score': new_score,
                'grade': new_grade
            }
            self.user_info(table=table, user_name=user_name, msg=msg, is_show=is_show)

            return res

    def sign_up(self, table: str, user_name: str, msg: str = '', is_show: bool = False) -> None:
        """
        用户注册
        :param table: 数据表的名称
        :param user_name: 用户名
        :param msg: 运行时打印的提示信息
        :param is_show: 是否打印表格

        用法 ::

            >>> db.sign_up(table='users', user_name='九月的海风')

        """
        if not self.is_connect:
            print(self.wrong_msg)

        else:
            if self.is_user(table=table, user_name=user_name):
                res = self.user_info(table=table, user_name=user_name)
                self.delete(table=table, condition=f'id={res["id"]}')

            # MySQL语句
            sql = f'''
                INSERT INTO {table} (name, grade) VALUES ("{strings.check(user_name)}", "青铜");
            '''
            if not msg:
                msg = '用户注册成功😊，全部用户如下：'

            self._run(table=table, sql=sql)
            self.select_all(table=table, msg=msg, is_show=is_show)

    def get_bottle(self, table: str, msg: str = '', is_show: bool = False) -> Tuple[str]:
        """
        获取漂流瓶的信息
        :param table: 数据表的名称
        :param msg: 运行时打印的提示信息
        :param is_show: 是否打印表格
        :return: 漂流瓶的文本信息, 漂流瓶的图片信息

        用法 ::

            >>> message, image = db.get_bottle(table='bottles')
            >>> print('message:', message)
            >>> print('image:', image)
            message: 这是一条测试信息
            image: 3.jpg

        """
        if not self.is_connect:
            print(self.wrong_msg)

        else:
            # MySQL语句
            sql = f'''
                SELECT * FROM {table} ORDER BY visited, add_time;
            '''
            if is_show and not msg:
                msg = '数据表排序成功😊，全部数据如下：'

            # 获取漂流瓶的文本和图片信息
            results = self._run(table=table, sql=sql, msg=msg)
            message = results[0]['message']
            image = results[0]['image']

            # 修改漂流瓶的访问次数
            id = results[0]['id']
            visited = results[0]['visited']
            self.update(table=table, content=f'visited={visited + 1}', condition=f'id={id}')

            return message, image

    def get_bottles_relay(self, table: str, msg: str = '', is_show: bool = False) -> List[str]:
        """
        获取接力漂流瓶的所有信息
        :param table: 数据表的名称
        :param msg: 运行时打印的提示信息
        :param is_show: 是否打印表格
        :return: 接力漂流瓶的文本信息

        用法 ::

            >>> messages = db.get_bottles_relay(table='bottles_relay')
            >>> print('messages:', messages)
            messages: ['这是一条测试信息', '这是另一条测试信息']

        """
        if not self.is_connect:
            print(self.wrong_msg)

        else:
            # 获取接力漂流瓶的文本信息
            results = self.select_all(table=table, msg=msg, is_show=is_show)
            messages: List[str] = [result['message'] for result in results]

            return messages
    
    def insert(self, table: str, owner: str, message: str, on_img: bool, msg: str = '', is_show: bool = False) -> Optional[str]:
        """
        发送一个漂流瓶
        :param table: 数据表的名称
        :param owner: 漂流瓶的发送者
        :param message: 文本信息
        :param on_img: 是否发送图片
        :param msg: 运行时打印的提示信息
        :param is_show: 是否打印表格
        :return: 图片名

        用法 ::

            >>> img = db.insert2(
                    table='bottles',
                    owner='细菌',
                    message='这是一条测试信息',
                    on_img=True
                )
            >>> print(img)
            3.jpg

        """
        if not self.is_connect:
            print(self.wrong_msg)

        else:
            # MySQL语句
            sql = f'''
                INSERT INTO {table} (species, owner, message, image) VALUES ("human", "{strings.check(owner)}", "{strings.check(message)}", "");
            '''
            if is_show and not msg:
                msg = '数据插入成功😊，全部数据如下：'

            self._run(table=table, sql=sql)
            results = self.select_all(table=table)
            if on_img:
                id = results[-1]['id']
                image = str(id) + '.jpg'
                self.update(table=table, content=f'image="{image}"', condition=f'id={id}', msg=msg, is_show=is_show)

                return image

    def relay(self, table: str, owner: str, message: str, msg: str = '', is_show: bool = False) -> None:
        """
        漂流瓶接力
        :param table: 数据表的名称
        :param owner: 漂流瓶的发送者
        :param message: 文本信息
        :param msg: 运行时打印的提示信息
        :param is_show: 是否打印表格

        用法 ::

            >>> db.relay(
                    table='bottles_relay',
                    owner='细菌',
                    message='这是一条测试信息'
                )

        """
        if not self.is_connect:
            print(self.wrong_msg)

        else:
            # MySQL语句
            sql = f'''
                INSERT INTO {table} (owner, message) VALUES ("{strings.check(owner)}", "{strings.check(message)}");
            '''
            if is_show and not msg:
                msg = '数据插入成功😊，全部数据如下：'

            self._run(table=table, sql=sql)
            self.select_all(table=table, msg=msg, is_show=is_show)
    
    def update(self, table: str, content: str, condition: str, msg: str = '', is_show: bool = False) -> None:
        """
        更改数据的信息
        :param table: 数据表的名称
        :param content: 要更改的内容
        :param condition: 查询的条件
        :param msg: 运行时打印的提示信息
        :param is_show: 是否打印表格

        用法 ::

            >>> db.update(
                    table='bottles',
                    content='visited=1',
                    condition='id=2'
                )

        """
        if not self.is_connect:
            print(self.wrong_msg)

        else:
            # MySQL语句
            sql = f'''
                UPDATE {table} SET {content} WHERE {condition};
            '''
            if is_show and not msg:
                msg = '数据修改成功😊，全部数据如下：'

            self._run(table=table, sql=sql)
            self.select_all(table=table, msg=msg, is_show=is_show)

    def delete(self, table: str, condition: str, msg: str = '', is_show: bool = False) -> None:
        """
        删除数据
        :param table: 数据表的名称
        :param condition: 查询的条件
        :param msg: 运行时打印的提示信息
        :param is_show: 是否打印表格

        用法 ::

            >>> db.delete(
                    table='bottles',
                    condition='id=3'
                )

        """
        if not self.is_connect:
            print(self.wrong_msg)

        else:
            # MySQL语句
            sql = f'''
                DELETE FROM {table} WHERE {condition};
            '''
            if is_show and not msg:
                msg = '数据删除成功😊，全部数据如下：'

            self._run(table=table, sql=sql)
            self.select_all(table=table, msg=msg, is_show=is_show)

    def clear_table(self, table: str, msg: str = '', is_show: bool = False) -> None:
        """
        清空数据表
        :param table: 数据表的名称
        :param msg: 运行时打印的提示信息
        :param is_show: 是否打印表格

        用法 ::

            >>> db.clear_table(table='bottles')

        """
        if not self.is_connect:
            print(self.wrong_msg)

        else:
            # MySQL语句
            sql = f'''
                TRUNCATE TABLE {table};
            '''
            if is_show and not msg:
                msg = '数据表清空成功😊，表的结构如下：'

            self._run(table=table, sql=sql)
            self.table_info(table=table, msg=msg, is_show=is_show)

    def delete_table(self, table: str, msg: str = '') -> None:
        """
        删除数据表
        :param table: 数据表的名称
        :param msg: 运行时打印的提示信息

        用法 ::

            >>> db.delete_table(table='bottles')

        """
        if not self.is_connect:
            print(self.wrong_msg)

        else:
            # MySQL语句
            sql = f'''
                DROP TABLE {table};
            '''
            if not msg:
                msg = '数据表删除成功😊'

            self._run(table=table, sql=sql)
            print(msg)


if __name__ == '__main__':
    db = MySQL(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_DATABASE')
    )
    db.create_table(table='bottles')
    db.select_all(table='bottles')
    db.insert(
        table='bottles',
        owner='九月的海风',
        message='这是一条测试信息',
        on_img=True
    )
    db.update(
        table='bottles',
        content='visited=1',
        condition='id=2'
    )
    db.delete(
        table='bottles',
        condition='id=1'
    )
    db.delete_table(table='users')
