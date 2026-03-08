# app/db/base.py
#
# This module defines the SQLAlchemy declarative base.
# Every database model in the project will inherit from `Base`
# so SQLAlchemy knows about the table and can create/query it.

from sqlalchemy.orm import declarative_base

# Base is the parent class for all ORM models.
# When a model inherits from Base, SQLAlchemy registers it
# and maps it to a database table automatically.
Base = declarative_base()
