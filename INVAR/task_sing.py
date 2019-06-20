from urllib.request import urlopen
from xml.etree import ElementTree as ET
import time


def get_currencies(currencies_ids_lst=['R01239', 'R01235', 'R01035']):
    cur_res_str = urlopen("http://www.cbr.ru/scripts/XML_daily.asp")
    result = {}
    cur_res_xml = ET.parse(cur_res_str)
    root = cur_res_xml.getroot()
    valutes = root.findall('Valute')
    for el in valutes:
        valute_id = el.get('ID')
        if str(valute_id) in currencies_ids_lst:
            valute_cur_val = el.find('Value').text
            result[valute_id] = valute_cur_val
    time.clock()
    return result


def singleton(cls):
    """
    Пример реализации одиночки на Python по материалам лекции
    """
    instances = {}
    def get_instance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return get_instance


@singleton
class CurrencyBoard():
    """
    Создание класса-синглтон/одиночки
    """
    def __init__(self):
        """
        Инициализируем переменные
        Храним данные о валютах
        """
        self.currencies = ['R01235','R01239','R01820']
        self.rates = get_currencies(self.currencies)

    def get_currency_saving(self, code):
        """
        Метод для получения информации о всех сохраненных в кэше валютах без запроса к сайту
        """
        return self.rates.setdefault(code)

    def get_new_currency(self, code):
        """
        Метод о запросе курса новой валюты (с получением свежих данных с сервера) и добавлением её в кэш
        """
        self.currencies.append(code)
        self.rates.update(get_currencies([code]))
        return self.rates[code]

    def update(self):
        """
        Метод класса для принудительного обновления данных о валютах
        """
        self.rates.clear()
        self.rates = get_currencies(self.currencies)
        return self.rates

    def check(self):
        """
        Метод проверки загружены ли данные и если прошло 
        больше 5 минут с момента последней загрузки, то отправлялся бы запрос к серверу
        """
        if (time.clock() > 300):
            return self.update()
        else:
            print('Прошло слишком мало времени, последнее обновление было меньше 5-и минут назад')


#data = CurrencyBoard()
#print('Курс валюты:', data.rates)
