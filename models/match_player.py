from init import db, ma
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer
from typing import List
from datetime import datetime
# from marshmallow import fields
# from marshmallow.validate import Length

from typing import Optional
from sqlalchemy import ForeignKey


class Match_Player(db.Model):
    __tablename__ = "match_player_join"
    match_id: Mapped[int] = mapped_column(
        ForeignKey("matches.id"), primary_key=True)
    player_id: Mapped[int] = mapped_column(
        ForeignKey("players.id"), primary_key=True
    )
    result: Mapped[Optional[str]] = mapped_column(String(10))
    games_won: Mapped[Optional[int]] = mapped_column(Integer)
    tie_break: Mapped[Optional[int]] = mapped_column(Integer)

    player: Mapped["Player"] = relationship(
        back_populates="matches_ass")
    match: Mapped["Match"] = relationship(
        back_populates="players_ass", overlaps="results")


class Match_PlayerSchema(ma.Schema):
    # players = fields.Nested("PlayerSchema", many=True, exclude=("matches",))
    # court = fields.Nested("CourtSchema")

    class Meta:
        fields = ('result', 'player_id', 'games_won', 'tie_break')


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
