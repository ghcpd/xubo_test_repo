# JSONL Viewer

A Python application to display JSONL (JSON Lines) file data with interactive viewing capabilities. This tool provides multiple interfaces to view your JSONL data: command-line, web-based, and GUI (when tkinter is available).

## Features

- **Multiple Interfaces**: CLI, Web, and GUI options
- **Interactive Viewing**: Display unique_id for each row and click/select to view detailed information
- **JSONL Support**: Parse and display JSON Lines format files
- **Sample Data**: Includes sample data for testing
- **Error Handling**: Robust error handling for malformed JSON and missing files

## Files

- `demo.py` - Interactive demo script to try all viewers
- `jsonl_cli_viewer.py` - Command-line interface viewer
- `jsonl_web_viewer.py` - Web-based interface viewer
- `jsonl_viewer.py` - GUI interface viewer (requires tkinter)
- `sample_data.jsonl` - Sample JSONL data file for testing

## Quick Start

To get started quickly, use the demo script:

```bash
python3 demo.py
```

This interactive demo will let you try all three interfaces and view the sample data.

## Usage

### Command Line Interface

```bash
# Use with a specific file
python3 jsonl_cli_viewer.py your_file.jsonl

# Use with sample data (if available in the same directory)
python3 jsonl_cli_viewer.py
```

The CLI version provides an interactive menu where you can:
1. View all unique_id values with index numbers
2. Enter a number to view detailed information for that record
3. Type 'q' or 'quit' to exit

### Web Interface

```bash
# Start web server with a specific file
python3 jsonl_web_viewer.py your_file.jsonl

# Start web server with sample data
python3 jsonl_web_viewer.py
```

Then open your browser to `http://localhost:8000` to view the interactive web interface.

The web interface provides:
- A list of unique_id values on the left
- Click any unique_id to view detailed JSON information on the right
- Responsive design that works on different screen sizes

### GUI Interface (if tkinter is available)

```bash
python3 jsonl_viewer.py
```

The GUI provides:
- File browser to select JSONL files
- List view of unique_id values
- Detailed information panel
- Built-in sample data loading

## JSONL File Format

The viewers expect JSONL files where each line contains a valid JSON object. For best results, ensure each JSON object has a `unique_id` field:

```json
{"unique_id": "user_001", "name": "Alice Johnson", "age": 28, "occupation": "Software Engineer"}
{"unique_id": "user_002", "name": "Bob Smith", "age": 35, "occupation": "Data Scientist"}
```

If no `unique_id` field is present, the viewers will generate identifiers like `Record_1`, `Record_2`, etc.

## Sample Data

The included `sample_data.jsonl` contains 5 sample user records with the following fields:
- unique_id
- name
- age
- occupation
- location
- email

## Error Handling

All viewers include error handling for:
- Missing files
- Invalid JSON syntax
- Empty files
- Missing unique_id fields

## Requirements

- Python 3.6+
- Standard library modules only (no external dependencies)
- Optional: tkinter for GUI version (usually included with Python)

## Examples

### Example 1: Quick Start with Sample Data
```bash
python3 jsonl_cli_viewer.py
```

### Example 2: Web Viewer
```bash
python3 jsonl_web_viewer.py sample_data.jsonl
# Then open http://localhost:8000 in your browser
```

### Example 3: Custom JSONL File
```bash
python3 jsonl_cli_viewer.py /path/to/your/data.jsonl
```