from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime, Enum as SQLEnum, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum
from config.database import Base


class TemperatureType(str, Enum):
    """Temperature requirement type"""
    FROZEN = "frozen"  # 냉동 (-18°C ~ -25°C)
    CHILLED = "chilled"  # 냉장 (0°C ~ 6°C)
    AMBIENT = "ambient"  # 상온


class OrderPriority(str, Enum):
    """Order priority level"""
    URGENT = "urgent"  # 긴급
    HIGH = "high"  # 높음
    NORMAL = "normal"  # 보통
    LOW = "low"  # 낮음


class OrderStatus(str, Enum):
    """Order processing status"""
    PENDING = "pending"  # 대기중
    ASSIGNED = "assigned"  # 배차됨
    IN_TRANSIT = "in_transit"  # 운송중
    LOADING = "loading"  # 상차중
    LOADED = "loaded"  # 상차완료
    UNLOADING = "unloading"  # 하차중
    COMPLETED = "completed"  # 완료
    CANCELLED = "cancelled"  # 취소됨
    FAILED = "failed"  # 실패


class Order(Base):
    """Order table - 주문"""
    __tablename__ = "orders"
    
    # Primary Key
    order_id = Column(String(50), primary_key=True, index=True, comment="주문 번호")
    
    # Client References
    pickup_client_id = Column(String(50), nullable=False, index=True, comment="상차 거래처 코드")
    delivery_client_id = Column(String(50), nullable=False, index=True, comment="하차 거래처 코드")
    
    # Order Date
    order_date = Column(DateTime, nullable=False, index=True, comment="주문 일자")
    
    # Temperature and Cargo Information
    temperature_type = Column(SQLEnum(TemperatureType), nullable=False, comment="온도대 구분")
    required_pallets = Column(Integer, nullable=False, comment="필요 팔레트 수")
    weight_kg = Column(Float, nullable=False, comment="중량 (kg)")
    volume_cbm = Column(Float, nullable=True, comment="부피 (CBM)")
    
    # Cargo Details
    cargo_description = Column(String(500), nullable=True, comment="화물 설명")
    cargo_category = Column(String(100), nullable=True, comment="화물 분류")
    is_stackable = Column(Boolean, default=True, comment="적재 가능 여부")
    is_fragile = Column(Boolean, default=False, comment="깨지기 쉬운 화물")
    requires_special_handling = Column(Boolean, default=False, comment="특별 취급 필요")
    
    # Time Windows
    pickup_time_start = Column(String(5), nullable=False, comment="상차 시작 시간 (HH:MM)")
    pickup_time_end = Column(String(5), nullable=False, comment="상차 종료 시간 (HH:MM)")
    delivery_time_start = Column(String(5), nullable=False, comment="하차 시작 시간 (HH:MM)")
    delivery_time_end = Column(String(5), nullable=False, comment="하차 종료 시간 (HH:MM)")
    
    # Priority and Status
    priority = Column(SQLEnum(OrderPriority), default=OrderPriority.NORMAL, comment="우선순위")
    status = Column(SQLEnum(OrderStatus), default=OrderStatus.PENDING, index=True, comment="처리 상태")
    
    # Assignment Information
    assigned_vehicle_id = Column(String(50), nullable=True, index=True, comment="배차된 차량 ID")
    assigned_at = Column(DateTime, nullable=True, comment="배차 일시")
    dispatch_sequence = Column(Integer, nullable=True, comment="배차 순서")
    
    # Estimated Times (from OR-Tools)
    estimated_pickup_time = Column(DateTime, nullable=True, comment="예상 상차 시간")
    estimated_delivery_time = Column(DateTime, nullable=True, comment="예상 하차 시간")
    estimated_distance_km = Column(Float, nullable=True, comment="예상 거리 (km)")
    estimated_duration_minutes = Column(Integer, nullable=True, comment="예상 소요 시간 (분)")
    
    # Actual Times (from GPS tracking)
    actual_pickup_start = Column(DateTime, nullable=True, comment="실제 상차 시작")
    actual_pickup_end = Column(DateTime, nullable=True, comment="실제 상차 종료")
    actual_delivery_start = Column(DateTime, nullable=True, comment="실제 하차 시작")
    actual_delivery_end = Column(DateTime, nullable=True, comment="실제 하차 종료")
    actual_distance_km = Column(Float, nullable=True, comment="실제 거리 (km)")
    
    # Customer Information
    customer_name = Column(String(100), nullable=True, comment="고객명")
    customer_phone = Column(String(20), nullable=True, comment="고객 연락처")
    customer_email = Column(String(100), nullable=True, comment="고객 이메일")
    
    # Special Requirements
    special_instructions = Column(Text, nullable=True, comment="특별 지시사항")
    delivery_instructions = Column(String(500), nullable=True, comment="배송 지시사항")
    
    # Documents
    requires_signature = Column(Boolean, default=True, comment="서명 필요 여부")
    requires_photo = Column(Boolean, default=False, comment="사진 촬영 필요")
    signature_url = Column(String(500), nullable=True, comment="서명 이미지 URL")
    photo_url = Column(String(500), nullable=True, comment="배송 사진 URL")
    
    # Pricing (optional)
    freight_charge = Column(Float, nullable=True, comment="운송비")
    additional_charges = Column(Float, nullable=True, comment="추가 비용")
    total_charge = Column(Float, nullable=True, comment="총 비용")
    
    # Cancellation
    cancelled_at = Column(DateTime, nullable=True, comment="취소 일시")
    cancellation_reason = Column(String(500), nullable=True, comment="취소 사유")
    
    # Failure
    failure_reason = Column(String(500), nullable=True, comment="실패 사유")
    
    # Metadata
    notes = Column(Text, nullable=True, comment="비고")
    created_at = Column(DateTime, server_default=func.now(), comment="생성일시")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="수정일시")
    
    def __repr__(self):
        return f"<Order {self.order_id} - {self.temperature_type.value} - {self.status.value}>"
