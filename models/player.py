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


class Player(db.Model):
    __tablename__ = "players"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))

    matches_ass: Mapped[List["Match_Player"]] = relationship(
        back_populates="player")
    matches: Mapped[List["Match"]] = association_proxy(
        "matches_ass", "match")


class PlayerSchema(ma.Schema):
    matches = fields.Nested('MatchSchema', many=True, exclude=("players",))

    class Meta:
        fields = ("id", "name", "matches")

    # class Player(db.Model):
    #     __tablename__ = "players"

    #     id: Mapped[int] = mapped_column(primary_key=True)
    #     name: Mapped[str] = mapped_column(String(100))
    #     age: Mapped[int] = mapped_column(Integer())

    #     matches: Mapped[List['Match_Player']] = relationship(
    #         back_populates='matches')

    # class PlayerSchema(ma.Schema):
    #     class Meta:
    #         fields = ['id', 'name', 'age']
