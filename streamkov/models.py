# -*- coding: utf-8 -*-
"""
    models
    ~~~~~~

    SQLAlchemy models for streamkov app
"""

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from streamkov import CONNECTION_STRING


engine = sa.engine.create_engine(CONNECTION_STRING)
metadata = sa.MetaData(bind=engine)
Base = declarative_base(metadata)


class Chain(Base):
    __tablename__ = 'chains'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.Text)
    state = sa.Column(JSONB)
    sources = sa.Column(JSONB)

Base.metadata.create_all(engine)

session = sessionmaker(bind=engine)()
