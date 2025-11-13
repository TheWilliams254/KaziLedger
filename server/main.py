from fastapi import FastAPI
from app.routers import api_router
from app.database import init_db
import uvicorn

app = FastAPI(
    title="KaziLedger API",
    description="Payroll & Attendance Management for Construction Subcontractors",
    version="1.0.0"
)
@app.on_event("startup")
def startup():
    init_db()

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)