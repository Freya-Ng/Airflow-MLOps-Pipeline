#!/usr/bin/env python3
"""
Cleanup script for Airflow ML Pipeline.
Removes generated files, logs, and temporary data.
"""

import os
import shutil


def clean_logs():
    """Clean log files."""
    log_dir = './logs'
    if os.path.exists(log_dir):
        for item in os.listdir(log_dir):
            if item != '.gitkeep':
                path = os.path.join(log_dir, item)
                try:
                    if os.path.isdir(path):
                        shutil.rmtree(path)
                    else:
                        os.remove(path)
                    print(f"✓ Removed: {path}")
                except Exception as e:
                    print(f"✗ Failed to remove {path}: {e}")


def clean_data():
    """Clean generated data files (keep directory structure)."""
    data_dirs = ['./data/raw', './data/processed', './data/model']
    
    for data_dir in data_dirs:
        if os.path.exists(data_dir):
            for item in os.listdir(data_dir):
                if item != '.gitkeep':
                    path = os.path.join(data_dir, item)
                    try:
                        if os.path.isfile(path):
                            os.remove(path)
                            print(f"✓ Removed: {path}")
                    except Exception as e:
                        print(f"✗ Failed to remove {path}: {e}")


def clean_cache():
    """Clean Python cache files."""
    for root, dirs, files in os.walk('.'):
        # Remove __pycache__ directories
        if '__pycache__' in dirs:
            cache_path = os.path.join(root, '__pycache__')
            try:
                shutil.rmtree(cache_path)
                print(f"✓ Removed: {cache_path}")
            except Exception as e:
                print(f"✗ Failed to remove {cache_path}: {e}")
        
        # Remove .pyc files
        for file in files:
            if file.endswith('.pyc'):
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    print(f"✓ Removed: {file_path}")
                except Exception as e:
                    print(f"✗ Failed to remove {file_path}: {e}")


def main():
    """Main cleanup function."""
    print("=" * 60)
    print("Airflow ML Pipeline - Cleanup")
    print("=" * 60)
    
    print("\n1. Cleaning logs...")
    clean_logs()
    
    print("\n2. Cleaning data files...")
    clean_data()
    
    print("\n3. Cleaning cache...")
    clean_cache()
    
    print("\n" + "=" * 60)
    print("Cleanup completed!")
    print("=" * 60)


if __name__ == '__main__':
    main()
