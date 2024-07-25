from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from io import BytesIO
import json

from rasp_parser.rasp_parser import XParser
from database.db_class import Database


router = APIRouter(prefix="/upload")

db = Database()

@router.post("/schedule-excel")
async def upload_preps(file: UploadFile = File(...)):
    """
    Парсинг расписания и обновление JSON файла
    """
    try:
        schedule = await file.read()
        parser = XParser(BytesIO(schedule))
        file = open("rasp.json", "w", encoding="utf-8")
        json.dump(parser.parse(), file, ensure_ascii=False, indent=2)
        return JSONResponse(content={"SUCCESS": "Расписание успешно преобразовано в JSON!"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"ERROR": str(e)}, status_code=400)


@router.post("info-json")
async def upload_preps(file: UploadFile = File(...)):
    """
    Обновления JSON с данными о преподавателях, предметах и группах
    """
    try:
        preps = await file.read()
        f = open("info.json", "wb")
        f.write(preps)
        return JSONResponse(content={"SUCCESS": "JSON список преподавателей успешно обновлен!"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"ERROR": str(e)}, status_code=400)
    