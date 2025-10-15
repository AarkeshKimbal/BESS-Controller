from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas import Decision
from app.service import SourceDataLoader, optimize_for_interval
from app.models import OptimizationLog

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/decisions", response_model=list[Decision])
def get_all_decisions(interval_len: int = None, db: Session = Depends(get_db)):
    loader = SourceDataLoader(db)
    if interval_len is None:
        interval_len = loader.get_interval_minutes()
    logs = db.query(OptimizationLog).filter(
        OptimizationLog.interval % interval_len == 0
    ).order_by(OptimizationLog.interval).all()
    return logs

@router.post("/run-optimization")
def run_optimization(db: Session = Depends(get_db)):
    loader = SourceDataLoader(db)
    try:
        required_energy = loader.get_param_value("required_energy")
        initial_soc = loader.get_param_value("initial_soc")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    interval_minutes = loader.get_interval_minutes()
    num_blocks = int(24 * 60 / interval_minutes)
    soc = initial_soc
    for t in range(num_blocks):
        optimize_for_interval(loader, required_energy, soc, t)
        # TODO: Update SOC after each interval (battery model dependent)
    return {"status": "Optimization completed"}
