"""Seed file for auth_db"""

from models import User, Feedback, db
from app import app

"""Create all tables"""
db.drop_all()
db.create_all()
