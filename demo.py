#!/usr/bin/env python3
"""
Demo script for JSONL viewers

This script demonstrates all three JSONL viewer interfaces:
1. CLI viewer
2. Web viewer  
3. GUI viewer (if tkinter is available)
"""

import os
import sys
import subprocess
import time

def main():
    """Run demonstrations of all JSONL viewers"""
    print("🎯 JSONL Viewer Demo")
    print("=" * 40)
    
    # Check if sample data exists
    sample_file = 'sample_data.jsonl'
    if not os.path.exists(sample_file):
        print("❌ Sample data not found. Please run this script from the repository directory.")
        sys.exit(1)
    
    print(f"📁 Using sample file: {sample_file}")
    
    # Show available viewers
    print("\n🔧 Available JSONL Viewers:")
    print("1. CLI Viewer (jsonl_cli_viewer.py) - Command line interactive interface")
    print("2. Web Viewer (jsonl_web_viewer.py) - Browser-based interface")
    print("3. GUI Viewer (jsonl_viewer.py) - Desktop GUI interface (requires tkinter)")
    
    print("\n" + "=" * 40)
    print("Choose a demo:")
    print("1 - CLI Viewer Demo")
    print("2 - Web Viewer Demo (starts server)")
    print("3 - GUI Viewer Demo") 
    print("4 - Show sample data")
    print("q - Quit")
    
    while True:
        choice = input("\nEnter your choice (1-4 or q): ").strip().lower()
        
        if choice == 'q':
            print("👋 Goodbye!")
            break
        elif choice == '1':
            print("\n🚀 Starting CLI Viewer...")
            print("Note: This will start an interactive session. Type 'q' to quit when done.")
            input("Press Enter to continue...")
            subprocess.call([sys.executable, 'jsonl_cli_viewer.py', sample_file])
        elif choice == '2':
            print("\n🚀 Starting Web Viewer...")
            print("The web server will start on http://localhost:8000")
            print("Press Ctrl+C in the terminal to stop the server.")
            input("Press Enter to continue...")
            try:
                subprocess.call([sys.executable, 'jsonl_web_viewer.py', sample_file])
            except KeyboardInterrupt:
                print("\n🛑 Web server stopped.")
        elif choice == '3':
            print("\n🚀 Starting GUI Viewer...")
            try:
                import tkinter
                subprocess.call([sys.executable, 'jsonl_viewer.py'])
            except ImportError:
                print("❌ Tkinter not available. GUI viewer cannot run in this environment.")
                print("💡 Try the CLI or Web viewer instead.")
        elif choice == '4':
            print("\n📄 Sample Data Preview:")
            print("-" * 60)
            with open(sample_file, 'r') as f:
                for i, line in enumerate(f, 1):
                    print(f"{i}. {line.strip()}")
            print("-" * 60)
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()