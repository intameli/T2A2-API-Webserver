from init import db, ma
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer
from typing import List
from datetime import datetime
from sqlalchemy.ext.associationproxy import association_proxy
# from marshmallow.validate import Length

from typing import Optional
from sqlalchemy import ForeignKey
from marshmallow import fields


class Match(db.Model):
    __tablename__ = "matches"
    id: Mapped[int] = mapped_column(primary_key=True)
    time: Mapped[datetime]

    court_id: Mapped[int] = mapped_column(ForeignKey("courts.id"))
    court: Mapped['Court'] = relationship()

    results: Mapped[List["Match_Player"]] = relationship(cascade='all, delete')

    players_ass: Mapped[List["Match_Player"]] = relationship(
        back_populates="match", cascade="all, delete", viewonly=True)
    players: Mapped[List["Player"]] = association_proxy(
        "players_ass", "player")


class MatchSchema(ma.Schema):
    players = fields.Nested("PlayerSchema", many=True, exclude=("matches",))
    court = fields.Nested("CourtSchema")
    results = fields.Nested(
        "Match_PlayerSchema", many=True)

    class Meta:
        fields = ("id", "time", "court", "players",
                  "results", 'court_id')


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