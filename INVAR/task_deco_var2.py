from urllib.request import urlopen
from xml.etree import ElementTree as ET
import xmltodict
from json import dumps
from abc import ABCMeta, abstractmethod

class Interface(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def get_data(self):
        pass

class CurrenciesXMLData(Interface):
    """Класс для получения данных с сайта Центробанка РФ"""

    def get_data(self):
        cur_res_str = urlopen("http://www.cbr.ru/scripts/XML_daily.asp")
        return ET.tostring(ET.parse(cur_res_str).getroot(),encoding="unicode")


class CurrenciesJSONData(Interface):
    """ 
        Декоратор CurrenciesJSONData, позволяющий преобразовывать данные, 
        имеющиеся в классе CurrenciesXMLData, в формат JSON. 
    """
    def __init__(self, obj):
        self.obj = obj

    def get_currencies(self):
        """
        Преобразовываем данные в JSON формат
        """
        cur_res_str = urlopen("http://www.cbr.ru/scripts/XML_daily.asp")
        root = ET.tostring(ET.parse(cur_res_str).getroot(),encoding="unicode")
        return dumps(xmltodict.parse(root, encoding='utf-8'), ensure_ascii=False)

    def serialize(self):
        """
            Метод serialize() в декораторе, который позволяет сохранять данные в файл в формате JSON.
        """
        with open('data.json', 'w', encoding='utf-8') as f:
            f.write(self.get_currencies())

data = CurrenciesXMLData()
valute = CurrenciesJSONData(data)
print(valute.get_currencies())
valute.serialize()
