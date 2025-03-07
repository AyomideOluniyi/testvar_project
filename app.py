from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db, FlashcardSet, Flashcard  

# Create the Flask application instance
app = Flask(__name__)

# configure databese
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testvar.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['DAILY_LIMIT'] = 20 

# Initialize SQLAlchemy
db.init_app(app)

# Create all database tables (if they don't exist already)
with app.app_context():
    db.create_all()


#route to Render the homepage of the application
@app.route('/')
def home():
    return render_template('index.html')

# route to list all flashcard sets in the system
@app.route('/sets')
def list_sets():
    sets = FlashcardSet.query.all()
    return render_template('sets.html', sets=sets)


# route to provide a form to create a new flashcard set (GET) and process the form submission (POST)
@app.route('/sets/new', methods=['GET', 'POST'])
def new_set():
    if request.method == 'POST':
        name = request.form.get('name')
        if name:
            from datetime import date
            today = date.today()
            # Count the number of sets created today
            count_today = FlashcardSet.query.filter(FlashcardSet.created_at >= today).count()
            if count_today >= app.config['DAILY_LIMIT']:
                return "Daily limit reached! Try again tomorrow."
            # Create and save the new flashcard set
            new_set = FlashcardSet(name=name)
            db.session.add(new_set)
            db.session.commit()
            return redirect(url_for('list_sets'))
    return render_template('new_set.html')

# route to display details of a single flashcard set, including its flashcards, comments, and reviews
@app.route('/sets/<int:set_id>')
def set_detail(set_id):
    flashcard_set = FlashcardSet.query.get_or_404(set_id)
    return render_template('set_detail.html', flashcard_set=flashcard_set)


# route to Provide a JSON representation of all flashcard sets
@app.route('/api/sets', methods=['GET'])
def api_list_sets():
    sets = FlashcardSet.query.all()
    sets_data = []
    for s in sets:
        sets_data.append({
            'id': s.id,
            'name': s.name,
            'created_at': s.created_at.isoformat()
        })
    return jsonify(sets_data)

# route to Provide a form to add a new flashcard to a set (GET) and process the submission (POST) Also handles the "hidden" flag for flashcards.
@app.route('/sets/<int:set_id>/cards/new', methods=['GET', 'POST'])
def new_card(set_id):
    flashcard_set = FlashcardSet.query.get_or_404(set_id)
    
    if request.method == 'POST':
        question = request.form.get('question')
        answer = request.form.get('answer')
        hidden_value = request.form.get('hidden')
        hidden = True if hidden_value == 'on' else False
        
        if question and answer:
            new_card = Flashcard(question=question, answer=answer, set_id=set_id, hidden=hidden)
            db.session.add(new_card)
            db.session.commit()
            return redirect(url_for('set_detail', set_id=set_id))
    
    return render_template('new_card.html', flashcard_set=flashcard_set)

# Import additional models for comments, reviews, and telemetry
from models import db, FlashcardSet, Flashcard, Comment, Review, Telemetry

# route to allow users to add a comment to a flashcard set.
@app.route('/sets/<int:set_id>/comment', methods=['GET', 'POST'])
def add_comment(set_id):
    flashcard_set = FlashcardSet.query.get_or_404(set_id)
    if request.method == 'POST':
        comment_text = request.form.get('comment')
        author = request.form.get('author')  # Optional author field
        if comment_text:
            new_comment = Comment(comment=comment_text, author=author, set_id=set_id)
            db.session.add(new_comment)
            db.session.commit()
            return redirect(url_for('set_detail', set_id=set_id))
    return render_template('add_comment.html', flashcard_set=flashcard_set)


# route to allow users to add a review (with rating) to a flashcard set.
@app.route('/sets/<int:set_id>/review', methods=['GET', 'POST'])
def add_review(set_id):
    flashcard_set = FlashcardSet.query.get_or_404(set_id)
    if request.method == 'POST':
        try:
            rating = int(request.form.get('rating'))
        except (TypeError, ValueError):
            rating = 0
        review_text = request.form.get('review_text')
        author = request.form.get('author')
        # Validate that the rating is between 1 and 5
        if rating < 1 or rating > 5:
            return "Rating must be between 1 and 5.", 400
        new_review = Review(rating=rating, review_text=review_text, author=author, set_id=set_id)
        db.session.add(new_review)
        db.session.commit()
        return redirect(url_for('set_detail', set_id=set_id))
    return render_template('add_review.html', flashcard_set=flashcard_set)


# route to record telemetry data when users interact with flashcards (e.g., show answer events).
@app.route('/telemetry', methods=['POST'])
def telemetry():
    data = request.get_json()
    if not data or 'flashcard_set_id' not in data or 'event' not in data:
        return jsonify({'error': 'Invalid data'}), 400

    telemetry_entry = Telemetry(
        flashcard_set_id=data.get('flashcard_set_id'),
        flashcard_id=data.get('flashcard_id'),
        event=data.get('event'),
        duration=data.get('duration')
    )
    db.session.add(telemetry_entry)
    db.session.commit()
    return jsonify({'message': 'Telemetry data recorded'}), 200

# route to allow an admin to view or update the daily limit for flashcard set creation.
@app.route('/admin/daily_limit', methods=['GET', 'POST'])
def admin_daily_limit():
    if request.method == 'POST':
        try:
            new_limit = int(request.form.get('daily_limit'))
            app.config['DAILY_LIMIT'] = new_limit
            return redirect(url_for('list_sets'))
        except (TypeError, ValueError):
            return "Invalid limit", 400
    return render_template('admin_daily_limit.html')


# route to return the current API version as JSON.
@app.route('/api/version', methods=['GET'])
def api_version():
    return jsonify({"version": "1.0.0"})

# route to Delete a flashcard set by its ID. returns a 204 status if deletion is successful, or 404 if not found.
@app.route('/sets/<int:set_id>', methods=['DELETE'])
def delete_set(set_id):
    flashcard_set = FlashcardSet.query.get(set_id)
    if not flashcard_set:
        return jsonify({"message": "Flashcard set not found"}), 404
    db.session.delete(flashcard_set)
    db.session.commit()
    return '', 204

# run the Flask application in debug mode if this file is executed directly
if __name__ == '__main__':
    app.run(debug=True)
