#!/usr/bin/env python3
"""
BookSwapBuddy Start Script
=========================

This script starts the BookSwapBuddy application with appropriate configurations
for different environments.

Usage:
    python start.py [options]

Options:
    --port PORT       Port to run the application on (default: 5000)
    --host HOST       Host to bind to (default: 127.0.0.1)
    --debug           Run in debug mode
    --production      Run in production mode
    --help            Show this help message
"""

import os
import sys
import argparse
import subprocess
from datetime import datetime

class BookSwapBuddyRunner:
    def __init__(self):
        self.project_dir = os.path.dirname(os.path.abspath(__file__))
        self.app_file = os.path.join(self.project_dir, "app.py")
        
    def print_banner(self):
        """Print the application banner."""
        print("""
╔══════════════════════════════════════════════════════════════════════════════════╗
║                           BookSwapBuddy Server                                  ║
║                    Student Book Exchange Platform                               ║
╚══════════════════════════════════════════════════════════════════════════════════╝
""")
    
    def check_requirements(self):
        """Check if all requirements are met."""
        print("🔍 Checking requirements...")
        
        # Check if app.py exists
        if not os.path.exists(self.app_file):
            print("❌ app.py not found!")
            print("Please make sure you're in the BookSwapBuddy directory")
            return False
        
        # Check if database exists
        db_path = os.path.join(self.project_dir, "instance", "bookswap.db")
        if not os.path.exists(db_path):
            print("⚠️  Database not found!")
            print("Run 'python setup.py' to initialize the database")
            response = input("Do you want to initialize the database now? (y/n): ")
            if response.lower() == 'y':
                print("Initializing database...")
                try:
                    subprocess.run([sys.executable, "setup.py"], check=True)
                    print("✅ Database initialized")
                except subprocess.CalledProcessError:
                    print("❌ Failed to initialize database")
                    return False
            else:
                print("❌ Cannot start without database")
                return False
        
        # Check if uploads directory exists
        uploads_path = os.path.join(self.project_dir, "static", "uploads")
        if not os.path.exists(uploads_path):
            os.makedirs(uploads_path)
            print("✅ Created uploads directory")
        
        print("✅ All requirements met")
        return True
    
    def get_server_info(self, host, port, debug):
        """Get server configuration information."""
        return {
            'host': host,
            'port': port,
            'debug': debug,
            'url': f"http://{host}:{port}",
            'local_url': f"http://localhost:{port}" if host != 'localhost' else f"http://localhost:{port}"
        }
    
    def print_server_info(self, info):
        """Print server information."""
        print(f"""
🚀 Starting BookSwapBuddy Server
═══════════════════════════════

📍 Host: {info['host']}
🔢 Port: {info['port']}
🔧 Debug: {'Enabled' if info['debug'] else 'Disabled'}
🌐 URL: {info['url']}

📋 Available at:
   • Local: {info['local_url']}
   • Network: {info['url']}

⭐ Features Available:
   • Book Exchange Platform
   • User Authentication
   • Advanced Search & Filters  
   • Messaging System
   • Wishlist & Reviews
   • Admin Dashboard
   • Analytics & Reports

🔐 Default Accounts:
   Admin: admin / admin123
   User: alice_smith / password123

📖 Documentation: README.md
🆘 Support: Check troubleshooting in README.md

═══════════════════════════════
Press Ctrl+C to stop the server
═══════════════════════════════
""")
    
    def start_application(self, host='127.0.0.1', port=5000, debug=False, production=False):
        """Start the Flask application."""
        
        # Set environment variables
        os.environ['FLASK_APP'] = 'app.py'
        if debug and not production:
            os.environ['FLASK_ENV'] = 'development'
            os.environ['FLASK_DEBUG'] = '1'
        else:
            os.environ['FLASK_ENV'] = 'production'
            os.environ['FLASK_DEBUG'] = '0'
        
        # Get server info
        server_info = self.get_server_info(host, port, debug and not production)
        
        # Print server information
        self.print_server_info(server_info)
        
        try:
            # Import and run the app
            sys.path.insert(0, self.project_dir)
            from app import app, db
            
            # Ensure database tables exist
            with app.app_context():
                db.create_all()
            
            # Start the server
            app.run(
                host=host,
                port=port,
                debug=debug and not production,
                threaded=True
            )
            
        except ImportError as e:
            print(f"❌ Failed to import application: {e}")
            print("Make sure all dependencies are installed:")
            print("   python -m pip install -r requirements.txt")
            sys.exit(1)
        except KeyboardInterrupt:
            print("\n\n👋 BookSwapBuddy server stopped by user")
            print("Thank you for using BookSwapBuddy!")
        except Exception as e:
            print(f"❌ Server error: {e}")
            sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Start BookSwapBuddy application server")
    parser.add_argument('--port', type=int, default=5000,
                       help='Port to run the application on (default: 5000)')
    parser.add_argument('--host', default='127.0.0.1',
                       help='Host to bind to (default: 127.0.0.1)')
    parser.add_argument('--debug', action='store_true',
                       help='Run in debug mode')
    parser.add_argument('--production', action='store_true',
                       help='Run in production mode (overrides debug)')
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.production and args.debug:
        print("⚠️  Production mode overrides debug mode")
        args.debug = False
    
    runner = BookSwapBuddyRunner()
    runner.print_banner()
    
    # Check requirements before starting
    if not runner.check_requirements():
        sys.exit(1)
    
    # Start the application
    runner.start_application(
        host=args.host,
        port=args.port,
        debug=args.debug,
        production=args.production
    )

if __name__ == "__main__":
    main()
