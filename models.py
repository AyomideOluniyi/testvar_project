from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# Model representing a flashcard set (a collection of flashcards, comments, and reviews)
class FlashcardSet(db.Model):
    __tablename__ = 'flashcard_sets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    flashcards = db.relationship('Flashcard', backref='flashcard_set', lazy=True)
    comments = db.relationship('Comment', backref='flashcard_set', lazy=True)
    reviews = db.relationship('Review', backref='flashcard_set', lazy=True)

# Model representing an individual flashcard with question, answer, and a hidden flag
class Flashcard(db.Model):
    __tablename__ = 'flashcards'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200), nullable=False)
    answer = db.Column(db.String(200), nullable=False)
    set_id = db.Column(db.Integer, db.ForeignKey('flashcard_sets.id'), nullable=False)
    hidden = db.Column(db.Boolean, default=False)

# Model representing a comment made on a flashcard set
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(50), nullable=True)
    set_id = db.Column(db.Integer, db.ForeignKey('flashcard_sets.id'), nullable=False)

# Model representing a review for a flashcard set including a rating and optional review text
class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    review_text = db.Column(db.String(500), nullable=True)
    author = db.Column(db.String(50), nullable=True)
    set_id = db.Column(db.Integer, db.ForeignKey('flashcard_sets.id'), nullable=False)

# Model for recording telemetry events (e.g., when a flashcard answer is shown)
class Telemetry(db.Model):
    __tablename__ = 'telemetry'
    id = db.Column(db.Integer, primary_key=True)
    flashcard_set_id = db.Column(db.Integer, db.ForeignKey('flashcard_sets.id'), nullable=False)
    flashcard_id = db.Column(db.Integer, db.ForeignKey('flashcards.id'), nullable=True)
    event = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    duration = db.Column(db.Float, nullable=True)
