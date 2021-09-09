import pymysql

from flask import Flask
from flask import request


app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


@app.route('/database/check', methods=['GET', 'POST'])
def check():
    host = request.form['host']
    user = request.form['user']
    password = request.form['password']
    database = request.form['database']

    code: int
    info: str
    err: str

    try:
        # 检查数据库连接是否成功
        db = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            charset='utf8mb4'
        )
        db.close()
        code = 200
        info = '数据库连接成功😊'
        err = ''

    except Exception as e:
        code = 250
        info = '数据库连接失败😭'
        err = repr(e)

    res = {
        'code': code,
        'info': info,
        'err': err
    }

    return res


@app.route('/database/run', methods=['GET', 'POST'])
def run():
    host = request.form['host']
    user = request.form['user']
    password = request.form['password']
    database = request.form['database']
    sql = request.form['sql']

    code: int
    info: str
    err: str

    # 打开数据库连接
    db = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        charset='utf8mb4'
    )

    results = []

    # 创建cursor对象
    cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
    # print('sql:', sql)    # 方便调试

    try:
        # 执行MySQL语句
        cursor.execute(sql)

        # 提交到数据库执行
        db.commit()

        # 获取所有结果
        results = cursor.fetchall()
        # print('results:', results)    # 方便调试

        code = 200
        info = '执行成功'
        err = ''

    except Exception as e:
        # 如果发生错误则回滚
        db.rollback()

        code = 250
        info = '执行失败'
        err = repr(e)

    finally:
        # 关闭数据库连接
        cursor.close()
        db.close()

    res = {
        'code': code,
        'info': info,
        'err': err,
        'results': results
    }

    return res


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
