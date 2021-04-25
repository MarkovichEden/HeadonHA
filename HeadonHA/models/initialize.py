from api import db

import models

db.drop_all()
db.create_all()
