from sqlalchemy.orm import Session
from app.models import (
    Source, SourceOAParam, SourceTariffData,
    OptimizationLog, IntervalConfig, Schedule, OptimizationParams
)
from typing import Dict

class SourceDataLoader:
    def __init__(self, session: Session):
        self.session = session

    def get_active_schedule(self):
        return (
            self.session.query(Schedule)
            .filter(Schedule.active == True)
            .order_by(Schedule.id.desc())
            .first()
        )

    def get_interval_minutes(self):
        schedule = self.get_active_schedule()
        if schedule and schedule.interval_config:
            return schedule.interval_config.interval_minutes
        cfg = self.session.query(IntervalConfig).order_by(IntervalConfig.id.desc()).first()
        return cfg.interval_minutes if cfg else 15

    def get_param_value(self, param_name: str):
        param = self.session.query(OptimizationParams).filter_by(param_name=param_name).first()
        if param:
            return param.param_value
        raise ValueError(f"Parameter '{param_name}' not found in optimization_params table")

    def read_sources(self) -> Dict[str, Dict]:
        sources = {}
        for s in self.session.query(Source):
            params = self.session.query(SourceOAParam).filter(SourceOAParam.source_id == s.id).all()
            charges = {p.param_name: p.param_value for p in params if p.param_type == 'charge'}
            losses = {p.param_name: p.param_value for p in params if p.param_type == 'loss'}
            tariffs = self.session.query(SourceTariffData).filter(SourceTariffData.source_id == s.id).all()
            tariff_by_interval = {d.interval: d.tariff for d in tariffs}
            cap_by_interval = {d.interval: d.capacity for d in tariffs}
            sources[s.name] = {
                "charges": charges,
                "losses": losses,
                "tariff": tariff_by_interval,
                "capacity": cap_by_interval
            }
        return sources

    def log_decision(self, interval, source, energy, cost_per_kWh, landed_cost, soc, comments):
        log = OptimizationLog(
            interval=interval,
            source=source,
            energy=energy,
            cost_per_kWh=cost_per_kWh,
            landed_cost=landed_cost,
            soc=soc,
            comments=comments
        )
        self.session.add(log)
        self.session.commit()

#Basic Logic - Complex logics to be constructed

def optimize_for_interval(loader: SourceDataLoader, required_energy: float, soc: float, interval: int):
    sources = loader.read_sources()
    allocation = []
    left = required_energy
    for name, s in sources.items():
        tar = s["tariff"].get(interval, 0)
        cap = s["capacity"].get(interval, 0)
        charges = sum(s["charges"].values())
        losses = sum(s["losses"].values())
        loss_factor = 1 - losses
        landed_cost = (tar + charges) / (loss_factor if loss_factor > 0 else 1e-6)
        alloc = min(left, cap)
        if alloc > 0:
            allocation.append((name, alloc, landed_cost))
            loader.log_decision(interval, name, alloc, landed_cost, landed_cost, soc, "Optimized allocation")
            left -= alloc
        if left <= 0:
            break
    return allocation
