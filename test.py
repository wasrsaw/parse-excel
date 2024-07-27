
a = {
    "КМБО-02-23": {
        "ПН": 
            [
                {
                    "Пара": "Мет.и ст.прогр.(2пг)",
                    "Преподаватель": "Смирнов",
                    "Подгруппа": "2пг",
                    "Недели": None,
                    "Четность": None
                }
            ]
    },
    "КМБО-02-25": {
        "ПН": 
            [
                {
                    "Пара": "Мет.и ст.прогр.(2пг)",
                    "Преподаватель": "Смирнов",
                    "Подгруппа": "2пг",
                    "Недели": None,
                    "Четность": None
                }
            ]
    }
}


# from app.rasp_parser.rasp_parser import XParser
# import json 

# with open("/Users/ilyabarinov/Desktop/WORK/ПРАКТИКА/parse-excel/rasp.json", "r") as fp:
#     dict = json.load(fp)
# print(list(dict['КМБО-02-23']))
# # parser = XParser("/Users/ilyabarinov/Desktop/WORK/ПРАКТИКА/parse-excel/2024spr2p.xlsx")

# # parse = parser.parse()
# # with open("rasp.json", "w", encoding='utf8') as fp:
# #     json.dump(parse, fp, ensure_ascii=False, indent=2)
# #     # fp.write(js)

a = "IIн Прогр. в ЗРЛ (2пг)"
print(a.split("\n")[0])