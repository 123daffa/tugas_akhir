from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

# Dipisah ke file sendiri (bukan di app/__init__.py) supaya model-model di
# app/models/*.py bisa `from extensions import db` tanpa circular import
# dengan create_app().

db = SQLAlchemy()
jwt = JWTManager()