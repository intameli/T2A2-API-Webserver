from init import db, ma
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String


class Court(db.Model):
    __tablename__ = "courts"
    id: Mapped[int] = mapped_column(primary_key=True)
    surface: Mapped[str] = mapped_column(String(10))


class CourtSchema(ma.Schema):
    class Meta:
        fields = ("id", "surface")
