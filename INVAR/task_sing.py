from urllib.request import urlopen
from xml.etree import ElementTree as ET
import time

def get_currencies(currencies_ids_lst=['R01235', 'R01239', 'R01820']):
    """
    Функция позволяет получать данные о текущих курсах валют с сайта Центробанка РФ
    """
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
        return self.currencies[code]

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
        new_val = get_currencies(self.currencies)
        self.rates.update(dict(zip(sorted(self.currencies),new_val.values())))
        return self.rates

    def check(self):
        """
        Метод проверки загружены ли данные и если прошло 
        больше 5 минут с момента последней загрузки, то отправлялся бы запрос к серверу
        """
        if (time.clock() > 300):
            return get_currencies(self.currencies)
        else:
            print('Прошло слишком мало времени, последнее обновление было меньше 5-и минут назад')

#get_data = get_currencies()
#print(get_data)
