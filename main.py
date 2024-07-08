from app.parser_class import XParser
import json

PATH = "/Users/ilyabarinov/Downloads/Telegram Desktop/2024spr2p.xlsx"

parser = XParser(PATH)

with open('rasp.json', 'w', encoding='utf-8') as file:
    # Записываем словарь в файл
    json.dump(parser.parse(), file, ensure_ascii=False, indent=4)
