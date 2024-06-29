from init import db, ma
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Boolean
from typing import List
from datetime import datetime
from marshmallow import fields
from marshmallow.validate import Length
from sqlalchemy.ext.associationproxy import association_proxy
from typing import Optional
from sqlalchemy import ForeignKey


class Player(db.Model):
    __tablename__ = "players"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(200), unique=True)
    password: Mapped[str] = mapped_column(String(200))
    admin: Mapped[bool] = mapped_column(Boolean(), server_default="false")

    matches_ass: Mapped[List["Match_Player"]] = relationship(
        back_populates="player")
    matches: Mapped[List["Match"]] = association_proxy(
        "matches_ass", "match")


class PlayerSchema(ma.Schema):
    matches = fields.Nested('MatchSchema', many=True, exclude=("players",))
    email = fields.Email(required=True)
    password = fields.String(validate=Length(
        min=6, error='Password must be at least 8 characters long'), required=True)

    class Meta:
        fields = ("id", "name", "matches", "email", "password", "admin")
