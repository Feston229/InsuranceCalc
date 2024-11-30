from fastapi.routing import APIRouter
from insurance_calc.web.api import echo
from insurance_calc.web.api import dummy
from insurance_calc.web.api import redis
from insurance_calc.web.api import kafka
from insurance_calc.web.api import monitoring

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(echo.router, prefix="/echo", tags=["echo"])
api_router.include_router(dummy.router, prefix="/dummy", tags=["dummy"])
api_router.include_router(redis.router, prefix="/redis", tags=["redis"])
api_router.include_router(kafka.router, prefix="/kafka", tags=["kafka"])
