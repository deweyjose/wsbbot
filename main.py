import os

import controller
from core.application import app
from core.database import db
from core.schemas import ma

app.config.from_object(os.getenv('APP_SETTINGS', 'core.config.DevelopmentConfig'))
db.init_app(app)
ma.init_app(app)
controller.init_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
