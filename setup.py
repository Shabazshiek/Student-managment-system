#!/usr/bin/env python
"""
EduTrack SMS — One-click setup script
Run this file to set up the entire project automatically.
Usage: python setup.py
"""
import os
import sys
import subprocess


def run(cmd, cwd=None):
    print(f"  → {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd)
    if result.returncode != 0:
        print(f"  ❌ Command failed: {cmd}")
        sys.exit(1)


def main():
    base = os.path.dirname(os.path.abspath(__file__))
    print("\n🎓 EduTrack Student Management System — Setup\n" + "="*50)

    # Check Python
    version = sys.version_info
    if version.major < 3 or version.minor < 8:
        print("❌ Python 3.8+ is required.")
        sys.exit(1)
    print(f"✓ Python {version.major}.{version.minor} detected")

    # Install requirements
    print("\n📦 Installing requirements...")
    run(f"{sys.executable} -m pip install -r requirements.txt", cwd=base)
    print("✓ Requirements installed")

    # Migrations
    print("\n🗄️  Setting up database...")
    run(f"{sys.executable} manage.py makemigrations", cwd=base)
    run(f"{sys.executable} manage.py migrate", cwd=base)
    print("✓ Database ready")

    # Seed data
    print("\n🌱 Loading sample data...")
    run(f"{sys.executable} manage.py seed_data", cwd=base)

    # Collect static
    print("\n📁 Collecting static files...")
    run(f"{sys.executable} manage.py collectstatic --noinput", cwd=base)

    print("\n" + "="*50)
    print("✅ Setup complete! Run the server with:")
    print("   python manage.py runserver")
    print("\n🌐 Open: http://127.0.0.1:8000/")
    print("🔑 Login: admin / admin123")
    print("="*50 + "\n")


if __name__ == '__main__':
    main()
