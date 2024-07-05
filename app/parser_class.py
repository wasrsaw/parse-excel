import pandas as pd
import openpyxl
import json

"""
Здесь основной функционал, мы парсим excel файл.

"""
#TODO: Рефакторинг

ws = openpyxl.load_workbook("/Users/ilyabarinov/Downloads/Telegram Desktop/2024spr2p.xlsx").active

groups = {}
max_column = ws.max_column
max_row = ws.max_row

groups_row = 2
weekday_column = 1
para_column = 2


for col in range(1, max_column+1):
    group = ws.cell(row=groups_row, column=col).value
    if group:  # Проверяем, что ячейка не пуста
        weekday_paras = {}  

        for row1 in range(groups_row+1, max_row):
            weekday = ws.cell(row=row1, column=weekday_column).value
            if weekday:
                paras = {}
                row2 = row1
                order = ws.cell(row=row2, column=para_column).value
                lesson = ws.cell(row=row2, column=col).value
                prepod = ws.cell(row=row2, column=col+1).value
                paras[f"Para {order}"] = [{"lesson": lesson, "prep": prepod}]
                while True:
                    
                    row2 += 1
                    check_day = ws.cell(row=row2, column=weekday_column).value
                    cell_value = ws.cell(row=row2, column=para_column).value
                    lesson = ws.cell(row=row2, column=col).value
                    prepod = ws.cell(row=row2, column=col+1).value

                    if (check_day and check_day != weekday) or row2 >= max_row:
                        weekday_paras[weekday] = paras
                        break

                    if cell_value:
                        order = cell_value
                        paras[f"Para {order}"] = []
            
                    if lesson or prepod:
                        paras[f"Para {order}"].append({"lesson": lesson, "prep": prepod})

        groups[group] = weekday_paras              

with open('rasp2.json', 'w', encoding='utf-8') as file:
    # Записываем словарь в файл
    json.dump(groups, file, ensure_ascii=False, indent=4)