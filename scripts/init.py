#!/usr/bin/env python3
"""
Initialization script for Airflow ML Pipeline.
Sets up directories, checks dependencies, and initializes configurations.
"""

import os
import sys


def create_directories():
    """Create necessary directories if they don't exist."""
    directories = [
        './data/raw',
        './data/processed',
        './data/model',
        './logs',
        './plugins',
        './config'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created directory: {directory}")


def check_dependencies():
    """Check if required dependencies are installed."""
    required_packages = ['airflow', 'pandas', 'sklearn']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package} is installed")
        except ImportError:
            missing_packages.append(package)
            print(f"✗ {package} is NOT installed")
    
    if missing_packages:
        print(f"\nPlease install missing packages: pip install {' '.join(missing_packages)}")
        return False
    return True


def main():
    """Main initialization function."""
    print("=" * 60)
    print("Airflow ML Pipeline - Initialization")
    print("=" * 60)
    
    print("\n1. Creating directories...")
    create_directories()
    
    print("\n2. Checking dependencies...")
    if not check_dependencies():
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("Initialization completed successfully!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Copy .env.example to .env and configure")
    print("2. Run: docker-compose up airflow-init")
    print("3. Run: docker-compose up -d")
    print("4. Access UI at http://localhost:8080")


if __name__ == '__main__':
    main()
