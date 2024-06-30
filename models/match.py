from init import db, ma
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from datetime import datetime
from sqlalchemy.ext.associationproxy import association_proxy
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
    players = fields.Nested("PlayerSchema", many=True,
                            exclude=("matches", "email", "password", "admin"))
    court = fields.Nested("CourtSchema")
    results = fields.Nested(
        "Match_PlayerSchema", many=True)

    class Meta:
        fields = ("id", "time", "court", "players",
                  "results", 'court_id')
