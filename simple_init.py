#!/usr/bin/env python3
"""
Simple database initialization script for BookSwapBuddy
"""

import os
import sys
from werkzeug.security import generate_password_hash
from datetime import datetime

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def init_database():
    """Initialize the database with basic data"""
    try:
        from app import app, db, User, Book, Message, Wishlist, Review, Transaction, AdminLog
        
        with app.app_context():
            print("Creating database tables...")
            db.create_all()
            
            # Check if admin already exists
            admin = User.query.filter_by(username='admin').first()
            if not admin:
                print("Creating admin user...")
                admin = User(
                    username='admin',
                    email='admin@bookswapbuddy.com',
                    password_hash=generate_password_hash('admin123'),
                    is_admin=True,
                    full_name='System Administrator',
                    college='BookSwapBuddy Admin',
                    department='Administration',
                    year=4,
                    points=500
                )
                db.session.add(admin)
            
            # Create demo users
            demo_users = [
                {
                    'username': 'alice_smith',
                    'email': 'alice@university.edu',
                    'password': 'password123',
                    'full_name': 'Alice Smith',
                    'college': 'Delhi University',
                    'department': 'Computer Science',
                    'year': 3,
                    'points': 150
                },
                {
                    'username': 'bob_jones',
                    'email': 'bob@university.edu',
                    'password': 'password123',
                    'full_name': 'Bob Jones',
                    'college': 'Delhi University',
                    'department': 'Mathematics',
                    'year': 2,
                    'points': 75
                },
                {
                    'username': 'carol_white',
                    'email': 'carol@university.edu',
                    'password': 'password123',
                    'full_name': 'Carol White',
                    'college': 'Delhi University',
                    'department': 'Physics',
                    'year': 4,
                    'points': 200
                }
            ]
            
            created_users = []
            for user_data in demo_users:
                existing_user = User.query.filter_by(username=user_data['username']).first()
                if not existing_user:
                    print(f"Creating user: {user_data['username']}")
                    user = User(
                        username=user_data['username'],
                        email=user_data['email'],
                        password_hash=generate_password_hash(user_data['password']),
                        full_name=user_data['full_name'],
                        college=user_data['college'],
                        department=user_data['department'],
                        year=user_data['year'],
                        points=user_data['points']
                    )
                    db.session.add(user)
                    created_users.append(user)
                else:
                    created_users.append(existing_user)
            
            db.session.commit()
            
            # Create demo books
            book_count = Book.query.count()
            if book_count < 5:  # Only add if we have fewer than 5 books
                print("Adding demo books...")
                
                demo_books = [
                    {
                        'title': 'Introduction to Algorithms',
                        'author': 'Thomas H. Cormen',
                        'subject': 'Data Structures and Algorithms',
                        'department': 'Computer Science',
                        'year_of_study': 2,
                        'condition': 'Good',
                        'swap_type': 'sell',
                        'price': 800.0,
                        'description': 'Comprehensive guide to algorithms and data structures',
                        'user_index': 0  # alice_smith
                    },
                    {
                        'title': 'Calculus: Early Transcendentals',
                        'author': 'James Stewart',
                        'subject': 'Calculus',
                        'department': 'Mathematics',
                        'year_of_study': 1,
                        'condition': 'Excellent',
                        'swap_type': 'sell',
                        'price': 600.0,
                        'description': 'Perfect for first-year calculus students',
                        'user_index': 1  # bob_jones
                    },
                    {
                        'title': 'Physics for Scientists and Engineers',
                        'author': 'Raymond A. Serway',
                        'subject': 'Physics',
                        'department': 'Physics',
                        'year_of_study': 2,
                        'condition': 'Good',
                        'swap_type': 'swap',
                        'price': None,
                        'description': 'Looking to swap for advanced physics books',
                        'user_index': 2  # carol_white
                    },
                    {
                        'title': 'Python Programming: An Introduction',
                        'author': 'John M. Zelle',
                        'subject': 'Programming',
                        'department': 'Computer Science',
                        'year_of_study': 1,
                        'condition': 'Very Good',
                        'swap_type': 'free',
                        'price': None,
                        'description': 'Great for beginners learning Python',
                        'user_index': 0  # alice_smith
                    },
                    {
                        'title': 'Linear Algebra and Its Applications',
                        'author': 'David C. Lay',
                        'subject': 'Linear Algebra',
                        'department': 'Mathematics',
                        'year_of_study': 2,
                        'condition': 'Good',
                        'swap_type': 'sell',
                        'price': 450.0,
                        'description': 'Excellent resource for linear algebra concepts',
                        'user_index': 1  # bob_jones
                    }
                ]
                
                created_books = []
                for book_data in demo_books:
                    book = Book(
                        title=book_data['title'],
                        author=book_data['author'],
                        subject=book_data['subject'],
                        department=book_data['department'],
                        year_of_study=book_data['year_of_study'],
                        condition=book_data['condition'],
                        swap_type=book_data['swap_type'],
                        price=book_data['price'],
                        description=book_data['description'],
                        user_id=created_users[book_data['user_index']].id,
                        status='available'
                    )
                    db.session.add(book)
                    created_books.append(book)
                
                db.session.commit()
                
                # Create demo reviews
                print("Adding demo reviews...")
                demo_reviews = [
                    {
                        'book_index': 0,  # Introduction to Algorithms
                        'reviewer_index': 1,  # bob_jones
                        'rating': 5,
                        'review_text': 'Excellent book! Very comprehensive and well-written.',
                        'transaction_type': 'buy'
                    },
                    {
                        'book_index': 1,  # Calculus book
                        'reviewer_index': 2,  # carol_white
                        'rating': 4,
                        'review_text': 'Good condition and helpful for understanding calculus concepts.',
                        'transaction_type': 'buy'
                    },
                    {
                        'book_index': 3,  # Python Programming
                        'reviewer_index': 2,  # carol_white
                        'rating': 5,
                        'review_text': 'Amazing that this was free! Perfect for beginners.',
                        'transaction_type': 'free'
                    }
                ]
                
                for review_data in demo_reviews:
                    book = created_books[review_data['book_index']]
                    reviewer = created_users[review_data['reviewer_index']]
                    
                    review = Review(
                        book_id=book.id,
                        reviewer_id=reviewer.id,
                        seller_id=book.user_id,
                        rating=review_data['rating'],
                        review_text=review_data['review_text'],
                        transaction_type=review_data['transaction_type']
                    )
                    db.session.add(review)
                
                # Create demo wishlist items
                print("Adding demo wishlist items...")
                wishlist_items = [
                    {
                        'user_index': 0,  # alice_smith
                        'book_title': 'Advanced Data Structures',
                        'author': 'Mark Allen Weiss',
                        'subject': 'Computer Science'
                    },
                    {
                        'user_index': 1,  # bob_jones
                        'book_title': 'Abstract Algebra',
                        'author': 'David S. Dummit',
                        'subject': 'Mathematics'
                    }
                ]
                
                for item_data in wishlist_items:
                    user = created_users[item_data['user_index']]
                    wishlist_item = Wishlist(
                        user_id=user.id,
                        book_title=item_data['book_title'],
                        author=item_data['author'],
                        subject=item_data['subject']
                    )
                    db.session.add(wishlist_item)
                
                # Create demo messages
                print("Adding demo messages...")
                demo_messages = [
                    {
                        'sender_index': 1,  # bob_jones
                        'receiver_index': 0,  # alice_smith
                        'book_index': 0,  # Introduction to Algorithms
                        'subject': 'Interested in your Algorithms book',
                        'content': 'Hi! I\'m interested in purchasing your Introduction to Algorithms book. Is it still available?'
                    },
                    {
                        'sender_index': 2,  # carol_white
                        'receiver_index': 1,  # bob_jones
                        'book_index': 1,  # Calculus book
                        'subject': 'Question about Calculus book condition',
                        'content': 'Hello! Could you provide more details about the condition of the calculus book?'
                    }
                ]
                
                for msg_data in demo_messages:
                    sender = created_users[msg_data['sender_index']]
                    receiver = created_users[msg_data['receiver_index']]
                    book = created_books[msg_data['book_index']]
                    
                    message = Message(
                        sender_id=sender.id,
                        receiver_id=receiver.id,
                        book_id=book.id,
                        subject=msg_data['subject'],
                        content=msg_data['content']
                    )
                    db.session.add(message)
            
            db.session.commit()
            print("✅ Database initialized successfully!")
            print("\n🔐 Login Credentials:")
            print("Admin: admin / admin123")
            print("Users: alice_smith / password123")
            print("       bob_jones / password123")
            print("       carol_white / password123")
            
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == '__main__':
    init_database()
