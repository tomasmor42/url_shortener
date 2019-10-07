from . import db

class Urls(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    short_url = db.Column(
        db.String(20), unique=True, nullable=False)
    full_url = db.Column(
        db.String(500), unique=False, nullable=False)
    created = db.Column(db.DateTime, nullable=False)
    last_used = db.Column(db.DateTime, nullable=True, default=None)
    counts = db.Column(db.Integer, default=0)
