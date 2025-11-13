from fastapi import APIRouter
from . import auth_routes, subcontractors, workers, attendance, payouts, mpesa

# Create a main router
api_router = APIRouter()

api_router.include_router(auth_routes.router, prefix="/auth", tags=["Auth"])
api_router.include_router(subcontractors.router, prefix="/subcontractors", tags=["Subcontractors"])
api_router.include_router(workers.router, prefix="/workers", tags=["Workers"])
api_router.include_router(attendance.router, prefix="/attendance", tags=["Attendance"])
api_router.include_router(payouts.router, prefix="/payouts", tags=["Payouts"])
api_router.include_router(mpesa.router, prefix="/mpesa", tags=["Mpesa"])
