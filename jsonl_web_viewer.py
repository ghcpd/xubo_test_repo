#!/usr/bin/env python3
"""
JSONL Web Viewer - A Python script to display JSONL file data via web interface.

This script provides a web interface to:
1. Load JSONL files
2. Display unique_id for each row
3. Click to view detailed information for each row
"""

import json
import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
from typing import List, Dict, Any


class JSONLWebViewer:
    def __init__(self):
        self.jsonl_data: List[Dict[str, Any]] = []
        self.current_file = None
    
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
    
    def get_html_page(self) -> str:
        """Generate HTML page"""
        # Generate unique ID items HTML
        unique_id_items = ""
        for i, record in enumerate(self.jsonl_data):
            unique_id = record.get('unique_id', f'Record_{i+1}')
            unique_id_items += f'<div class="unique-id-item" id="item-{i}" onclick="showDetails({i})">{unique_id}</div>\n'
        
        # Get data for template
        filename = os.path.basename(self.current_file) if self.current_file else "Unknown"
        record_count = len(self.jsonl_data)
        records_json = json.dumps(self.jsonl_data, indent=2)
        
        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>JSONL Viewer</title>
            <style>
                body {{ 
                    font-family: Arial, sans-serif; 
                    margin: 20px; 
                    background-color: #f5f5f5;
                }}
                .container {{ 
                    max-width: 1200px; 
                    margin: 0 auto; 
                    background: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                .header {{ 
                    border-bottom: 2px solid #007bff; 
                    padding-bottom: 10px; 
                    margin-bottom: 20px;
                }}
                .content {{ 
                    display: flex; 
                    gap: 20px; 
                }}
                .list-panel {{ 
                    flex: 1; 
                    min-width: 300px;
                }}
                .details-panel {{ 
                    flex: 2; 
                    min-width: 400px;
                }}
                .unique-id-list {{ 
                    border: 1px solid #ddd; 
                    border-radius: 4px; 
                    max-height: 600px; 
                    overflow-y: auto;
                    background: #fafafa;
                }}
                .unique-id-item {{ 
                    padding: 10px 15px; 
                    border-bottom: 1px solid #eee; 
                    cursor: pointer; 
                    transition: background-color 0.2s;
                }}
                .unique-id-item:hover {{ 
                    background-color: #e9ecef; 
                }}
                .unique-id-item.selected {{ 
                    background-color: #007bff; 
                    color: white; 
                }}
                .details-box {{ 
                    border: 1px solid #ddd; 
                    border-radius: 4px; 
                    padding: 15px; 
                    background: #f8f9fa;
                    min-height: 400px;
                }}
                .json-content {{ 
                    font-family: 'Courier New', monospace; 
                    white-space: pre-wrap; 
                    font-size: 14px; 
                    line-height: 1.4;
                    background: white;
                    padding: 15px;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                }}
                .file-info {{
                    background: #e7f3ff;
                    padding: 10px;
                    border-radius: 4px;
                    margin-bottom: 20px;
                    border-left: 4px solid #007bff;
                }}
                h1 {{ 
                    color: #007bff; 
                    margin: 0;
                }}
                h2 {{ 
                    color: #495057; 
                    margin-top: 0;
                }}
                .no-selection {{
                    color: #6c757d;
                    font-style: italic;
                    text-align: center;
                    padding: 50px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>JSONL File Viewer</h1>
                </div>
                
                <div class="file-info">
                    <strong>File:</strong> {filename} | <strong>Records:</strong> {record_count}
                </div>
                
                <div class="content">
                    <div class="list-panel">
                        <h2>Unique IDs</h2>
                        <div class="unique-id-list">
                            {unique_id_items}
                        </div>
                    </div>
                    
                    <div class="details-panel">
                        <h2>Detailed Information</h2>
                        <div class="details-box">
                            <div id="details-content" class="no-selection">
                                Select a row from the list to view detailed information.
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <script>
                const records = {records_json};
                
                function showDetails(index) {{
                    const record = records[index];
                    const detailsContent = document.getElementById('details-content');
                    
                    // Remove previous selections
                    document.querySelectorAll('.unique-id-item').forEach(item => {{
                        item.classList.remove('selected');
                    }});
                    
                    // Highlight selected item
                    document.getElementById('item-' + index).classList.add('selected');
                    
                    // Show formatted JSON
                    detailsContent.innerHTML = '<div class="json-content">' + 
                        JSON.stringify(record, null, 2) + '</div>';
                }}
            </script>
        </body>
        </html>
        """
        
        return html


class JSONLRequestHandler(BaseHTTPRequestHandler):
    viewer = None
    
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            if self.viewer and self.viewer.jsonl_data:
                html_content = self.viewer.get_html_page()
                self.wfile.write(html_content.encode())
            else:
                error_html = """
                <html><body>
                <h1>JSONL Viewer</h1>
                <p>No data loaded. Please restart the server with a valid JSONL file.</p>
                </body></html>
                """
                self.wfile.write(error_html.encode())
        else:
            self.send_error(404)
    
    def log_message(self, format, *args):
        # Suppress default logging
        return


def main():
    """Main function"""
    print("JSONL Web Viewer")
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
            print("Usage: python jsonl_web_viewer.py <file_path>")
            print("Or place a 'sample_data.jsonl' file in the same directory.")
            sys.exit(1)
    
    viewer = JSONLWebViewer()
    if not viewer.load_file(file_path):
        print("Failed to load data. Exiting.")
        sys.exit(1)
    
    # Set up the web server
    JSONLRequestHandler.viewer = viewer
    
    port = 8000
    server_address = ('localhost', port)
    httpd = HTTPServer(server_address, JSONLRequestHandler)
    
    print(f"\nWeb server starting on http://localhost:{port}")
    print("Press Ctrl+C to stop the server")
    print("-" * 40)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down the server...")
        httpd.server_close()


if __name__ == "__main__":
    main()