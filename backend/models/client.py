from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime, Enum as SQLEnum
from sqlalchemy.sql import func
from datetime import datetime
from enum import Enum
from config.database import Base


class ServiceType(str, Enum):
    """Client service type"""
    PICKUP = "pickup"  # 상차만
    DELIVERY = "delivery"  # 하차만
    BOTH = "both"  # 상차/하차 모두


class Client(Base):
    """Client master table - 거래처 마스터"""
    __tablename__ = "clients"
    
    # Primary Key
    client_id = Column(String(50), primary_key=True, index=True, comment="거래처 코드 (예: CUST-0001)")
    
    # Basic Information
    client_name = Column(String(200), nullable=False, index=True, comment="거래처명")
    business_registration_number = Column(String(20), unique=True, nullable=True, comment="사업자등록번호")
    service_type = Column(SQLEnum(ServiceType), nullable=False, comment="서비스 구분 (상차/하차/양쪽)")
    
    # Contact Information
    contact_person = Column(String(100), nullable=True, comment="담당자명")
    contact_phone = Column(String(20), nullable=True, comment="연락처")
    contact_email = Column(String(100), nullable=True, comment="이메일")
    
    # Address Information
    address = Column(String(500), nullable=False, comment="주소")
    address_detail = Column(String(200), nullable=True, comment="상세주소")
    postal_code = Column(String(10), nullable=True, comment="우편번호")
    
    # Geocoding (Naver Maps API)
    latitude = Column(Float, nullable=True, index=True, comment="위도")
    longitude = Column(Float, nullable=True, index=True, comment="경도")
    geocoding_status = Column(String(20), default="pending", comment="지오코딩 상태 (pending/success/failed)")
    geocoding_error = Column(String(500), nullable=True, comment="지오코딩 오류 메시지")
    manual_coordinates = Column(Boolean, default=False, comment="수동 좌표 입력 여부")
    
    # Operational Time Windows
    pickup_time_start = Column(String(5), nullable=True, comment="상차 가능 시작 시간 (HH:MM)")
    pickup_time_end = Column(String(5), nullable=True, comment="상차 가능 종료 시간 (HH:MM)")
    delivery_time_start = Column(String(5), nullable=True, comment="하차 가능 시작 시간 (HH:MM)")
    delivery_time_end = Column(String(5), nullable=True, comment="하차 가능 종료 시간 (HH:MM)")
    
    # Facility Information
    has_forklift = Column(Boolean, default=False, comment="지게차 보유 여부")
    has_loading_dock = Column(Boolean, default=False, comment="상하차장 보유 여부")
    allows_large_truck = Column(Boolean, default=True, comment="대형 차량 진입 가능 여부")
    allows_night_delivery = Column(Boolean, default=False, comment="야간 배송 가능 여부")
    
    # Loading/Unloading Time
    avg_loading_time_minutes = Column(Integer, default=30, comment="평균 상차 시간 (분)")
    avg_unloading_time_minutes = Column(Integer, default=30, comment="평균 하차 시간 (분)")
    
    # Operational Constraints
    requires_appointment = Column(Boolean, default=False, comment="사전 예약 필수 여부")
    appointment_notice_hours = Column(Integer, default=24, comment="예약 통보 시간 (시간 단위)")
    max_pallets_per_visit = Column(Integer, nullable=True, comment="1회 방문당 최대 팔레트 수")
    
    # Special Notes
    access_restrictions = Column(String(500), nullable=True, comment="접근 제한 사항")
    parking_notes = Column(String(500), nullable=True, comment="주차 관련 메모")
    special_instructions = Column(String(1000), nullable=True, comment="특별 지시사항")
    
    # Credit and Business
    credit_rating = Column(String(10), nullable=True, comment="신용등급")
    payment_terms = Column(String(50), nullable=True, comment="결제 조건")
    
    # Metadata
    is_active = Column(Boolean, default=True, comment="활성 상태")
    notes = Column(String(1000), nullable=True, comment="비고")
    created_at = Column(DateTime, server_default=func.now(), comment="생성일시")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="수정일시")
    
    def __repr__(self):
        return f"<Client {self.client_id} - {self.client_name} ({self.service_type.value})>"
