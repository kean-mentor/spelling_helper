from datetime import datetime

from app import db


class Word(db.Model):
    word_id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(64), nullable=False)

    db.UniqueConstraint(value)

    def __str__(self):
        return self.value


class Score(db.Model):
    score_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    percent = db.Column(db.Float, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    db.UniqueConstraint(username, created)

    def __str__(self):
        return f"{self.created} - {self.username} - {self.score}"
