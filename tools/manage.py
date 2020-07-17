import os

from flask import Flask
from flask_migrate import Migrate

from core.database import db

app = Flask('WSBBOT Migrations')
app.config.from_object(os.getenv('APP_SETTINGS', 'core.config.DevelopmentConfig'))
db.init_app(app)

migrate = Migrate(app, db)

