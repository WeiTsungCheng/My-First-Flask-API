from app import app
from db import db

db.init_app(app)
print('0001')
@app.before_first_request
def create_tables():
    print('0002')
    db.create_all()
