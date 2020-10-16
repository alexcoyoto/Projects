from functools import partial


class User:
    user_id = 0
    name = 'unknown'
    password = '123'
    email = 'unknown@gmail.com'
    books = ''
    coins = 0
    image = 'question.png'

    # РЕАЛИЗАЦИЯ ПАТТЕРНА "ОДИНОЧКА" В КАЧЕСТВЕ КОНСТРУКТОРА КЛАССА
    def __new__(cls):
        # Перекрываем создание объекта класса
        if not hasattr(cls, 'instance'):
            cls.instance = super(User, cls).__new__(cls)
        return cls.instance

    def set(self, user_id, name, password, email, books, coins, image):
        self.user_id = user_id
        self.name = name
        self.password = password
        self.email = email
        self.books = books
        self.coins = coins
        self.image = image


class Statistics:
    info_id = 1
    total_downloads = 0
    total_users = 0
    total_earned = 50

    def set(self, info_id, total_downloads, total_users, total_earned):
        self.info_id = info_id
        self.total_downloads = total_downloads
        self.total_users = total_users
        self.total_earned = total_earned

    def clear(self):
        self.info_id = 0
        self.total_downloads = 0
        self.total_users = 0
        self.total_earned = 0


# РЕАЛИЗАЦИЯ ПАТТЕРНА "ЗАМЕСТИТЕЛЬ" В КАЧЕСТВЕ ОТЛОЖЕННОГО КЛАССА
class StatisticsProxy:
    def __init__(self):
        self.proxy_object = Statistics()
        self.operations = []

    def set(self, *args):
        func = partial(self.set, *args)
        self.operations.append(func)

    def clear(self, *args):
        func = partial(self.clear, *args)
        self.operations.append(func)


# РЕАЛИЗАЦИЯ ПАТТЕРНА "СТРАТЕГИЯ" В КАЧЕСТВЕ ГРУППЫ НЕЗАВИСИМЫХ КЛАССОВ
class SmallValue:
    @staticmethod
    def decode():
        print('few coins are collected')


class BigValue:
    @staticmethod
    def decode():
        print('a lot of coins are collected')


class Strategy(object):
    @classmethod
    def analyze(cls, value):
        if value <= 12:
            decoder = SmallValue
        elif value > 12:
            decoder = BigValue
        else:
            raise RuntimeError('Невозможно подобрать стратегию %s' % value)
        return cls(decoder.decode(), value)

    def __init__(self, byterange, filename):
        self._byterange = byterange
        self._filename = filename


class Book:
    title = 'unknown'
    author = 'unknown'
    price = 0

    def set(self, title, author, price):
        self.title = title
        self.author = author
        self.price = price

    def get(self):
        return self.title, self.author, self.price
