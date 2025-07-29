# BookSwapBuddy 📘 - Student Book Exchange Platform

**A comprehensive web application for Indian students to exchange, buy, sell, and share academic books within their college community.**

![BookSwapBuddy](https://img.shields.io/badge/Python-3.10%2B-blue) ![Flask](https://img.shields.io/badge/Flask-2.3.3-green) ![Bootstrap](https://img.shields.io/badge/Bootstrap-5.0-purple) ![Status](https://img.shields.io/badge/Status-Production%20Ready-success)

## 🌟 Features

### 📚 Core Functionality
- **Book Exchange**: Buy, sell, or swap academic books with fellow students
- **Smart Search**: Find books by title, author, subject, department, or year
- **Book Status Management**: Track book availability (available, sold, reserved, suspended)
- **Wishlist System**: Add desired books to wishlist with smart matching
- **Messaging System**: Direct communication between users for book transactions
- **Review & Rating**: Rate books and sellers after transactions

### 👥 User Management
- **Student Registration**: Create account with college and department details
- **User Profiles**: Manage personal information, contact details, and preferences
- **Points System**: Earn points for successful transactions and good reviews
- **Leaderboard**: See top contributors and active users

### 🔧 Admin Features
- **Admin Dashboard**: Comprehensive overview of platform statistics
- **User Management**: View, edit, and manage user accounts
- **Book Management**: Monitor and moderate book listings
- **Review Management**: Oversee user reviews and ratings
- **Admin Actions**: Toggle admin privileges, update book status, delete content
- **Audit Trail**: Log all admin actions for accountability

### 🎨 Design & Accessibility
- **Indian Theme**: Vibrant color scheme reflecting Indian culture
- **Responsive Design**: Optimized for desktop, tablet, and mobile devices
- **High Contrast**: Excellent readability with accessible color combinations
- **Bootstrap 5**: Modern, clean interface with intuitive navigation
- **Font Awesome Icons**: Clear visual cues throughout the application

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)

### Automated Setup
Run the comprehensive setup script:

```bash
python setup.py
```

This will:
- Check Python version compatibility
- Install all required dependencies
- Create necessary directories
- Initialize the database with sample data
- Create environment configuration
- Run basic tests

### Manual Setup
If you prefer manual setup:

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Initialize database
python simple_init.py

# 3. Start the application
python start.py
```

### Start the Application
```bash
python start.py
```

Options:
- `--port`: Specify port (default: 5000)
- `--host`: Specify host (default: 0.0.0.0)
- `--debug`: Enable debug mode
- `--production`: Run in production mode

## 🏫 Demo Accounts

### Admin Account
- **Username**: `admin`
- **Password**: `admin123`
- **Access**: Full admin panel with user/book management

### Student Accounts
- **Username**: `alice_smith` | **Password**: `password123`
- **Username**: `bob_jones` | **Password**: `password123`
- **Username**: `carol_white` | **Password**: `password123`

## 📋 System Requirements

### Dependencies
```
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Werkzeug==2.3.7
Pillow==10.0.1
qrcode==7.4.2
```

### Indian Colleges & Departments
Pre-configured with popular Indian educational institutions:
- Delhi University, Mumbai University, Bangalore University
- IIT Delhi, Mumbai, Bangalore, Kanpur, Kharagpur
- NIT Trichy, Warangal, Calicut
- BITS Pilani, VIT Chennai, Manipal Institute
- Anna University, Pune University, Calcutta University

Departments include:
- Computer Science & Engineering
- Electronics & Communication Engineering
- Mechanical Engineering, Civil Engineering
- Mathematics, Physics, Chemistry, Biology
- Commerce, Economics, Business Administration
- English Literature, Hindi Literature
- And many more...

## 🗂️ Project Structure

```
BookSwapBuddy/
├── app.py                 # Main Flask application (999 lines)
├── simple_init.py         # Database initialization script
├── setup.py              # Comprehensive setup script
├── start.py              # Application start script
├── requirements.txt      # Python dependencies
├── README.md             # This documentation
├── instance/
│   └── bookswap.db       # SQLite database
├── static/
│   ├── css/
│   │   └── style.css     # Custom styling with Indian theme
│   ├── js/
│   │   └── custom.js     # Interactive JavaScript features
│   └── uploads/          # Book images and files
└── templates/
    ├── base.html         # Base template with navigation
    ├── index.html        # Landing page
    ├── login.html        # User authentication
    ├── register.html     # User registration
    ├── dashboard.html    # User dashboard
    ├── book_detail.html  # Book details with reviews
    ├── add_book.html     # Add new book listing
    ├── search.html       # Book search interface
    ├── messages.html     # Messaging system
    ├── wishlist.html     # User wishlist
    ├── profile.html      # User profile management
    ├── leaderboard.html  # Community leaderboard
    ├── analytics.html    # Admin analytics
    └── admin/            # Admin panel templates
        ├── dashboard.html
        ├── users.html
        ├── books.html
        └── reviews.html
```

## 🔧 Technical Architecture

### Backend
- **Framework**: Flask 2.3.3
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: Session-based with password hashing
- **File Handling**: Pillow for image processing
- **Security**: CSRF protection, input validation

### Database Models
- **User**: Student profiles with college/department info
- **Book**: Book listings with metadata and status
- **Message**: Direct messaging between users
- **Review**: Book and seller ratings
- **Wishlist**: User book wish lists
- **Transaction**: Transaction history
- **AdminLog**: Admin action audit trail

### Frontend
- **Framework**: Bootstrap 5 with custom CSS
- **JavaScript**: Vanilla JS with interactive features
- **Responsive**: Mobile-first design approach
- **Accessibility**: WCAG 2.1 compliant

## 🎯 Core Features Detail

### 📖 Book Management
- Add books with detailed information (title, author, subject, condition)
- Upload book images (JPEG, PNG supported)
- Set exchange type (buy, sell, swap, free)
- Track book status throughout transaction lifecycle
- QR code generation for easy sharing

### 💬 Communication
- Direct messaging between users
- Book-specific conversations
- Message history and organization
- Real-time notification system

### 🔍 Search & Discovery
- Advanced search with multiple filters
- Department and year-based filtering
- Condition and price range filters
- Smart wishlist matching
- Popular book recommendations

### 🏆 Gamification
- Points system for user engagement
- Leaderboard for top contributors
- Achievement-based rewards
- Community recognition

### ⚙️ Admin Control
- Comprehensive dashboard with key metrics
- User account management and moderation
- Book listing oversight and status control
- Review and rating moderation
- System-wide configuration options

## 🛡️ Security Features

- Password hashing with Werkzeug security
- Session-based authentication
- Admin privilege separation
- Input validation and sanitization
- CSRF protection on forms
- Secure file upload handling

## 🌐 Accessibility

- High contrast color scheme (saffron, white, green)
- Keyboard navigation support
- Screen reader compatibility
- Alternative text for images
- Clear focus indicators
- Responsive text sizing

## 📊 Analytics & Reporting

- User engagement metrics
- Book transaction statistics
- Department-wise activity
- Popular book trends
- Monthly/weekly activity reports

## 🔄 API Endpoints

### Public Routes
- `GET /` - Landing page
- `POST /register` - User registration
- `POST /login` - User authentication
- `GET /health` - Health check

### User Routes
- `GET /dashboard` - User dashboard
- `GET /books` - Browse books
- `GET /book/<id>` - Book details
- `POST /add_book` - Add new book
- `GET /messages` - User messages
- `POST /send_message` - Send message
- `GET /wishlist` - User wishlist
- `POST /add_to_wishlist` - Add to wishlist
- `GET /profile` - User profile
- `GET /leaderboard` - Community leaderboard

### Admin Routes
- `GET /admin` - Admin dashboard
- `GET /admin/users` - User management
- `GET /admin/books` - Book management
- `GET /admin/reviews` - Review management
- `POST /admin/user/<id>/toggle_admin` - Toggle admin status
- `POST /admin/book/<id>/update_status` - Update book status
- `POST /admin/user/<id>/delete` - Delete user
- `POST /admin/book/<id>/delete` - Delete book

### Book Management Routes
- `POST /book/<id>/mark_status` - Mark book status
- `POST /book/<id>/review` - Add review
- `POST /book/<id>/delete` - Delete own book

## 🚦 Getting Help

### Common Issues

1. **Database Error**: Run `python simple_init.py` to reinitialize
2. **Missing Dependencies**: Run `pip install -r requirements.txt`
3. **Permission Error**: Ensure write permissions in project directory
4. **Port Conflict**: Use `python start.py --port 5001` for different port

### Support
- Check the setup script output for detailed error messages
- Review the application logs in the terminal
- Ensure all dependencies are correctly installed
- Verify Python version compatibility (3.10+)

### Development Mode
```bash
# Run with debug mode
python start.py --debug

# Run on different port
python start.py --port 8080

# Run with custom host
python start.py --host 127.0.0.1
```

## 📈 Performance Features

- Efficient database queries with SQLAlchemy
- Image optimization for faster loading
- Responsive design reduces mobile data usage
- Minimal external dependencies
- Fast search with indexed database fields

## 🔮 Future Enhancements

- Email notifications for messages and wishlist matches
- Book recommendation system based on user preferences
- Integration with external book databases (Google Books API)
- Mobile app development (React Native/Flutter)
- Payment gateway integration for secure transactions
- Multi-language support (Hindi, regional languages)

## 🧪 Testing

The application includes:
- Database initialization testing
- Route accessibility testing
- Form validation testing
- File upload testing
- Authentication flow testing

Run tests:
```bash
python setup.py  # Includes basic tests
```

## 🔧 Configuration

### Environment Variables
- `FLASK_ENV`: Set to 'development' or 'production'
- `SECRET_KEY`: Flask secret key for sessions
- `DATABASE_URL`: Database connection string
- `UPLOAD_FOLDER`: Directory for uploaded files

### Default Settings
- Development server: `http://localhost:5000`
- Database: SQLite (`instance/bookswap.db`)
- Upload directory: `static/uploads/`
- Session timeout: 24 hours

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Use meaningful commit messages
- Add tests for new features
- Update documentation for API changes

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- Flask community for the excellent web framework
- Bootstrap team for the responsive design framework
- Font Awesome for the comprehensive icon library
- Indian student community for inspiration and feedback
- SQLAlchemy for the powerful ORM
- Werkzeug for security utilities

## 🌟 Key Achievements

✅ **Complete Feature Set**: All requested features implemented
✅ **Indian Context**: Tailored for Indian colleges and students
✅ **Admin Dashboard**: Full administrative control
✅ **Book Status System**: Complete transaction lifecycle
✅ **Review System**: User feedback and ratings
✅ **Responsive Design**: Works on all devices
✅ **Security**: Proper authentication and authorization
✅ **Setup Scripts**: Easy installation and deployment
✅ **Comprehensive Documentation**: Detailed user and developer guides

---

**Built with ❤️ for Indian students by students**

*Empowering education through book sharing and community collaboration*

## 📞 Contact & Support

For technical support, feature requests, or contributions:
- Create an issue in the repository
- Follow the contribution guidelines above
- Check existing documentation and FAQ

**Happy Book Swapping! 📚✨**
