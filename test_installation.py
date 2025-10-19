#!/usr/bin/env python3
"""
Test script to verify Modbus TCP Client installation and dependencies.
Run this script to check if all required packages are installed correctly.
"""

import sys
import importlib

def test_imports():
    """Test if all required packages can be imported"""
    required_packages = [
        'flask',
        'pymodbus',
        'flask_cors',
        'dotenv'
    ]
    
    print("Testing package imports...")
    failed_imports = []
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✓ {package}")
        except ImportError as e:
            print(f"✗ {package} - {e}")
            failed_imports.append(package)
    
    return failed_imports

def test_modbus_client():
    """Test if ModbusClient can be instantiated"""
    try:
        from modbus_client import ModbusClient
        client = ModbusClient()
        print("✓ ModbusClient instantiation successful")
        return True
    except Exception as e:
        print(f"✗ ModbusClient instantiation failed - {e}")
        return False

def test_flask_app():
    """Test if Flask app can be created"""
    try:
        from app import app
        print("✓ Flask app creation successful")
        return True
    except Exception as e:
        print(f"✗ Flask app creation failed - {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("Modbus TCP Client Installation Test")
    print("=" * 50)
    
    print(f"Python version: {sys.version}")
    print()
    
    # Test imports
    failed_imports = test_imports()
    print()
    
    # Test ModbusClient
    modbus_ok = test_modbus_client()
    print()
    
    # Test Flask app
    flask_ok = test_flask_app()
    print()
    
    # Summary
    print("=" * 50)
    print("Test Summary:")
    print("=" * 50)
    
    if failed_imports:
        print(f"✗ Failed to import: {', '.join(failed_imports)}")
        print("  Install missing packages with: pip install -r requirements.txt")
    else:
        print("✓ All package imports successful")
    
    if modbus_ok:
        print("✓ ModbusClient module working")
    else:
        print("✗ ModbusClient module has issues")
    
    if flask_ok:
        print("✓ Flask application working")
    else:
        print("✗ Flask application has issues")
    
    if not failed_imports and modbus_ok and flask_ok:
        print()
        print("🎉 All tests passed! Your installation is ready.")
        print()
        print("To start the application, run:")
        print("  python app.py")
        print()
        print("Then open your browser to: http://localhost:5000")
    else:
        print()
        print("❌ Some tests failed. Please fix the issues above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
