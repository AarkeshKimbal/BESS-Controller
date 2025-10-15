from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()

class IntervalConfig(Base):
    __tablename__ = "interval_config"
    id = Column(Integer, primary_key=True, index=True)
    interval_minutes = Column(Integer, default=15, nullable=False)

class Schedule(Base):
    __tablename__ = "schedules"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    interval_config_id = Column(Integer, ForeignKey("interval_config.id"))
    active = Column(Boolean, default=True)

    interval_config = relationship("IntervalConfig", backref="schedules")

class Source(Base):
    __tablename__ = 'sources'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

class SourceOAParam(Base):
    __tablename__ = 'source_oa_params'
    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, ForeignKey('sources.id'))
    param_type = Column(String)  # 'charge' or 'loss'
    param_name = Column(String)
    param_value = Column(Float)

class SourceTariffData(Base):
    __tablename__ = 'source_tariff_data'
    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, ForeignKey('sources.id'))
    interval = Column(Integer, nullable=False, index=True)
    tariff = Column(Float, nullable=False)
    capacity = Column(Float, nullable=False)

class OptimizationLog(Base):
    __tablename__ = 'optimization_log'
    id = Column(Integer, primary_key=True, index=True)
    ts = Column(DateTime, default=func.now())
    interval = Column(Integer, nullable=False, index=True)
    source = Column(String, nullable=False)
    energy = Column(Float, nullable=False)
    cost_per_kWh = Column(Float, nullable=False)
    landed_cost = Column(Float, nullable=False)
    soc = Column(Float, nullable=False)
    comments = Column(String)

class OptimizationParams(Base):
    __tablename__ = 'optimization_params'
    id = Column(Integer, primary_key=True, index=True)
    param_name = Column(String, unique=True, nullable=False)
    param_value = Column(Float, nullable=False)
