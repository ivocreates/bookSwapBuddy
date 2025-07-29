from app import app, db, User, Book, Message, Wishlist
from datetime import datetime, timedelta
import random

def init_database():
    """Initialize database with sample data"""
    
    with app.app_context():
        # Drop all tables and recreate
        db.drop_all()
        db.create_all()
        
        print("Creating sample users...")
        
        # Create admin user
        admin = User(
            username='admin',
            email='admin@bookswapbuddy.com',
            full_name='System Administrator',
            college='BookSwapBuddy University',
            department='Administration',
            year=1,
            points=500,
            is_admin=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Create sample students
        students_data = [
            {
                'username': 'arjun_sharma',
                'email': 'arjun.sharma@student.edu',
                'full_name': 'Arjun Sharma',
                'college': 'Indian Institute of Technology Delhi',
                'department': 'Computer Science Engineering',
                'year': 3,
                'hostel': 'Nilgiri Hostel',
                'phone': '+91-9876543210',
                'points': 150
            },
            {
                'username': 'priya_patel',
                'email': 'priya.patel@student.edu',
                'full_name': 'Priya Patel',
                'college': 'Indian Institute of Technology Delhi',
                'department': 'Electronics and Communication',
                'year': 2,
                'hostel': 'Aravali Hostel',
                'phone': '+91-9876543211',
                'points': 225
            },
            {
                'username': 'rahul_kumar',
                'email': 'rahul.kumar@student.edu',
                'full_name': 'Rahul Kumar',
                'college': 'Indian Institute of Technology Delhi',
                'department': 'Mechanical Engineering',
                'year': 4,
                'hostel': 'Shivalik Hostel',
                'phone': '+91-9876543212',
                'points': 75
            },
            {
                'username': 'sneha_singh',
                'email': 'sneha.singh@student.edu',
                'full_name': 'Sneha Singh',
                'college': 'Indian Institute of Technology Delhi',
                'department': 'Civil Engineering',
                'year': 1,
                'hostel': 'Girnar Hostel',
                'phone': '+91-9876543213',
                'points': 300
            },
            {
                'username': 'vivek_gupta',
                'email': 'vivek.gupta@student.edu',
                'full_name': 'Vivek Gupta',
                'college': 'Indian Institute of Technology Delhi',
                'department': 'Chemical Engineering',
                'year': 3,
                'hostel': 'Karakoram Hostel',
                'phone': '+91-9876543214',
                'points': 125
            },
            {
                'username': 'ananya_reddy',
                'email': 'ananya.reddy@student.edu',
                'full_name': 'Ananya Reddy',
                'college': 'Indian Institute of Technology Delhi',
                'department': 'Electrical Engineering',
                'year': 2,
                'hostel': 'Zanskar Hostel',
                'phone': '+91-9876543215',
                'points': 180
            }
        ]
        
        users = []
        for user_data in students_data:
            user = User(**user_data)
            user.set_password('password123')
            db.session.add(user)
            users.append(user)
        
        db.session.commit()
        print(f"Created {len(users) + 1} users")
        
        # Create sample books
        print("Creating sample books...")
        
        books_data = [
            # Computer Science Books
            {
                'title': 'Introduction to Algorithms (CLRS)',
                'author': 'Thomas H. Cormen',
                'subject': 'Data Structures and Algorithms',
                'department': 'Computer Science Engineering',
                'year_of_study': 2,
                'condition': 'Very Good',
                'price': 450.0,
                'swap_type': 'sell',
                'description': 'Classic algorithms textbook. Excellent condition with minimal highlighting.',
                'user_id': users[0].id
            },
            {
                'title': 'Operating System Concepts',
                'author': 'Abraham Silberschatz',
                'subject': 'Operating Systems',
                'department': 'Computer Science Engineering',
                'year_of_study': 3,
                'condition': 'Good',
                'price': 350.0,
                'swap_type': 'sell',
                'description': 'Comprehensive OS textbook. Some notes in margins.',
                'user_id': users[0].id
            },
            {
                'title': 'Computer Networks',
                'author': 'Andrew S. Tanenbaum',
                'subject': 'Computer Networks',
                'department': 'Computer Science Engineering',
                'year_of_study': 3,
                'condition': 'Like New',
                'price': 0.0,
                'swap_type': 'free',
                'description': 'Excellent networking book. Free for a good student!',
                'user_id': users[5].id
            },
            
            # Electronics Books
            {
                'title': 'Electronic Devices and Circuit Theory',
                'author': 'Robert Boylestad',
                'subject': 'Electronic Devices',
                'department': 'Electronics and Communication',
                'year_of_study': 2,
                'condition': 'Good',
                'price': 300.0,
                'swap_type': 'sell',
                'description': 'Essential electronics textbook with practice problems.',
                'user_id': users[1].id
            },
            {
                'title': 'Signals and Systems',
                'author': 'Alan V. Oppenheim',
                'subject': 'Signals and Systems',
                'department': 'Electronics and Communication',
                'year_of_study': 3,
                'condition': 'Very Good',
                'price': 0.0,
                'swap_type': 'swap',
                'description': 'Looking to swap for Digital Signal Processing book.',
                'user_id': users[1].id
            },
            
            # Mechanical Engineering Books
            {
                'title': 'Engineering Mechanics: Statics',
                'author': 'R.C. Hibbeler',
                'subject': 'Engineering Mechanics',
                'department': 'Mechanical Engineering',
                'year_of_study': 1,
                'condition': 'Good',
                'price': 250.0,
                'swap_type': 'sell',
                'description': 'Fundamental mechanics book. Great for first year students.',
                'user_id': users[2].id
            },
            {
                'title': 'Thermodynamics: An Engineering Approach',
                'author': 'Yunus A. Cengel',
                'subject': 'Thermodynamics',
                'department': 'Mechanical Engineering',
                'year_of_study': 2,
                'condition': 'Like New',
                'price': 400.0,
                'swap_type': 'sell',
                'description': 'Comprehensive thermodynamics textbook. Barely used.',
                'user_id': users[2].id
            },
            
            # Civil Engineering Books
            {
                'title': 'Structural Analysis',
                'author': 'R.C. Hibbeler',
                'subject': 'Structural Engineering',
                'department': 'Civil Engineering',
                'year_of_study': 3,
                'condition': 'Good',
                'price': 0.0,
                'swap_type': 'swap',
                'description': 'Looking to swap for Concrete Technology book.',
                'user_id': users[3].id
            },
            {
                'title': 'Fluid Mechanics',
                'author': 'Frank M. White',
                'subject': 'Fluid Mechanics',
                'department': 'Civil Engineering',
                'year_of_study': 2,
                'condition': 'Very Good',
                'price': 320.0,
                'swap_type': 'sell',
                'description': 'Essential fluid mechanics textbook with solved examples.',
                'user_id': users[3].id
            },
            
            # Chemical Engineering Books
            {
                'title': 'Chemical Process Safety',
                'author': 'Daniel A. Crowl',
                'subject': 'Process Safety',
                'department': 'Chemical Engineering',
                'year_of_study': 4,
                'condition': 'Good',
                'price': 280.0,
                'swap_type': 'sell',
                'description': 'Important safety concepts for chemical engineers.',
                'user_id': users[4].id
            },
            {
                'title': 'Unit Operations of Chemical Engineering',
                'author': 'Warren McCabe',
                'subject': 'Unit Operations',
                'department': 'Chemical Engineering',
                'year_of_study': 3,
                'condition': 'Very Good',
                'price': 0.0,
                'swap_type': 'free',
                'description': 'Classic ChemE textbook. Free for final year students.',
                'user_id': users[4].id
            },
            
            # Electrical Engineering Books
            {
                'title': 'Electrical Machines',
                'author': 'P.S. Bimbhra',
                'subject': 'Electrical Machines',
                'department': 'Electrical Engineering',
                'year_of_study': 3,
                'condition': 'Good',
                'price': 340.0,
                'swap_type': 'sell',
                'description': 'Comprehensive book on electrical machines and drives.',
                'user_id': users[5].id
            },
            {
                'title': 'Power System Analysis',
                'author': 'John J. Grainger',
                'subject': 'Power Systems',
                'department': 'Electrical Engineering',
                'year_of_study': 4,
                'condition': 'Like New',
                'price': 380.0,
                'swap_type': 'sell',
                'description': 'Advanced power system concepts. Minimal wear.',
                'user_id': users[5].id
            },
            
            # General Engineering Books
            {
                'title': 'Engineering Mathematics',
                'author': 'B.S. Grewal',
                'subject': 'Mathematics',
                'department': 'Computer Science Engineering',
                'year_of_study': 1,
                'condition': 'Good',
                'price': 200.0,
                'swap_type': 'sell',
                'description': 'Essential math book for all engineering branches.',
                'user_id': users[0].id
            },
            {
                'title': 'Technical Communication',
                'author': 'Meenakshi Raman',
                'subject': 'Communication Skills',
                'department': 'Computer Science Engineering',
                'year_of_study': 1,
                'condition': 'Very Good',
                'price': 0.0,
                'swap_type': 'free',
                'description': 'Communication skills book. Free for first year students.',
                'user_id': users[1].id
            }
        ]
        
        books = []
        for book_data in books_data:
            book = Book(**book_data)
            db.session.add(book)
            books.append(book)
        
        db.session.commit()
        
        # Generate QR codes for all books
        for book in books:
            book.generate_qr_code()
        
        db.session.commit()
        print(f"Created {len(books)} books with QR codes")
        
        # Create sample messages
        print("Creating sample messages...")
        
        messages_data = [
            {
                'sender_id': users[1].id,
                'receiver_id': users[0].id,
                'book_id': books[0].id,
                'content': 'Hi! Is the CLRS algorithms book still available? I\'m really interested in buying it.',
                'created_at': datetime.utcnow() - timedelta(hours=2)
            },
            {
                'sender_id': users[0].id,
                'receiver_id': users[1].id,
                'book_id': books[0].id,
                'content': 'Yes, it\'s still available! The condition is really good. When would you like to meet?',
                'created_at': datetime.utcnow() - timedelta(hours=1)
            },
            {
                'sender_id': users[2].id,
                'receiver_id': users[4].id,
                'book_id': books[10].id,
                'content': 'I saw your Unit Operations book is free. I\'m a final year student and would love to have it!',
                'created_at': datetime.utcnow() - timedelta(hours=3)
            },
            {
                'sender_id': users[3].id,
                'receiver_id': users[1].id,
                'book_id': books[4].id,
                'content': 'I have a Digital Signal Processing book. Would you like to swap for your Signals and Systems book?',
                'created_at': datetime.utcnow() - timedelta(hours=4)
            }
        ]
        
        for msg_data in messages_data:
            message = Message(**msg_data)
            db.session.add(message)
        
        db.session.commit()
        print(f"Created {len(messages_data)} sample messages")
        
        # Create sample wishlist items
        print("Creating sample wishlist items...")
        
        wishlist_data = [
            {
                'user_id': users[0].id,
                'book_title': 'Database System Concepts',
                'author': 'Henry F. Korth',
                'subject': 'Database Management',
                'department': 'Computer Science Engineering'
            },
            {
                'user_id': users[1].id,
                'book_title': 'Digital Signal Processing',
                'author': 'John G. Proakis',
                'subject': 'Signal Processing',
                'department': 'Electronics and Communication'
            },
            {
                'user_id': users[2].id,
                'book_title': 'Machine Design',
                'author': 'Robert Norton',
                'subject': 'Machine Design',
                'department': 'Mechanical Engineering'
            },
            {
                'user_id': users[3].id,
                'book_title': 'Concrete Technology',
                'author': 'M.S. Shetty',
                'subject': 'Construction Materials',
                'department': 'Civil Engineering'
            }
        ]
        
        for wish_data in wishlist_data:
            wishlist_item = Wishlist(**wish_data)
            db.session.add(wishlist_item)
        
        db.session.commit()
        print(f"Created {len(wishlist_data)} wishlist items")
        
        print("\n=== Database Initialization Complete! ===")
        print("\nDemo Login Credentials:")
        print("------------------------")
        print("Admin Access:")
        print("  Username: admin")
        print("  Password: admin123")
        print("\nStudent Users:")
        print("  Username: arjun_sharma    Password: password123  (150 points)")
        print("  Username: priya_patel     Password: password123  (225 points)")
        print("  Username: rahul_kumar     Password: password123  (75 points)")
        print("  Username: sneha_singh     Password: password123  (300 points)")
        print("  Username: vivek_gupta     Password: password123  (125 points)")
        print("  Username: ananya_reddy    Password: password123  (180 points)")
        print("\nFeatures Included:")
        print("- 15 sample books across different engineering departments")
        print("- Sample messages between users")
        print("- Wishlist items for users")
        print("- QR codes for all books")
        print("- Points system with demo data")
        print("- Indian engineering college context")

if __name__ == '__main__':
    init_database()
