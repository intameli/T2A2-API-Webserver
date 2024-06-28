from init import db, ma
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer
from typing import List
from datetime import datetime
from marshmallow import fields
# from marshmallow.validate import Length
from sqlalchemy.ext.associationproxy import association_proxy
from typing import Optional
from sqlalchemy import ForeignKey


class Court(db.Model):
    __tablename__ = "courts"
    id: Mapped[int] = mapped_column(primary_key=True)
    surface: Mapped[str] = mapped_column(String(10))

    # match_id: Mapped[int] = mapped_column(ForeignKey("matches.id"))
    # matches_ass: Mapped[List["Match_Player"]] = relationship(
    #     back_populates="player")
    # matches: Mapped[List["Match"]] = association_proxy(
    #     "matches_ass", "match")


class CourtSchema(ma.Schema):
    # matches = fields.Nested('MatchSchema', many=True, exclude=("players",))

    class Meta:
        fields = ("id", "surface")
