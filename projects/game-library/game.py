from sqlalchemy import CheckConstraint, String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Game(Base):
    __tablename__ = "games"

    __table_args__ = (
        CheckConstraint(
            "rating BETWEEN 1 AND 10",
            name="check_rating",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    release_date: Mapped[str] = mapped_column(String(10), nullable=False)
    rating: Mapped[int] = mapped_column(nullable=False)

    def __str__(self) -> str:
        return (
            f"{self.name} ({self.release_date}) "
            f"- Rating: {self.rating}/10"
        )