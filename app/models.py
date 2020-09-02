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

def populate_db():
    if len(Word.query.all()) == 0:
        word_list = [
            'lyuk', 'hely', 'folyik', 'boly', 'robaj', 'olaj', 'karaj',
            'duhaj', 'tolvaj', 'ibolya', 'ajtó', 'papagáj', 'vaj',
            'gereblye', 'talaj', 'moly', 'zsindely', 'bagoly', 'fejes',
            'sajt', 'kehely', 'tutaj', 'bojler', 'gólya', 'golyó'
        ]

        for w in word_list:
            word_obj = Word(value=w)

            db.session.add(word_obj)
        db.session.commit()

        return True
    else:
        return False
