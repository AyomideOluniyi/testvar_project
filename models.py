from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class FlashcardSet(db.Model):
    __tablename__ = 'flashcard_sets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    flashcards = db.relationship('Flashcard', backref='flashcard_set', lazy=True)
    comments = db.relationship('Comment', backref='flashcard_set', lazy=True)
    reviews = db.relationship('Review', backref='flashcard_set', lazy=True)

class Flashcard(db.Model):
    __tablename__ = 'flashcards'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200), nullable=False)
    answer = db.Column(db.String(200), nullable=False)
    set_id = db.Column(db.Integer, db.ForeignKey('flashcard_sets.id'), nullable=False)
    hidden = db.Column(db.Boolean, default=False)

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(50), nullable=True)
    set_id = db.Column(db.Integer, db.ForeignKey('flashcard_sets.id'), nullable=False)

class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)  
    review_text = db.Column(db.String(500), nullable=True)
    author = db.Column(db.String(50), nullable=True)
    set_id = db.Column(db.Integer, db.ForeignKey('flashcard_sets.id'), nullable=False)

class Telemetry(db.Model):
    __tablename__ = 'telemetry'
    id = db.Column(db.Integer, primary_key=True)
    flashcard_set_id = db.Column(db.Integer, db.ForeignKey('flashcard_sets.id'), nullable=False)
    flashcard_id = db.Column(db.Integer, db.ForeignKey('flashcards.id'), nullable=True)
    event = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    duration = db.Column(db.Float, nullable=True) 