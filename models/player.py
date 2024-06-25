from init import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
# from typing import Optional, List
# from marshmallow import fields
# from marshmallow.validate import Length


class Player(db.Model):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
