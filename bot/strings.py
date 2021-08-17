def check(msg: str) -> str:
    """
    对字符串中的特殊字符加上转义字符`/`
    :param msg: 输入字符串
    :return: 加上转义字符后的字符串

    用法 ::

        >>> import strings
        >>> msg = strings.check(msg="I'm a lovely pig.")
        >>> print(msg)
        I\\'m a lovely pig.

    """
    msg = msg.replace('\\', '\\\\')
    msg = msg.replace('"', '\\"')
    msg = msg.replace("'", "\\'")

    return msg



def symbolize(num: int) -> str:
    """
    将数字转换为符号
    :param num: 输入数字
    :return: 转换为符号后的字符串

    用法 ::

        >>> import strings
        >>> num_str = strings.symbolize(num=123)
        >>> print(num_str)
        1️⃣2️⃣3️⃣

    """
    num_str = ''
    label_map = {
        '0': '0️⃣',
        '1': '1️⃣',
        '2': '2️⃣',
        '3': '3️⃣',
        '4': '4️⃣',
        '5': '5️⃣',
        '6': '6️⃣',
        '7': '7️⃣',
        '8': '8️⃣',
        '9': '9️⃣'
    }
    for char in str(num):
        num_str += label_map[char]

    return num_str


if __name__ == '__main__':
    name = check(msg="I'm a lovely pig.")
    print(name)

    num_str = symbolize(123)
    print(num_str)
