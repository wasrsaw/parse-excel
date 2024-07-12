from app.parser_class import XParser
import json

PATH = ""

parser = XParser(PATH)

with open('rasp.json', 'w', encoding='utf-8') as file:
    # Записываем словарь в файл
    json.dump(parser.parse(), file, ensure_ascii=False, indent=4)
