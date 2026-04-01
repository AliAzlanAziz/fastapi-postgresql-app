from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Integer
from app.db import Base

class Education(Base):
    __tablename__ = "educations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    degree: Mapped[str] = mapped_column(String(100), nullable=False)
    field: Mapped[str] = mapped_column(String(150), nullable=False)
    institute: Mapped[str] = mapped_column(String(200), nullable=False)

    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    user: Mapped["User"] = relationship(back_populates="educations")
