from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime, Enum as SQLEnum
from sqlalchemy.sql import func
from datetime import datetime
from enum import Enum
from config.database import Base


class VehicleType(str, Enum):
    """Vehicle temperature type"""
    FROZEN = "frozen"  # 냉동 (-18°C ~ -25°C)
    CHILLED = "chilled"  # 냉장 (0°C ~ 6°C)
    MULTI = "multi"  # 겸용 (냉동/냉장 구획 분리)
    AMBIENT = "ambient"  # 상온


class VehicleStatus(str, Enum):
    """Vehicle operational status"""
    AVAILABLE = "available"  # 배차 가능
    DISPATCHED = "dispatched"  # 배차됨
    IN_TRANSIT = "in_transit"  # 운행중
    LOADING = "loading"  # 상차중
    UNLOADING = "unloading"  # 하차중
    MAINTENANCE = "maintenance"  # 정비중
    UNAVAILABLE = "unavailable"  # 사용불가


class Vehicle(Base):
    """Vehicle master table - 차량 마스터"""
    __tablename__ = "vehicles"
    
    # Primary Key
    vehicle_id = Column(String(50), primary_key=True, index=True, comment="차량 코드 (예: TRUCK-001)")
    
    # UVIS Integration
    uvis_device_id = Column(String(100), unique=True, nullable=True, index=True, comment="UVIS 단말기 ID")
    
    # Vehicle Specifications
    vehicle_type = Column(SQLEnum(VehicleType), nullable=False, comment="차량 타입")
    truck_tonnage = Column(Float, nullable=False, comment="차량 톤수")
    max_pallets = Column(Integer, nullable=False, comment="최대 적재 팔레트 수")
    max_weight_kg = Column(Float, nullable=False, comment="최대 적재 중량 (kg)")
    
    # Temperature Specifications
    temperature_range_min = Column(Float, nullable=False, comment="최저 온도 (°C)")
    temperature_range_max = Column(Float, nullable=False, comment="최고 온도 (°C)")
    multi_chamber = Column(Boolean, default=False, comment="겸용차량 여부 (냉동/냉장 구획 분리)")
    
    # Vehicle Information
    license_plate = Column(String(20), unique=True, nullable=True, comment="차량 번호판")
    manufacturer = Column(String(50), nullable=True, comment="제조사")
    model = Column(String(50), nullable=True, comment="모델명")
    year = Column(Integer, nullable=True, comment="연식")
    
    # Driver Information
    driver_name = Column(String(100), nullable=True, comment="기사 이름")
    driver_phone = Column(String(20), nullable=True, comment="기사 연락처")
    
    # Operational Status
    current_status = Column(SQLEnum(VehicleStatus), default=VehicleStatus.AVAILABLE, comment="현재 상태")
    current_pallets = Column(Integer, default=0, comment="현재 적재 팔레트 수")
    current_weight_kg = Column(Float, default=0.0, comment="현재 적재 중량")
    
    # Location (last known)
    last_latitude = Column(Float, nullable=True, comment="마지막 위도")
    last_longitude = Column(Float, nullable=True, comment="마지막 경도")
    last_location_update = Column(DateTime, nullable=True, comment="마지막 위치 업데이트 시간")
    
    # Operational Constraints
    work_start_time = Column(String(5), default="06:00", comment="근무 시작 시간 (HH:MM)")
    work_end_time = Column(String(5), default="20:00", comment="근무 종료 시간 (HH:MM)")
    max_driving_hours = Column(Integer, default=10, comment="최대 운행 시간")
    
    # Garage Location
    garage_address = Column(String(500), nullable=True, comment="차고지 주소")
    garage_latitude = Column(Float, nullable=True, comment="차고지 위도")
    garage_longitude = Column(Float, nullable=True, comment="차고지 경도")
    
    # Metadata
    is_active = Column(Boolean, default=True, comment="활성 상태")
    notes = Column(String(1000), nullable=True, comment="비고")
    created_at = Column(DateTime, server_default=func.now(), comment="생성일시")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="수정일시")
    
    def __repr__(self):
        return f"<Vehicle {self.vehicle_id} ({self.vehicle_type.value}) - {self.current_status.value}>"
