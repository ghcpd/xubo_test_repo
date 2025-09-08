#!/usr/bin/env python3
"""
JSONL CLI Viewer - A command-line Python script to display JSONL file data.

This script provides a CLI interface to:
1. Load JSONL files
2. Display unique_id for each row
3. Allow selection to view detailed information for each row
"""

import json
import os
import sys
from typing import List, Dict, Any


class JSONLCLIViewer:
    def __init__(self, file_path: str = None):
        self.jsonl_data: List[Dict[str, Any]] = []
        self.current_file = file_path
        
        if file_path:
            self.load_file(file_path)
    
    def load_file(self, file_path: str) -> bool:
        """Load a JSONL file"""
        try:
            self.jsonl_data = []
            with open(file_path, 'r', encoding='utf-8') as file:
                for line_num, line in enumerate(file, 1):
                    line = line.strip()
                    if line:  # Skip empty lines
                        try:
                            data = json.loads(line)
                            self.jsonl_data.append(data)
                        except json.JSONDecodeError as e:
                            print(f"Error parsing line {line_num}: {str(e)}")
                            return False
            
            if not self.jsonl_data:
                print("No valid JSON data found in the file.")
                return False
            
            self.current_file = file_path
            print(f"Loaded: {os.path.basename(file_path)} ({len(self.jsonl_data)} records)")
            return True
            
        except Exception as e:
            print(f"Failed to load file: {str(e)}")
            return False
    
    def display_unique_ids(self):
        """Display all unique_id values with index numbers"""
        if not self.jsonl_data:
            print("No data loaded. Please load a JSONL file first.")
            return
        
        print(f"\nUnique IDs from {os.path.basename(self.current_file) if self.current_file else 'loaded data'}:")
        print("-" * 50)
        
        for i, record in enumerate(self.jsonl_data):
            unique_id = record.get('unique_id', f'Record_{i+1}')
            print(f"{i+1:3d}. {unique_id}")
    
    def show_details(self, index: int):
        """Display detailed information for a specific record"""
        if not self.jsonl_data:
            print("No data loaded.")
            return
        
        if index < 1 or index > len(self.jsonl_data):
            print(f"Invalid selection. Please choose a number between 1 and {len(self.jsonl_data)}.")
            return
        
        record = self.jsonl_data[index - 1]
        unique_id = record.get('unique_id', f'Record_{index}')
        
        print(f"\nDetailed information for: {unique_id}")
        print("=" * 60)
        print(json.dumps(record, indent=2, ensure_ascii=False, sort_keys=True))
        print("=" * 60)
    
    def interactive_mode(self):
        """Run in interactive mode"""
        if not self.jsonl_data:
            print("No data available for interactive mode.")
            return
        
        while True:
            self.display_unique_ids()
            print(f"\nOptions:")
            print(f"  Enter a number (1-{len(self.jsonl_data)}) to view details")
            print(f"  Enter 'q' or 'quit' to exit")
            print(f"  Enter 'list' to show the list again")
            
            try:
                user_input = input(f"\nYour choice: ").strip().lower()
                
                if user_input in ['q', 'quit']:
                    print("Goodbye!")
                    break
                elif user_input == 'list':
                    continue
                elif user_input.isdigit():
                    index = int(user_input)
                    self.show_details(index)
                    
                    # Ask if user wants to continue
                    continue_input = input(f"\nPress Enter to continue or 'q' to quit: ").strip().lower()
                    if continue_input in ['q', 'quit']:
                        print("Goodbye!")
                        break
                else:
                    print(f"Invalid input. Please try again.")
                    
            except KeyboardInterrupt:
                print(f"\nGoodbye!")
                break
            except Exception as e:
                print(f"An error occurred: {str(e)}")


def main():
    """Main function"""
    print("JSONL CLI Viewer")
    print("================")
    
    # Check for command line arguments
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        if not os.path.exists(file_path):
            print(f"Error: File '{file_path}' not found.")
            sys.exit(1)
    else:
        # Try to use sample data if available
        sample_file = os.path.join(os.path.dirname(__file__), 'sample_data.jsonl')
        if os.path.exists(sample_file):
            file_path = sample_file
            print(f"Using sample data file: {sample_file}")
        else:
            print("Usage: python jsonl_cli_viewer.py <file_path>")
            print("Or place a 'sample_data.jsonl' file in the same directory.")
            sys.exit(1)
    
    viewer = JSONLCLIViewer(file_path)
    if viewer.jsonl_data:
        viewer.interactive_mode()
    else:
        print("Failed to load data. Exiting.")
        sys.exit(1)


if __name__ == "__main__":
    main()