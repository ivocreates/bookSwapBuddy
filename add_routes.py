import os

# Add all the missing routes
routes_code = '''
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
    user = User.query.get(session['user_id'])
    user_books = Book.query.filter_by(user_id=session['user_id']).all()
    
    # Get recent messages
    recent_messages = Message.query.filter_by(receiver_id=session['user_id']).order_by(Message.created_at.desc()).limit(5).all()
    
    # Get wishlist items
    wishlist_count = Wishlist.query.filter_by(user_id=session['user_id']).count()
    
    # Calculate stats
    stats = {
        'books_listed': len(user_books),
        'books_available': len([b for b in user_books if b.status == 'available']),
        'total_views': sum(book.views or 0 for book in user_books),
        'unread_messages': Message.query.filter_by(receiver_id=session['user_id'], is_read=False).count(),
        'wishlist_items': wishlist_count,
        'points': user.points
    }
    
    return render_template('dashboard.html', 
                         user=user, 
                         user_books=user_books, 
                         recent_messages=recent_messages,
                         stats=stats)

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
    
    return render_template('book_detail.html', book=book, similar_books=similar_books)

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

@app.route('/health')
def health_check():
    return {'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()}
'''

# Read existing app.py
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Insert routes before the template filter and main section
insert_position = content.find('# Template filter for time ago')
if insert_position == -1:
    # If not found, insert before the if __name__ section
    insert_position = content.find("if __name__ == '__main__':")

if insert_position != -1:
    new_content = content[:insert_position] + routes_code + '\\n\\n' + content[insert_position:]
    
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("Added all routes to app.py successfully!")
else:
    print("Could not find insertion point in app.py")
