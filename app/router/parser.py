from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import Response

from services.parser_class import XParser

router = APIRouter()

@router.post("/update_rasp")
async def excel_generate():#file: UploadFile = File(...)):
    return {'message': '/update_rasp/'}

@router.get("/rasp")
async def give_parsed_data():
    return {'message': '/rasp/ А ты хорош'}


    