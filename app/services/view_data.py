from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from io import BytesIO
from rasp_parser.rasp_parser import XParser


router = APIRouter(prefix="/view")

@router.get("/schedule-excel")
async def schedule_parse(file: UploadFile = File(...)):
    """
    Просмотр распарсенного расписания в JSON формате
    """
    try:
        schedule = await file.read()
        parser = XParser(BytesIO(schedule))
        response = parser.parse()
        return response
    except Exception as e:
        return JSONResponse(content={"ERROR": str(e)}, status_code=400) 

   
