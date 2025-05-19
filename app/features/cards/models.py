from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, String, UUID, func
from app.core.database import Base
import uuid

class CardModel(Base):
    __tablename__ = "cards"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    creator_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    number: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, autoincrement=True, default=1)
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(255), nullable=False, default="Membre") # Membre, Coordinateur, Sécrétaire, Président, ...
    contact: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    image_url: Mapped[str] = mapped_column(String(255), nullable=True)
    qr_code_url: Mapped[str] = mapped_column(String(), nullable=True)
    department_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("departments.id"), nullable=False)
    municipality_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("municipalities.id"), nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), default=func.now())

    creator = relationship("UserModel", back_populates="cards", lazy="joined")
    department = relationship("DepartmentModel", back_populates="cards", lazy="joined")
    municipality = relationship("MunicipalityModel", back_populates="cards", lazy="joined")
    