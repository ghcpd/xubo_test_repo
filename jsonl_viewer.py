#!/usr/bin/env python3
"""
JSONL Viewer - A Python script to display JSONL file data with interactive viewing.

This script provides a GUI interface to:
1. Load JSONL files
2. Display unique_id for each row
3. Click to view detailed information for each row
"""

import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
from typing import List, Dict, Any


class JSONLViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("JSONL File Viewer")
        self.root.geometry("800x600")
        
        # Data storage
        self.jsonl_data: List[Dict[str, Any]] = []
        self.current_file = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weight
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # File selection frame
        file_frame = ttk.Frame(main_frame)
        file_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        file_frame.columnconfigure(1, weight=1)
        
        ttk.Button(file_frame, text="Load JSONL File", 
                  command=self.load_file).grid(row=0, column=0, padx=(0, 10))
        
        self.file_label = ttk.Label(file_frame, text="No file loaded")
        self.file_label.grid(row=0, column=1, sticky=tk.W)
        
        # List frame (left side)
        list_frame = ttk.LabelFrame(main_frame, text="Unique IDs", padding="5")
        list_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Listbox with scrollbar
        listbox_frame = ttk.Frame(list_frame)
        listbox_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        listbox_frame.columnconfigure(0, weight=1)
        listbox_frame.rowconfigure(0, weight=1)
        
        self.listbox = tk.Listbox(listbox_frame, height=20, width=30)
        scrollbar_list = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=self.listbox.yview)
        self.listbox.configure(yscrollcommand=scrollbar_list.set)
        
        self.listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar_list.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Bind selection event
        self.listbox.bind('<<ListboxSelect>>', self.on_select)
        
        # Details frame (right side)
        details_frame = ttk.LabelFrame(main_frame, text="Detailed Information", padding="5")
        details_frame.grid(row=2, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        details_frame.columnconfigure(0, weight=1)
        details_frame.rowconfigure(0, weight=1)
        
        # Text widget for details
        self.details_text = scrolledtext.ScrolledText(details_frame, 
                                                     wrap=tk.WORD, 
                                                     width=50, 
                                                     height=20,
                                                     font=('Courier', 10))
        self.details_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Initially disable the text widget
        self.details_text.insert(tk.END, "Select a row from the list to view detailed information.")
        self.details_text.config(state=tk.DISABLED)
    
    def load_file(self):
        """Load a JSONL file"""
        file_path = filedialog.askopenfilename(
            title="Select JSONL File",
            filetypes=[("JSONL files", "*.jsonl"), ("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
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
                            messagebox.showerror(
                                "JSON Error", 
                                f"Error parsing line {line_num}: {str(e)}"
                            )
                            return
            
            if not self.jsonl_data:
                messagebox.showwarning("Warning", "No valid JSON data found in the file.")
                return
            
            self.current_file = file_path
            self.file_label.config(text=f"Loaded: {os.path.basename(file_path)} ({len(self.jsonl_data)} records)")
            self.populate_list()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {str(e)}")
    
    def populate_list(self):
        """Populate the listbox with unique_id values"""
        self.listbox.delete(0, tk.END)
        
        for i, record in enumerate(self.jsonl_data):
            unique_id = record.get('unique_id', f'Record_{i+1}')
            self.listbox.insert(tk.END, unique_id)
        
        # Clear details
        self.details_text.config(state=tk.NORMAL)
        self.details_text.delete('1.0', tk.END)
        self.details_text.insert(tk.END, "Select a row from the list to view detailed information.")
        self.details_text.config(state=tk.DISABLED)
    
    def on_select(self, event):
        """Handle selection of an item in the listbox"""
        selection = self.listbox.curselection()
        if not selection:
            return
        
        index = selection[0]
        if index < len(self.jsonl_data):
            record = self.jsonl_data[index]
            self.show_details(record)
    
    def show_details(self, record: Dict[str, Any]):
        """Display detailed information for the selected record"""
        self.details_text.config(state=tk.NORMAL)
        self.details_text.delete('1.0', tk.END)
        
        # Format the JSON data nicely
        formatted_json = json.dumps(record, indent=2, ensure_ascii=False, sort_keys=True)
        self.details_text.insert(tk.END, formatted_json)
        
        self.details_text.config(state=tk.DISABLED)


def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = JSONLViewer(root)
    
    # Load sample data if it exists
    sample_file = os.path.join(os.path.dirname(__file__), 'sample_data.jsonl')
    if os.path.exists(sample_file):
        try:
            with open(sample_file, 'r', encoding='utf-8') as file:
                app.jsonl_data = []
                for line in file:
                    line = line.strip()
                    if line:
                        app.jsonl_data.append(json.loads(line))
                
                if app.jsonl_data:
                    app.current_file = sample_file
                    app.file_label.config(text=f"Loaded: sample_data.jsonl ({len(app.jsonl_data)} records)")
                    app.populate_list()
        except Exception:
            pass  # If sample data can't be loaded, just continue without it
    
    root.mainloop()


if __name__ == "__main__":
    main()