from fastapi import APIRouter
from .view_data import router as view_router
from .upload_data import router as update_router

router = APIRouter()

router.include_router(view_router)
router.include_router(update_router)

