import json
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from io import BytesIO

import logging
from utils.exceptions import *
from rasp_parser.rasp_parser import XParser
from database.db_class import Database


router = APIRouter(prefix="/database")

db = Database()

@router.get("/update-from-json")
async def update_database():
    try:
        db.reset_data()

        #-------------------- Распаковывем JSON  с информацией о группах, преподавателях и предметах --------------------
        with open("info.json", "r") as info_file:
            info = json.load(info_file)

        for prep in info["Преподаватели"]:
            fio = prep["ФИО"]
            chair = prep["Должность"]
            degree = prep["Степень"]
            photo = prep["Фото"]
            student_id = 0 #int(prep["Student_id"])
            archive = False #bool(prep["Архив"])
            db.set_prep(fio, chair, degree, photo, student_id, archive)

        for subj in info["Предметы"]:
            db.set_subj(subj)

        for group in info["Группы"]:
            db.set_group(group)

        #-------------------- Распаковывем информацию с расписанием --------------------
        with open("rasp.json", "r") as rasp_file:
            rasp = json.load(rasp_file)
        
        for group in list(rasp):
            if group not in info["Группы"]:
                raise GroupNotFound(group)
            
            for weekday in rasp[group]:
                for i in range(0, len(rasp[group][weekday])):
                    para = rasp[group][weekday][i]
                    # Проверка правильности названия предмета
                    lesson = para["Пара"]
                    for subj in info["Предметы"]:
                        if subj.lower() in lesson.lower():
                            lesson = subj
                            break
                    db.set_subj(lesson)
                    
                    # Проверка правильности фамилии преподавателя
                    prep = para["Преподаватель"] 
                    if prep is None:
                        prep = "Не указан"
                    else:
                        for prep_info in info["Преподаватели"]:
                            if prep in prep_info["ФИО"]:
                                prep = prep_info["ФИО"]
                                
                    if weekday == "ПН":
                        weekday_order = 1
                    elif weekday == "ВТ":
                        weekday_order = 2
                    elif weekday == "СР":
                        weekday_order = 3
                    elif weekday == "ЧТ":
                        weekday_order = 4
                    elif weekday == "ПТ":
                        weekday_order = 5
                    elif weekday == "СБ":
                        weekday_order = 6
                    elif weekday == "ВС": 
                        weekday_order = 7
                    
                    order = para["Порядок"]
                    subgroup = para["Подгруппа"]
                    weeks = para["Недели"]
                    parity = para["Четность"]

                    db.set_rasp(lesson, prep, group, weekday_order)
        return JSONResponse(content={"SUCCESS": "БД успешно обновлена"}, status_code=200)
    except Exception as e:
        # db.reset_data()
        return JSONResponse(content={"ERROR": str(e)}, status_code=400)
    
@router.get("/test")
async def test():
    try:
        db.set_group("KOLOMNA")
        return JSONResponse(content={"SUCCESS": "TEST Success"})
    except Exception as e:
        return JSONResponse(content={"ERRORR": str(e)}, status_code=400)

@router.get("/drop")
async def drop_database():
    try:
        db.reset_data()
        return {"status": "БД успешно сброшена"}
    except Exception as e:
        return JSONResponse(content={"ERROR": str(e)}, status_code=400)