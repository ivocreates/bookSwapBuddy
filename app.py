from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import os
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'

# Database configuration with absolute path
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "instance", "bookswap.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file upload

db = SQLAlchemy(app)

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Helper function for file uploads
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Admin required decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        
        user = User.query.get(session['user_id'])
        if not user or not user.is_admin:
            flash('Admin access required.', 'error')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    college = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    hostel = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    points = db.Column(db.Integer, default=0)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    books = db.relationship('Book', backref='owner', lazy=True)
    sent_messages = db.relationship('Message', foreign_keys='Message.sender_id', backref='sender', lazy=True)
    received_messages = db.relationship('Message', foreign_keys='Message.receiver_id', backref='receiver', lazy=True)
    wishlist_items = db.relationship('Wishlist', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    year_of_study = db.Column(db.Integer, nullable=False)
    condition = db.Column(db.String(50), nullable=False)
    swap_type = db.Column(db.String(20), nullable=False)  # sell, swap, free
    price = db.Column(db.Float, nullable=True)
    description = db.Column(db.Text, nullable=True)
    isbn = db.Column(db.String(20), nullable=True)
    language = db.Column(db.String(50), default='English')
    preferred_books = db.Column(db.String(200), nullable=True)
    contact_method = db.Column(db.String(20), default='message')
    contact_info = db.Column(db.String(100), nullable=True)
    image_filename = db.Column(db.String(100), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), default='available')  # available, sold, reserved
    views = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    book = db.relationship('Book', backref='messages')

class Wishlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=True)
    subject = db.Column(db.String(100), nullable=True)
    department = db.Column(db.String(100), nullable=True)
    notifications = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    review_text = db.Column(db.Text, nullable=True)
    transaction_type = db.Column(db.String(20), nullable=False)  # buy, swap, free
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    book = db.relationship('Book', backref='reviews')
    reviewer = db.relationship('User', foreign_keys=[reviewer_id], backref='reviews_given')
    seller = db.relationship('User', foreign_keys=[seller_id], backref='reviews_received')

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    transaction_type = db.Column(db.String(20), nullable=False)  # buy, swap, free
    amount = db.Column(db.Float, nullable=True)  # For purchases
    status = db.Column(db.String(20), default='pending')  # pending, completed, cancelled
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    book = db.relationship('Book', backref='transactions')
    seller = db.relationship('User', foreign_keys=[seller_id], backref='sales')
    buyer = db.relationship('User', foreign_keys=[buyer_id], backref='purchases')

class AdminLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    action = db.Column(db.String(100), nullable=False)
    target_type = db.Column(db.String(50), nullable=False)  # user, book, message
    target_id = db.Column(db.Integer, nullable=False)
    details = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    admin = db.relationship('User', backref='admin_actions')


# Routes
@app.route('/')
def index():
    # Get recent books
    recent_books = Book.query.filter_by(status='available').order_by(Book.created_at.desc()).limit(6).all()
    
    # Get statistics
    stats = {
        'total_books': Book.query.count(),
        'total_users': User.query.count(),
        'books_available': Book.query.filter_by(status='available').count(),
        'total_exchanges': Message.query.count()
    }
    
    return render_template('index.html', recent_books=recent_books, stats=stats)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        full_name = request.form['full_name']
        college = request.form['college']
        department = request.form['department']
        year = int(request.form['year'])
        
        # Check if user exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists!', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered!', 'error')
            return render_template('register.html')
        
        # Create new user
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            full_name=full_name,
            college=college,
            department=department,
            year=year
        )
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['is_admin'] = user.is_admin
            flash(f'Welcome back, {user.full_name}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password!', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    user = db.session.get(User, session['user_id'])
    if not user:
        flash('User not found. Please log in again.', 'error')
        session.clear()
        return redirect(url_for('login'))
        
    user_books = Book.query.filter_by(user_id=session['user_id']).all()
    
    # Get recent messages
    recent_messages = Message.query.filter_by(receiver_id=session['user_id']).order_by(Message.created_at.desc()).limit(5).all()
    
    # Get wishlist items
    wishlist_count = Wishlist.query.filter_by(user_id=session['user_id']).count()
    
    # Calculate stats
    stats = {
        'books_listed': len(user_books),
        'books_available': len([b for b in user_books if b.status == 'available']),
        'books_sold': len([b for b in user_books if b.status == 'sold']),
        'total_views': sum(book.views or 0 for book in user_books),
        'unread_messages': Message.query.filter_by(receiver_id=session['user_id'], is_read=False).count(),
        'wishlist_items': wishlist_count,
        'points': user.points or 0
    }
    
    return render_template('dashboard.html', 
                         user=user, 
                         user_books=user_books, 
                         recent_messages=recent_messages,
                         stats=stats)

@app.route('/track_view/<int:book_id>', methods=['POST'])
def track_view(book_id):
    book = Book.query.get(book_id)
    if book:
        book.views = (book.views or 0) + 1
        db.session.commit()
    return {'success': True}

@app.route('/books')
def books():
    # Get filter parameters
    search = request.args.get('search', '')
    department = request.args.get('department', '')
    condition = request.args.get('condition', '')
    swap_type = request.args.get('swap_type', '')
    year = request.args.get('year', '')
    page = request.args.get('page', 1, type=int)
    
    # Build query
    query = Book.query.filter_by(status='available')
    
    if search:
        query = query.filter(
            (Book.title.contains(search)) |
            (Book.author.contains(search)) |
            (Book.subject.contains(search))
        )
    
    if department:
        query = query.filter_by(department=department)
    
    if condition:
        query = query.filter_by(condition=condition)
    
    if swap_type:
        query = query.filter_by(swap_type=swap_type)
    
    if year:
        query = query.filter_by(year_of_study=int(year))
    
    # Paginate results
    books = query.order_by(Book.created_at.desc()).paginate(
        page=page, per_page=12, error_out=False
    )
    
    # Get filter options
    departments = db.session.query(Book.department.distinct()).all()
    departments = [d[0] for d in departments]
    
    conditions = ['Excellent', 'Good', 'Fair', 'Poor']
    swap_types = ['sell', 'swap', 'free']
    years = [1, 2, 3, 4, 5]
    
    current_filters = {
        'search': search,
        'department': department,
        'condition': condition,
        'swap_type': swap_type,
        'year': year
    }
    
    return render_template('search.html', 
                         books=books,
                         departments=departments,
                         conditions=conditions,
                         swap_types=swap_types,
                         years=years,
                         current_filters=current_filters)

@app.route('/book/<int:id>')
def book_detail(id):
    book = Book.query.get_or_404(id)
    
    # Track view
    book.views = (book.views or 0) + 1
    db.session.commit()
    
    # Get similar books
    similar_books = Book.query.filter(
        Book.id != book.id,
        Book.status == 'available',
        (Book.subject == book.subject) | (Book.department == book.department)
    ).limit(4).all()
    
    # Get reviews for this book
    reviews = Review.query.filter_by(book_id=id).order_by(Review.created_at.desc()).all()
    
    # Calculate average rating
    avg_rating = 0
    if reviews:
        avg_rating = sum(review.rating for review in reviews) / len(reviews)
    
    # Check if current user can review (must be logged in and not the owner)
    can_review = False
    user_review = None
    if 'user_id' in session:
        user_id = session['user_id']
        can_review = (user_id != book.user_id)
        user_review = Review.query.filter_by(book_id=id, reviewer_id=user_id).first()
        if user_review:
            can_review = False
    
    return render_template('book_detail.html', 
                         book=book, 
                         similar_books=similar_books,
                         reviews=reviews,
                         avg_rating=avg_rating,
                         can_review=can_review,
                         user_review=user_review)

@app.route('/add_book', methods=['GET', 'POST'])
@login_required
def add_book():
    if request.method == 'POST':
        # Handle file upload
        image_filename = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                filename = secure_filename(file.filename)
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    # Create unique filename
                    import uuid
                    file_ext = filename.rsplit('.', 1)[1].lower()
                    image_filename = f"{uuid.uuid4().hex}.{file_ext}"
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
        
        # Create book
        book = Book(
            title=request.form['title'],
            author=request.form['author'],
            subject=request.form['subject'],
            department=request.form['department'],
            year_of_study=int(request.form['year_of_study']),
            condition=request.form['condition'],
            swap_type=request.form['swap_type'],
            price=float(request.form['price']) if request.form.get('price') else None,
            description=request.form.get('description', ''),
            isbn=request.form.get('isbn', ''),
            preferred_books=request.form.get('preferred_books', ''),
            contact_method=request.form.get('contact_method', 'message'),
            contact_info=request.form.get('contact_info', ''),
            image_filename=image_filename,
            user_id=session['user_id']
        )
        
        db.session.add(book)
        db.session.commit()
        
        flash('Book added successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('add_book.html')

@app.route('/book/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_book(id):
    book = Book.query.filter_by(id=id, user_id=session['user_id']).first()
    if not book:
        flash('Book not found or you do not have permission to edit it.', 'error')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        # Update book information
        book.title = request.form['title']
        book.author = request.form['author']
        book.subject = request.form['subject']
        book.department = request.form['department']
        book.year_of_study = int(request.form['year_of_study'])
        book.condition = request.form['condition']
        book.swap_type = request.form['swap_type']
        book.description = request.form['description']
        
        # Handle price
        if request.form['swap_type'] == 'sell':
            try:
                book.price = float(request.form['price'])
            except ValueError:
                book.price = 0.0
        else:
            book.price = None
        
        # Handle image upload
        if 'image' in request.files and request.files['image'].filename:
            file = request.files['image']
            if file and allowed_file(file.filename):
                # Delete old image if exists
                if book.image_filename:
                    try:
                        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], book.image_filename))
                    except:
                        pass
                
                # Save new image
                filename = secure_filename(file.filename)
                unique_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                file.save(file_path)
                book.image_filename = unique_filename
        
        db.session.commit()
        flash('Book updated successfully!', 'success')
        return redirect(url_for('book_detail', id=book.id))
    
    return render_template('edit_book.html', book=book)

@app.route('/messages')
@login_required
def messages():
    # Get all messages for the current user
    user_messages = db.session.query(Message).filter(
        (Message.sender_id == session['user_id']) | 
        (Message.receiver_id == session['user_id'])
    ).order_by(Message.created_at.desc()).all()
    
    # Group by conversation partner
    conversation_dict = {}
    for msg in user_messages:
        partner_id = msg.sender_id if msg.receiver_id == session['user_id'] else msg.receiver_id
        if partner_id not in conversation_dict:
            partner = User.query.get(partner_id)
            conversation_dict[partner_id] = {
                'partner': partner,
                'messages': [],
                'last_message': msg,
                'unread_count': 0
            }
        conversation_dict[partner_id]['messages'].append(msg)
        if msg.receiver_id == session['user_id'] and not msg.is_read:
            conversation_dict[partner_id]['unread_count'] += 1
    
    # Calculate message counts for template
    total_messages = len(user_messages)
    unread_count = sum(1 for msg in user_messages if msg.receiver_id == session['user_id'] and not msg.is_read)
    sent_count = sum(1 for msg in user_messages if msg.sender_id == session['user_id'])
    received_count = total_messages - sent_count
    
    message_counts = {
        'total': total_messages,
        'unread': unread_count,
        'sent': sent_count,
        'received': received_count
    }
    
    return render_template('messages.html', 
                         conversations=conversation_dict, 
                         messages=user_messages,
                         message_counts=message_counts)

@app.route('/send_message', methods=['POST'])
@login_required
def send_message():
    if 'recipient_username' in request.form:
        # New message by username
        recipient = User.query.filter_by(username=request.form['recipient_username']).first()
        if not recipient:
            flash('User not found!', 'error')
            return redirect(url_for('messages'))
        recipient_id = recipient.id
    else:
        # Reply to existing message
        recipient_id = request.form['recipient_id']
    
    book_id = request.form.get('book_id') if request.form.get('book_id') else None
    subject = request.form['subject']
    content = request.form['content']
    
    message = Message(
        sender_id=session['user_id'],
        receiver_id=recipient_id,
        book_id=book_id,
        subject=subject,
        content=content
    )
    
    db.session.add(message)
    db.session.commit()
    
    flash('Message sent successfully!', 'success')
    return redirect(url_for('messages'))

@app.route('/message/<int:message_id>')
@login_required
def view_message(message_id):
    message = Message.query.filter(
        Message.id == message_id,
        (Message.sender_id == session['user_id']) | (Message.receiver_id == session['user_id'])
    ).first()
    
    if not message:
        return jsonify({'error': 'Message not found'}), 404
    
    # Mark as read if it's for the current user
    if message.receiver_id == session['user_id'] and not message.is_read:
        message.is_read = True
        db.session.commit()
    
    return jsonify({
        'id': message.id,
        'subject': message.subject,
        'content': message.content,
        'sender': message.sender.username,
        'receiver': message.receiver.username,
        'book_title': message.book.title if message.book else None,
        'created_at': message.created_at.strftime('%Y-%m-%d %H:%M'),
        'is_read': message.is_read
    })

@app.route('/message/<int:message_id>/read', methods=['POST'])
@login_required
def mark_message_read(message_id):
    message = Message.query.filter(
        Message.id == message_id,
        Message.receiver_id == session['user_id']
    ).first()
    
    if message:
        message.is_read = True
        db.session.commit()
        return jsonify({'success': True})
    
    return jsonify({'success': False}), 404

@app.route('/message/<int:message_id>/delete', methods=['POST'])
@login_required
def delete_message(message_id):
    message = Message.query.filter(
        Message.id == message_id,
        (Message.sender_id == session['user_id']) | (Message.receiver_id == session['user_id'])
    ).first()
    
    if message:
        db.session.delete(message)
        db.session.commit()
        return jsonify({'success': True})
    
    return jsonify({'success': False}), 404

@app.route('/messages/mark-all-read', methods=['POST'])
@login_required
def mark_all_messages_read():
    messages = Message.query.filter(
        Message.receiver_id == session['user_id'],
        Message.is_read == False
    ).all()
    
    for message in messages:
        message.is_read = True
    
    db.session.commit()
    return jsonify({'success': True, 'count': len(messages)})

@app.route('/wishlist')
@login_required
def wishlist():
    items = Wishlist.query.filter_by(user_id=session['user_id']).all()
    
    # Find matching books for each wishlist item
    matches = {}
    for item in items:
        matching_books = Book.query.filter(
            Book.status == 'available',
            Book.title.contains(item.book_title)
        ).limit(3).all()
        matches[item.id] = matching_books
    
    # Get popular wishlist items
    popular_wishlist_items = db.session.query(
        Wishlist.book_title,
        Wishlist.author,
        db.func.count(Wishlist.id).label('count')
    ).group_by(Wishlist.book_title, Wishlist.author).order_by(db.desc('count')).limit(5).all()
    
    # Calculate stats
    matches_count = sum(len(match_list) for match_list in matches.values())
    recent_items_count = len([item for item in items if (datetime.utcnow() - item.created_at).days <= 7])
    
    return render_template('wishlist.html', 
                         wishlist_items=items, 
                         matches=matches,
                         popular_wishlist_items=popular_wishlist_items,
                         matches_count=matches_count,
                         recent_items_count=recent_items_count,
                         notifications_count=0)

@app.route('/add_to_wishlist', methods=['POST'])
@login_required
def add_to_wishlist():
    book_title = request.form['book_title']
    author = request.form.get('author', '')
    subject = request.form.get('subject', '')
    department = request.form.get('department', '')
    
    # Check if already in wishlist
    existing = Wishlist.query.filter_by(
        user_id=session['user_id'],
        book_title=book_title
    ).first()
    
    if existing:
        flash('Book already in your wishlist!', 'info')
    else:
        wishlist_item = Wishlist(
            user_id=session['user_id'],
            book_title=book_title,
            author=author,
            subject=subject,
            department=department
        )
        db.session.add(wishlist_item)
        db.session.commit()
        flash('Book added to wishlist!', 'success')
    
    return redirect(url_for('wishlist'))

@app.route('/edit_wishlist_item', methods=['POST'])
@login_required
def edit_wishlist_item():
    item_id = request.form['item_id']
    book_title = request.form['book_title']
    author = request.form.get('author', '')
    subject = request.form.get('subject', '')
    department = request.form.get('department', '')
    
    wishlist_item = Wishlist.query.filter_by(id=item_id, user_id=session['user_id']).first()
    if wishlist_item:
        wishlist_item.book_title = book_title
        wishlist_item.author = author
        wishlist_item.subject = subject
        wishlist_item.department = department
        db.session.commit()
        flash('Wishlist item updated!', 'success')
    else:
        flash('Wishlist item not found!', 'error')
    
    return redirect(url_for('wishlist'))

@app.route('/wishlist/<int:item_id>/remove', methods=['POST'])
@login_required
def remove_wishlist_item(item_id):
    wishlist_item = Wishlist.query.filter_by(id=item_id, user_id=session['user_id']).first()
    if wishlist_item:
        db.session.delete(wishlist_item)
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': 'Item not found'})

@app.route('/book/<int:book_id>/delete', methods=['POST'])
@login_required
def delete_book(book_id):
    book = Book.query.filter_by(id=book_id, user_id=session['user_id']).first()
    if book:
        # Delete associated image file
        if book.image_filename:
            try:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], book.image_filename))
            except:
                pass
        
        db.session.delete(book)
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': 'Book not found'})

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = db.session.get(User, session['user_id'])
    if not user:
        flash('User not found!', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        if request.form.get('action') == 'change_password':
            # Handle password change
            current_password = request.form['current_password']
            new_password = request.form['new_password']
            confirm_password = request.form['confirm_password']
            
            if not check_password_hash(user.password_hash, current_password):
                flash('Current password is incorrect!', 'error')
            elif new_password != confirm_password:
                flash('New passwords do not match!', 'error')
            else:
                user.password_hash = generate_password_hash(new_password)
                db.session.commit()
                flash('Password updated successfully!', 'success')
        else:
            # Handle profile update
            user.full_name = request.form['full_name']
            user.email = request.form['email']
            user.phone = request.form.get('phone', '')
            user.college = request.form['college']
            user.department = request.form['department']
            user.year = int(request.form['year'])
            user.hostel = request.form.get('hostel', '')
            
            db.session.commit()
            flash('Profile updated successfully!', 'success')
        
        return redirect(url_for('profile'))
    
    return render_template('profile.html', user=user)

@app.route('/leaderboard')
def leaderboard():
    # Get top users by points
    top_users = User.query.order_by(User.points.desc()).limit(10).all()
    
    # Get top book contributors
    top_contributors = db.session.query(
        User, db.func.count(Book.id).label('book_count')
    ).join(Book).group_by(User.id).order_by(db.desc('book_count')).limit(10).all()
    
    return render_template('leaderboard.html', 
                         top_users=top_users, 
                         top_contributors=top_contributors)

@app.route('/analytics')
@login_required
def analytics():
    user = db.session.get(User, session['user_id'])
    if not user or not user.is_admin:
        flash('Access denied. Admin only.', 'error')
        return redirect(url_for('dashboard'))
    
    # Get analytics data
    total_users = User.query.count()
    total_books = Book.query.count()
    total_messages = Message.query.count()
    books_available = Book.query.filter_by(status='available').count()
    
    # Get recent activity
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    recent_books = Book.query.order_by(Book.created_at.desc()).limit(5).all()
    
    stats = {
        'total_users': total_users,
        'total_books': total_books,
        'total_messages': total_messages,
        'books_available': books_available,
        'recent_users': recent_users,
        'recent_books': recent_books
    }
    
    return render_template('analytics.html', stats=stats)

# Admin Routes
@app.route('/admin')
@admin_required
def admin_dashboard():
    # Get comprehensive statistics
    stats = {
        'total_users': User.query.count(),
        'total_books': Book.query.count(),
        'available_books': Book.query.filter_by(status='available').count(),
        'sold_books': Book.query.filter_by(status='sold').count(),
        'total_messages': Message.query.count(),
        'total_reviews': Review.query.count(),
        'total_transactions': Transaction.query.count(),
        'pending_transactions': Transaction.query.filter_by(status='pending').count()
    }
    
    # Get recent activity
    recent_users = User.query.order_by(User.created_at.desc()).limit(10).all()
    recent_books = Book.query.order_by(Book.created_at.desc()).limit(10).all()
    recent_reviews = Review.query.order_by(Review.created_at.desc()).limit(10).all()
    
    # Get department statistics
    dept_stats = db.session.query(
        User.department, 
        db.func.count(User.id).label('user_count')
    ).group_by(User.department).all()
    
    return render_template('admin/dashboard.html', 
                         stats=stats, 
                         recent_users=recent_users,
                         recent_books=recent_books,
                         recent_reviews=recent_reviews,
                         dept_stats=dept_stats)

@app.route('/admin/users')
@admin_required
def admin_users():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    department = request.args.get('department', '')
    
    query = User.query
    
    if search:
        query = query.filter(User.username.contains(search) | 
                           User.email.contains(search) |
                           User.full_name.contains(search))
    
    if department:
        query = query.filter(User.department == department)
    
    users = query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False)
    
    # Get all departments for filter
    departments = db.session.query(User.department.distinct()).all()
    departments = [d[0] for d in departments]
    
    return render_template('admin/users.html', 
                         users=users, 
                         search=search,
                         department=department,
                         departments=departments)

@app.route('/admin/books')
@admin_required
def admin_books():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    status = request.args.get('status', '')
    department = request.args.get('department', '')
    
    query = Book.query.join(User)
    
    if search:
        query = query.filter(Book.title.contains(search) | 
                           Book.author.contains(search) |
                           Book.subject.contains(search))
    
    if status:
        query = query.filter(Book.status == status)
    
    if department:
        query = query.filter(Book.department == department)
    
    books = query.order_by(Book.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False)
    
    # Get filter options
    departments = db.session.query(Book.department.distinct()).all()
    departments = [d[0] for d in departments]
    
    statuses = ['available', 'sold', 'reserved', 'suspended']
    
    return render_template('admin/books.html', 
                         books=books,
                         search=search,
                         status=status,
                         department=department,
                         departments=departments,
                         statuses=statuses)

@app.route('/admin/reviews')
@admin_required
def admin_reviews():
    page = request.args.get('page', 1, type=int)
    rating = request.args.get('rating', '')
    
    query = Review.query.join(Book).join(User, Review.reviewer_id == User.id)
    
    if rating:
        query = query.filter(Review.rating == int(rating))
    
    reviews = query.order_by(Review.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False)
    
    return render_template('admin/reviews.html', reviews=reviews, rating=rating)

@app.route('/admin/user/<int:user_id>/toggle_admin', methods=['POST'])
@admin_required
def toggle_user_admin(user_id):
    user = User.query.get_or_404(user_id)
    
    # Don't allow removing admin from the current admin
    if user.id == session['user_id'] and user.is_admin:
        flash('Cannot remove admin privileges from yourself.', 'error')
        return redirect(url_for('admin_users'))
    
    user.is_admin = not user.is_admin
    db.session.commit()
    
    # Log admin action
    log_admin_action('toggle_admin', 'user', user_id, 
                    f"Set admin status to {user.is_admin}")
    
    flash(f"Admin status updated for {user.username}.", 'success')
    return redirect(url_for('admin_users'))

@app.route('/admin/book/<int:book_id>/update_status', methods=['POST'])
@admin_required
def update_book_status(book_id):
    book = Book.query.get_or_404(book_id)
    new_status = request.form['status']
    
    old_status = book.status
    book.status = new_status
    db.session.commit()
    
    # Log admin action
    log_admin_action('update_status', 'book', book_id,
                    f"Changed status from {old_status} to {new_status}")
    
    flash(f"Book status updated to {new_status}.", 'success')
    return redirect(url_for('admin_books'))

@app.route('/admin/user/<int:user_id>/delete', methods=['POST'])
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    
    # Don't allow deleting yourself
    if user.id == session['user_id']:
        flash('Cannot delete your own account.', 'error')
        return redirect(url_for('admin_users'))
    
    username = user.username
    
    # Delete user's books, messages, etc.
    Book.query.filter_by(user_id=user_id).delete()
    Message.query.filter((Message.sender_id == user_id) | (Message.receiver_id == user_id)).delete()
    Review.query.filter((Review.reviewer_id == user_id) | (Review.seller_id == user_id)).delete()
    Wishlist.query.filter_by(user_id=user_id).delete()
    Transaction.query.filter((Transaction.seller_id == user_id) | (Transaction.buyer_id == user_id)).delete()
    
    db.session.delete(user)
    db.session.commit()
    
    # Log admin action
    log_admin_action('delete_user', 'user', user_id, f"Deleted user {username}")
    
    flash(f"User {username} has been deleted.", 'success')
    return redirect(url_for('admin_users'))

@app.route('/admin/book/<int:book_id>/delete', methods=['POST'])
@admin_required
def admin_delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    
    book_title = book.title
    
    # Delete related data
    Message.query.filter_by(book_id=book_id).delete()
    Review.query.filter_by(book_id=book_id).delete()
    Transaction.query.filter_by(book_id=book_id).delete()
    
    db.session.delete(book)
    db.session.commit()
    
    # Log admin action
    log_admin_action('delete_book', 'book', book_id, f"Deleted book {book_title}")
    
    flash(f"Book '{book_title}' has been deleted.", 'success')
    return redirect(url_for('admin_books'))

def log_admin_action(action, target_type, target_id, details):
    """Log admin actions for audit trail"""
    log = AdminLog(
        admin_id=session['user_id'],
        action=action,
        target_type=target_type,
        target_id=target_id,
        details=details
    )
    db.session.add(log)
    db.session.commit()

# Book Status and Review Routes
@app.route('/book/<int:book_id>/mark_status', methods=['POST'])
@login_required
def mark_book_status(book_id):
    book = Book.query.get_or_404(book_id)
    
    # Only book owner can mark status
    if book.user_id != session['user_id']:
        flash('You can only update your own books.', 'error')
        return redirect(url_for('book_detail', id=book_id))
    
    new_status = request.form['status']
    book.status = new_status
    db.session.commit()
    
    flash(f"Book status updated to {new_status}.", 'success')
    return redirect(url_for('book_detail', id=book_id))

@app.route('/book/<int:book_id>/review', methods=['POST'])
@login_required
def add_review(book_id):
    book = Book.query.get_or_404(book_id)
    
    # Check if user already reviewed this book
    existing_review = Review.query.filter_by(
        book_id=book_id, 
        reviewer_id=session['user_id']
    ).first()
    
    if existing_review:
        flash('You have already reviewed this book.', 'error')
        return redirect(url_for('book_detail', id=book_id))
    
    # Can't review your own book
    if book.user_id == session['user_id']:
        flash('You cannot review your own book.', 'error')
        return redirect(url_for('book_detail', id=book_id))
    
    rating = int(request.form['rating'])
    review_text = request.form.get('review_text', '')
    transaction_type = request.form['transaction_type']
    
    review = Review(
        book_id=book_id,
        reviewer_id=session['user_id'],
        seller_id=book.user_id,
        rating=rating,
        review_text=review_text,
        transaction_type=transaction_type
    )
    
    db.session.add(review)
    
    # Award points to seller for good reviews
    if rating >= 4:
        seller = User.query.get(book.user_id)
        seller.points += 5
    
    db.session.commit()
    
    flash('Review added successfully!', 'success')
    return redirect(url_for('book_detail', id=book_id))

@app.route('/health')
def health_check():
    return {'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()}


# Template filter for time ago
@app.template_filter('timeago')
def timeago(date):
    now = datetime.utcnow()
    diff = now - date
    
    if diff.days > 0:
        return f"{diff.days} days ago"
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f"{hours} hours ago"
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f"{minutes} minutes ago"
    else:
        return "Just now"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
