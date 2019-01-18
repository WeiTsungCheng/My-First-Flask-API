from app import app
from db import db

db.init_app(app)
print('0002')
@app.before_first_request
def create_tables():
    print('0001')
    db.create_all()
