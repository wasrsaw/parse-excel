from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from io import BytesIO

from rasp_parser.rasp_parser import XParser
from database.db_class import Database


router = APIRouter(prefix="/schedule")

db = Database()


@router.post("/get-parse-excel")
async def schedule_parse(file: UploadFile = File(...)):
    try:
        schedule = await file.read()
        parser = XParser(BytesIO(schedule))
        response = parser.parse()
        return response
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)

@router.post("/drop-database")
async def drop_database():
    try:
        db.reset_data()
        return {"status": "БД успешно сброшена"}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)

@router.post("/update-database")
async def update_database(file: UploadFile = File(...)):
    try:
        schedule = await file.read()
        parser = XParser(BytesIO(schedule))
        response = parser.parse()
        return response
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)
