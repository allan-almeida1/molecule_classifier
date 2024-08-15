import os


class Config:
    """Set Flask configuration vars from .env file."""
    SECRET_KEY = os.getenv('SECRET_KEY') or 'somethingsecret'
