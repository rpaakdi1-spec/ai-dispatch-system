from sqlalchemy import Column, String, Float, Integer, DateTime, Boolean, Text
from sqlalchemy.sql import func
from datetime import datetime
from config.database import Base


class GPSLog(Base):
    """GPS tracking log from UVIS system"""
    __tablename__ = "gps_logs"
    
    # Primary Key
    id = Column(Integer, primary_key=True, autoincrement=True, comment="로그 ID")
    
    # Vehicle Reference
    vehicle_id = Column(String(50), nullable=False, index=True, comment="차량 코드")
    uvis_device_id = Column(String(100), nullable=True, index=True, comment="UVIS 단말기 ID")
    
    # Timestamp
    timestamp = Column(DateTime, nullable=False, index=True, comment="GPS 측정 시간")
    received_at = Column(DateTime, server_default=func.now(), comment="서버 수신 시간")
    
    # Location
    latitude = Column(Float, nullable=False, comment="위도")
    longitude = Column(Float, nullable=False, comment="경도")
    altitude = Column(Float, nullable=True, comment="고도 (m)")
    accuracy = Column(Float, nullable=True, comment="정확도 (m)")
    
    # Speed and Direction
    speed_kmh = Column(Float, nullable=True, comment="속도 (km/h)")
    heading = Column(Float, nullable=True, comment="방향 (0-360도)")
    
    # Temperature Monitoring
    compartment1_temp = Column(Float, nullable=True, comment="적재함1 온도 (°C)")
    compartment2_temp = Column(Float, nullable=True, comment="적재함2 온도 (°C)")
    setpoint_temp = Column(Float, nullable=True, comment="설정 온도 (°C)")
    temp_alarm = Column(Boolean, default=False, comment="온도 경보")
    
    # Vehicle Status
    engine_on = Column(Boolean, nullable=True, comment="엔진 ON/OFF")
    door_open = Column(Boolean, nullable=True, comment="문 열림/닫힘")
    refrigerator_on = Column(Boolean, nullable=True, comment="냉동기 ON/OFF")
    
    # Odometer
    odometer_km = Column(Float, nullable=True, comment="누적 주행거리 (km)")
    trip_distance_km = Column(Float, nullable=True, comment="구간 주행거리 (km)")
    
    # Address (reverse geocoding)
    address = Column(String(500), nullable=True, comment="주소 (역지오코딩)")
    
    # Event Detection
    is_stopped = Column(Boolean, default=False, comment="정차 여부")
    stop_duration_minutes = Column(Integer, default=0, comment="정차 시간 (분)")
    is_idling = Column(Boolean, default=False, comment="공회전 여부")
    
    # Route Deviation
    is_off_route = Column(Boolean, default=False, comment="경로 이탈 여부")
    route_deviation_km = Column(Float, nullable=True, comment="경로 이탈 거리 (km)")
    
    # Battery and Signal
    battery_voltage = Column(Float, nullable=True, comment="배터리 전압 (V)")
    signal_strength = Column(Integer, nullable=True, comment="신호 강도 (0-100)")
    
    # Additional Data
    raw_data = Column(Text, nullable=True, comment="원본 데이터 (JSON)")
    
    # Metadata
    created_at = Column(DateTime, server_default=func.now(), comment="생성일시")
    
    def __repr__(self):
        return f"<GPSLog {self.vehicle_id} at {self.timestamp} ({self.latitude}, {self.longitude})>"


class GPSEvent(Base):
    """GPS event detection log"""
    __tablename__ = "gps_events"
    
    # Primary Key
    id = Column(Integer, primary_key=True, autoincrement=True, comment="이벤트 ID")
    
    # Vehicle Reference
    vehicle_id = Column(String(50), nullable=False, index=True, comment="차량 코드")
    
    # Event Information
    event_type = Column(String(50), nullable=False, index=True, comment="이벤트 유형")
    event_time = Column(DateTime, nullable=False, index=True, comment="이벤트 발생 시간")
    event_description = Column(String(500), nullable=True, comment="이벤트 설명")
    
    # Location
    latitude = Column(Float, nullable=True, comment="위도")
    longitude = Column(Float, nullable=True, comment="경도")
    address = Column(String(500), nullable=True, comment="주소")
    
    # Severity
    severity = Column(String(20), default="info", comment="심각도 (info/warning/critical)")
    
    # Related Order
    order_id = Column(String(50), nullable=True, index=True, comment="관련 주문 번호")
    
    # Resolution
    is_resolved = Column(Boolean, default=False, comment="처리 완료 여부")
    resolved_at = Column(DateTime, nullable=True, comment="처리 완료 시간")
    resolution_note = Column(String(500), nullable=True, comment="처리 메모")
    
    # Metadata
    created_at = Column(DateTime, server_default=func.now(), comment="생성일시")
    
    def __repr__(self):
        return f"<GPSEvent {self.event_type} - {self.vehicle_id} at {self.event_time}>"
