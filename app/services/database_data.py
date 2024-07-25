import json
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from io import BytesIO

from utils.exceptions import *
from rasp_parser.rasp_parser import XParser
from database.db_class import Database


router = APIRouter(prefix="/database")

db = Database()

@router.get("/update")
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
            student_id = int(prep["Student_id"])
            archive = bool(prep["Архив"])

            db.set_prep(fio, chair, degree, photo, student_id, archive)

        for subj in info["Предметы"]:
            db.set_subj(subj)

        for group in info["Группы"]:
            db.set_group(group)

        #-------------------- Распаковывем информацию с расписанием --------------------
        with open("rasp.json", "r") as rasp_file:
            rasp = json.load(rasp_file)
        
        for group in list(rasp):
            if group in info["Группы"]:
                db.set_group(group)
            else:
                raise GroupNotFound
            
            for weekday in rasp[group]:
                for i in range(0, len(rasp[group][weekday])):
                    para = rasp[group][weekday][i]

                    order = para["Порядок"]

                    # Проверка правильности названия предмета
                    para = para["Пара"]
                    for subj in info["Предметы"]:
                        if subj in para:
                            para = subj
                    if para is None or para == "":
                        raise SubjNotFound
                        
                    # Проверка правильности фамилии преподавателя
                    prep = para["Преподаватель"] 
                    for prep_info in info["Преподаватели"]:
                        if prep in prep_info["ФИО"]:
                            prep = prep_info["ФИО"]

                    subgroup = para["Подгруппа"]
                    weeks = para["Недели"]
                    parity = para["Четность"]
                    weekday = int(weekday)

                    db.set_rasp(para, prep, group, weekday)
        return JSONResponse(content={"SUCCESS": "БД успешно обновлена"}, status_code=200)
    except Exception as e:
        db.reset_data()
        return JSONResponse(content={"ERRORR": str(e)}, status_code=400)
    
@router.post("/drop")
async def drop_database():
    try:
        db.reset_data()
        return {"status": "БД успешно сброшена"}
    except Exception as e:
        return JSONResponse(content={"ERROR": str(e)}, status_code=400)