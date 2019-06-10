
import urllib.request 
from xml.etree import ElementTree as ET
import json
 

class CurrenciesXMLData:
    """Класс для получения данных с сайта Центробанка РФ"""

    def get_currencies(self):
      resp = ET.parse(urllib.request.urlopen("http://www.cbr.ru/scripts/XML_daily.asp"))
    #распарсиваем данные с сайта 
      valutes = {}
    #findall - находит только элементы с тегом, которые являются прямыми потомками текущего элемента
      for row in resp.findall('Valute'):
        valutes.update({row.find('CharCode').text: float(row.find('Value').text.replace(",", "."))})
      valutes.update({'RUB': 1})
      return valutes


class CurrenciesJSONData:
    """ 
        Декоратор CurrenciesJSONData, позволяющий преобразовывать данные, 
        имеющиеся в классе CurrenciesXMLData, в формат JSON. 
    """

    def __init__(self, obj):
        self.obj = obj

    def get_currencies(self):
        """
              Метод dumps = сделай мне из dict json
              Аргумент indent = количество пробелов в отступах
        """
        return json.dumps(self.obj.get_currencies(), indent=5)

    def serialize(self):
        """
            Метод serialize() в декораторе, который позволяет сохранять данные в файл в формате JSON.
        """
        with open('data.json', 'w', encoding='utf-8') as f:
            f.write(self.get_currencies())



data = CurrenciesXMLData()
data= CurrenciesJSONData(data)
print(data.get_currencies())
data.serialize()
