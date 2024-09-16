import json
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from utils.exceptions import *
from database.db_class import Database


router = APIRouter(prefix="/database")

db = Database()

@router.get("/update-from-json")
async def update_database():
    """
    Обновляем информацию в БД из JSON файлов. 
    Тут происходит распаковка распаршенных данных из JSON файла
    """
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
            student_id = prep["Student_id"]
            archive = prep["Архив"]
            db.set_prep(fio, chair, degree, photo, student_id, archive)

        for subj in info["Предметы"]:
            db.set_subj(subj)

        for group in info["Группы"]:
            db.set_group(group)

        #-------------------- Подгатавливаем информацию для заполнения БД --------------------
        with open("rasp.json", "r") as rasp_file:
            rasp = json.load(rasp_file)
        
        for group in list(rasp):
            if group not in info["Группы"]:
                raise GroupNotFound(group)
            
            for weekday in rasp[group]:
                for i in range(0, len(rasp[group][weekday])):
                    para = rasp[group][weekday][i]

                    # Проверка правильности названия предмета
                    disc = para["Пара"]
                    for subj in info["Предметы"]:
                        if disc and (subj.lower() in disc.lower()):
                            disc = subj
                            break
                    db.set_subj(disc)
                    
                    # Проверка правильности фамилии преподавателя
                    preps = []
                    if para["Преподаватель"] is None:
                        preps.append("Не указан")
                    else:
                        prep = para["Преподаватель"].split("\n")
                        for fio in prep:
                            for prep_info in info["Преподаватели"]:
                                if fio and (fio.lower() in prep_info["ФИО"].lower()):
                                    preps.append(prep_info["ФИО"])
                                    break
                            if fio not in preps:
                                preps.append(fio)
                                db.set_prep(fio)

                    if preps == []:
                        raise PrepNotFound(para["Преподаватель"])
                                
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
                    else:
                        raise WeekdayNotFound(weekday)
                    
                    lesson = para["Порядок"]
                    subgroup = para["Подгруппа"]
                    week = para["Четность"]
                    
                    for prep in preps:
                        db.set_rasp(disc, prep, group, weekday_order, week, lesson, subgroup)
        return JSONResponse(content={"SUCCESS": "БД успешно обновлена"}, status_code=200)
    except Exception as e:
        db.reset_data()
        return JSONResponse(content={"ERROR": str(e)}, status_code=400)

@router.get("/drop")
async def drop_database():
    try:
        db.reset_data()
        return JSONResponse(content={"SUCCESS": "БД успешно сброшена"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"ERROR": str(e)}, status_code=400)