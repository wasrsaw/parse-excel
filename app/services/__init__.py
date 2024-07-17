from fastapi import APIRouter
from .schedule_parse import router as parser_router

router = APIRouter()

router.include_router(parser_router)

