import random


def probability(ratio: int) -> bool:
    """
    概率
    :param ratio: 0-10 -> 0%-100%
    :return: 真假

    用法 ::

        >>> import randoms
        >>> prob = randoms.probability(ratio=8)
        >>> print(prob)
        True

    """
    num = random.randint(0, 9)
    if num < ratio:
        return True
    else:
        return False


if __name__ == '__main__':
    prob = probability(ratio=8)
    print(prob)
