from fastapi.routing import APIRouter

from insurance_calc.web.api import auth, insurance, kafka, monitoring

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(insurance.router, prefix="/insurance", tags=["insurance"])
api_router.include_router(kafka.router, prefix="/kafka", tags=["kafka"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
