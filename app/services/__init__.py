from fastapi import APIRouter
from .view_data import router as view_router
from .upload_data import router as upload_router
from .database_data import router as db_router

router = APIRouter()

router.include_router(view_router)
router.include_router(upload_router)
router.include_router(db_router)

