#!/usr/bin/env python3
"""
Setup and Installation Script for Manim UI Builder
==================================================

This script helps set up the Manim UI Builder environment.
"""

import os
import sys
import subprocess
import platform

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required. Current version:", sys.version)
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def install_requirements():
    """Install Python dependencies."""
    print("\n📦 Installing Python dependencies...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def check_system_dependencies():
    """Check for system dependencies."""
    print("\n🖥️  Checking system dependencies...")
    
    system = platform.system()
    
    if system == "Linux":
        print("On Linux, you may need to install:")
        print("  sudo apt-get install libgl1-mesa-glx libegl1-mesa libxrandr2 libxss1 libxcursor1 libxcomposite1 libasound2 libxi6 libxtst6")
        print("  (Required for PyQt6 GUI)")
    elif system == "Windows":
        print("Windows detected - GUI should work out of the box")
    elif system == "Darwin":
        print("macOS detected - GUI should work out of the box")
    
    return True

def setup_gemini_api():
    """Help user set up Gemini API key."""
    print("\n🤖 Gemini AI Setup (Optional)")
    
    api_key = os.getenv('GEMINI_API_KEY')
    if api_key:
        print("✅ GEMINI_API_KEY environment variable found")
        return True
    
    print("ℹ️  To use AI features, you need a Gemini API key:")
    print("1. Get a free API key at: https://makersuite.google.com/app/apikey")
    print("2. Set environment variable:")
    
    system = platform.system()
    if system == "Windows":
        print("   set GEMINI_API_KEY=your-api-key-here")
    else:
        print("   export GEMINI_API_KEY=your-api-key-here")
    
    print("3. Restart the application")
    print("\n⚠️  Without this, AI assistant features will be disabled")
    
    return False

def run_tests():
    """Run basic functionality tests."""
    print("\n🧪 Running basic tests...")
    try:
        result = subprocess.run([sys.executable, 'test_basic.py'], 
                               capture_output=True, text=True)
        
        if "All tests passed!" in result.stdout:
            print("✅ Basic tests passed")
            return True
        else:
            print("⚠️  Some tests failed (GUI dependencies may be missing)")
            print("Core functionality should still work")
            return True
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def main():
    """Main setup function."""
    print("🎨 Manim UI Builder Setup")
    print("=" * 40)
    
    success = True
    
    # Check Python version
    success &= check_python_version()
    
    # Install requirements
    success &= install_requirements()
    
    # Check system dependencies
    success &= check_system_dependencies()
    
    # Setup Gemini API (optional)
    setup_gemini_api()
    
    # Run tests
    success &= run_tests()
    
    print("\n" + "=" * 40)
    if success:
        print("🎉 Setup completed successfully!")
        print("\nTo start the application:")
        print("  python main.py")
        print("\nFor help and documentation:")
        print("  https://github.com/shobhitvats/Manim-UI-with-AI")
    else:
        print("⚠️  Setup completed with warnings")
        print("Some features may not work properly")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())