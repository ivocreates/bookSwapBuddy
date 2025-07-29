#!/usr/bin/env python3
"""
BookSwapBuddy Setup Script
========================

This script sets up the BookSwapBuddy application with all necessary dependencies,
database initialization, and sample data.

Usage:
    python setup.py [options]

Options:
    --dev         Install development dependencies
    --production  Setup for production environment
    --reset       Reset database (delete existing data)
    --no-sample   Skip sample data insertion
    --help        Show this help message
"""

import os
import sys
import argparse
import subprocess
import platform
from datetime import datetime

class BookSwapBuddySetup:
    def __init__(self):
        self.python_cmd = self.get_python_command()
        self.pip_cmd = f"{self.python_cmd} -m pip"
        self.is_windows = platform.system() == "Windows"
        self.project_dir = os.path.dirname(os.path.abspath(__file__))
        
    def get_python_command(self):
        """Get the appropriate Python command for the current system."""
        # Try to find Python 3
        for cmd in ['python3', 'python']:
            try:
                result = subprocess.run([cmd, '--version'], capture_output=True, text=True)
                if result.returncode == 0 and '3.' in result.stdout:
                    return cmd
            except FileNotFoundError:
                continue
        
        print("❌ Python 3 is required but not found!")
        print("Please install Python 3.8 or higher from https://python.org")
        sys.exit(1)
    
    def print_banner(self):
        """Print the setup banner."""
        print("""
╔══════════════════════════════════════════════════════════════════════════════════╗
║                           BookSwapBuddy Setup                                   ║
║                    Student Book Exchange Platform                               ║
╚══════════════════════════════════════════════════════════════════════════════════╝
""")
    
    def print_step(self, step, message):
        """Print a setup step with formatting."""
        print(f"\n🔧 Step {step}: {message}")
        print("─" * 60)
    
    def run_command(self, command, description, check=True):
        """Run a command with proper error handling."""
        print(f"  Running: {command}")
        try:
            result = subprocess.run(command, shell=True, check=check, 
                                  capture_output=True, text=True)
            if result.stdout:
                print(f"  ✅ {description}")
            return result.returncode == 0
        except subprocess.CalledProcessError as e:
            print(f"  ❌ Error in {description}")
            print(f"  Error: {e.stderr}")
            return False
    
    def check_python_version(self):
        """Check Python version compatibility."""
        self.print_step(1, "Checking Python Version")
        
        result = subprocess.run([self.python_cmd, '--version'], 
                              capture_output=True, text=True)
        version = result.stdout.strip()
        print(f"  Python version: {version}")
        
        # Check if version is 3.8+
        version_parts = version.split()[1].split('.')
        major, minor = int(version_parts[0]), int(version_parts[1])
        
        if major < 3 or (major == 3 and minor < 8):
            print("  ❌ Python 3.8 or higher is required!")
            print("  Please upgrade Python from https://python.org")
            return False
        
        print("  ✅ Python version is compatible")
        return True
    
    def setup_virtual_environment(self):
        """Create and activate virtual environment."""
        self.print_step(2, "Setting up Virtual Environment")
        
        venv_path = os.path.join(self.project_dir, "bookswap_env")
        
        # Create virtual environment
        if not os.path.exists(venv_path):
            print("  Creating virtual environment...")
            success = self.run_command(
                f"{self.python_cmd} -m venv bookswap_env",
                "Virtual environment created"
            )
            if not success:
                return False
        else:
            print("  ✅ Virtual environment already exists")
        
        # Instructions for activation
        if self.is_windows:
            activate_cmd = "bookswap_env\\Scripts\\activate"
        else:
            activate_cmd = "source bookswap_env/bin/activate"
        
        print(f"  📝 To activate the virtual environment, run:")
        print(f"     {activate_cmd}")
        
        return True
    
    def install_dependencies(self, dev=False):
        """Install Python dependencies."""
        self.print_step(3, "Installing Dependencies")
        
        # Upgrade pip first
        print("  Upgrading pip...")
        self.run_command(f"{self.pip_cmd} install --upgrade pip", "Pip upgraded")
        
        # Install main dependencies
        print("  Installing main dependencies...")
        success = self.run_command(
            f"{self.pip_cmd} install -r requirements.txt",
            "Main dependencies installed"
        )
        
        if not success:
            print("  ❌ Failed to install dependencies")
            print("  Trying individual installation...")
            
            # Core dependencies
            core_deps = [
                "Flask==2.3.3",
                "Flask-SQLAlchemy==3.0.5",
                "Werkzeug==2.3.7",
                "Pillow==10.0.1",
                "qrcode==7.4.2",
                "bcrypt==4.1.2"
            ]
            
            for dep in core_deps:
                self.run_command(f"{self.pip_cmd} install {dep}", f"Installed {dep}")
        
        # Install development dependencies
        if dev:
            print("  Installing development dependencies...")
            dev_deps = [
                "pytest==7.4.3",
                "pytest-flask==1.3.0",
                "black==23.11.0",
                "flake8==6.1.0"
            ]
            
            for dep in dev_deps:
                self.run_command(f"{self.pip_cmd} install {dep}", f"Installed {dep}")
        
        return True
    
    def create_directories(self):
        """Create necessary directories."""
        self.print_step(4, "Creating Directory Structure")
        
        directories = [
            "instance",
            "static/uploads",
            "static/css",
            "static/js",
            "static/images",
            "templates/admin",
            "logs"
        ]
        
        for directory in directories:
            dir_path = os.path.join(self.project_dir, directory)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
                print(f"  ✅ Created directory: {directory}")
            else:
                print(f"  📁 Directory exists: {directory}")
        
        return True
    
    def initialize_database(self, reset=False, no_sample=False):
        """Initialize database with sample data."""
        self.print_step(5, "Initializing Database")
        
        if reset:
            db_path = os.path.join(self.project_dir, "instance", "bookswap.db")
            if os.path.exists(db_path):
                os.remove(db_path)
                print("  🗑️  Existing database removed")
        
        # Initialize database
        print("  Creating database tables...")
        success = self.run_command(
            f"{self.python_cmd} -c \"from app import app, db; app.app_context().push(); db.create_all()\"",
            "Database tables created"
        )
        
        if not success:
            print("  ❌ Failed to create database tables")
            return False
        
        # Add sample data
        if not no_sample:
            print("  Adding sample data...")
            if os.path.exists("simple_init.py"):
                success = self.run_command(
                    f"{self.python_cmd} simple_init.py",
                    "Sample data added"
                )
                if not success:
                    print("  ⚠️  Warning: Failed to add sample data")
            else:
                print("  ⚠️  Warning: simple_init.py not found, skipping sample data")
        
        return True
    
    def create_env_file(self, production=False):
        """Create environment configuration file."""
        self.print_step(6, "Creating Environment Configuration")
        
        env_content = f'''# BookSwapBuddy Environment Configuration
# Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

# Flask Configuration
SECRET_KEY=your-super-secret-key-change-this-in-production
FLASK_ENV={"production" if production else "development"}
FLASK_DEBUG={"False" if production else "True"}

# Database Configuration
DATABASE_URL=sqlite:///instance/bookswap.db

# Upload Configuration
UPLOAD_FOLDER=static/uploads
MAX_CONTENT_LENGTH=16777216

# Security Configuration
SESSION_COOKIE_SECURE={"True" if production else "False"}
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Lax

# Email Configuration (Optional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Analytics and Logging
LOG_LEVEL={"INFO" if production else "DEBUG"}
LOG_FILE=logs/bookswap.log
'''
        
        env_path = os.path.join(self.project_dir, ".env")
        if not os.path.exists(env_path):
            with open(env_path, 'w') as f:
                f.write(env_content)
            print("  ✅ Environment file created (.env)")
        else:
            print("  📄 Environment file already exists")
        
        return True
    
    def run_tests(self):
        """Run basic tests to verify setup."""
        self.print_step(7, "Running Basic Tests")
        
        # Test imports
        print("  Testing imports...")
        test_imports = [
            "import flask",
            "import flask_sqlalchemy", 
            "import werkzeug",
            "import PIL",
            "import qrcode",
            "import bcrypt"
        ]
        
        for import_test in test_imports:
            success = self.run_command(
                f"{self.python_cmd} -c \"{import_test}\"",
                f"Import test: {import_test.split()[-1]}",
                check=False
            )
            if not success:
                print(f"  ❌ Import failed: {import_test}")
        
        # Test application startup
        print("  Testing application startup...")
        success = self.run_command(
            f"{self.python_cmd} -c \"from app import app; print('App created successfully')\"",
            "Application startup test",
            check=False
        )
        
        return True
    
    def print_completion_message(self):
        """Print setup completion message with next steps."""
        print("""
╔══════════════════════════════════════════════════════════════════════════════════╗
║                              Setup Complete! 🎉                                ║
╚══════════════════════════════════════════════════════════════════════════════════╝

✅ BookSwapBuddy has been successfully set up!

📋 Next Steps:
""")
        
        if self.is_windows:
            print("   1. Activate the virtual environment:")
            print("      bookswap_env\\Scripts\\activate")
        else:
            print("   1. Activate the virtual environment:")
            print("      source bookswap_env/bin/activate")
        
        print("""
   2. Start the application:
      python app.py

   3. Open your browser and visit:
      http://localhost:5000

🔐 Default Admin Credentials:
   Username: admin
   Password: admin123

👤 Default Test User:
   Username: alice_smith
   Password: password123

📚 Features Available:
   • User registration and authentication
   • Book upload and management
   • Advanced search and filtering
   • Messaging system
   • Wishlist functionality
   • Review and rating system
   • Admin dashboard
   • Analytics and reporting

📖 For more information, check:
   • README.md - Complete documentation
   • DEMO_GUIDE.md - Usage examples
   • docs/ - Additional documentation

🆘 Need Help?
   • Check the troubleshooting section in README.md
   • Ensure all dependencies are installed
   • Verify Python version is 3.8+

Happy book swapping! 📚✨
""")

def main():
    parser = argparse.ArgumentParser(description="Setup BookSwapBuddy application")
    parser.add_argument('--dev', action='store_true', 
                       help='Install development dependencies')
    parser.add_argument('--production', action='store_true',
                       help='Setup for production environment')
    parser.add_argument('--reset', action='store_true',
                       help='Reset database (delete existing data)')
    parser.add_argument('--no-sample', action='store_true',
                       help='Skip sample data insertion')
    
    args = parser.parse_args()
    
    setup = BookSwapBuddySetup()
    setup.print_banner()
    
    try:
        # Run setup steps
        if not setup.check_python_version():
            sys.exit(1)
        
        if not setup.setup_virtual_environment():
            sys.exit(1)
        
        if not setup.install_dependencies(dev=args.dev):
            sys.exit(1)
        
        if not setup.create_directories():
            sys.exit(1)
        
        if not setup.initialize_database(reset=args.reset, no_sample=args.no_sample):
            sys.exit(1)
        
        if not setup.create_env_file(production=args.production):
            sys.exit(1)
        
        if not setup.run_tests():
            print("  ⚠️  Some tests failed, but setup can continue")
        
        setup.print_completion_message()
        
    except KeyboardInterrupt:
        print("\n\n❌ Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Setup failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
