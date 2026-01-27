# XML Sitemap URL Extractor

A lightweight tool to extract HTML page URLs from XML sitemaps, available as both a command-line tool and a web application. Built with Python and Streamlit, featuring a modern Botpresso design system.

## 📋 Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Project](#running-the-project)
- [Usage Guide](#usage-guide)
- [Project Structure](#project-structure)
- [Output Format](#output-format)
- [Supported File Types](#supported-file-types)
- [Troubleshooting](#troubleshooting)
- [Requirements](#requirements)

## ✨ Features

- ✅ **Recursive Processing**: Automatically follows nested sitemap indexes
- ✅ **HTML Filtering**: Extracts only HTML pages (filters out images, PDFs, videos, etc.)
- ✅ **Duplicate Prevention**: Automatically removes duplicate URLs
- ✅ **Error Handling**: Robust retry logic and timeout handling
- ✅ **Progress Tracking**: Real-time progress updates (web UI)
- ✅ **CSV Export**: Clean CSV output with single URL column
- ✅ **Modern UI**: Beautiful web interface with Botpresso design system
- ✅ **Pagination**: Efficient pagination for large result sets
- ✅ **Statistics Dashboard**: View extraction statistics and metrics

## 🔧 Prerequisites

Before running this project, ensure you have the following installed:

- **Python 3.7 or higher** (Python 3.8+ recommended)
- **pip** (Python package installer) or **bun** (JavaScript runtime and package manager)
- **Internet connection** (for downloading dependencies and accessing sitemaps)

### Checking Your Python Version

To check if Python is installed and verify the version:

```bash
python --version
```

Or on some systems:

```bash
python3 --version
```

If Python is not installed, download it from [python.org](https://www.python.org/downloads/).

## 📦 Installation

### Step 1: Clone or Download the Project

If you have the project files, navigate to the project directory:

```bash
cd "e:\Indexing Insight\New folder"
```

### Step 2: Install Dependencies

You can install dependencies using either **pip** (recommended) or **bun**:

#### Option A: Using pip (Recommended)

```bash
pip install -r requirements.txt
```

Or if you have multiple Python versions:

```bash
pip3 install -r requirements.txt
```

#### Option B: Using bun

If you prefer using bun:

```bash
bun install
```

**Note:** If you encounter permission errors, you may need to use:

```bash
pip install --user -r requirements.txt
```

Or on Windows PowerShell (as Administrator):

```powershell
pip install -r requirements.txt
```

### Step 3: Verify Installation

To verify that all packages are installed correctly:

```bash
pip list
```

You should see the following packages:
- `requests` (>=2.31.0)
- `beautifulsoup4` (>=4.12.0)
- `pandas` (>=2.0.0)
- `lxml` (>=4.9.0)
- `streamlit` (>=1.28.0)

## 🚀 Running the Project

This project offers two ways to extract URLs from sitemaps:

### Method 1: Web Application (Recommended)

The web application provides a user-friendly interface with real-time progress tracking.

#### Step 1: Start the Streamlit Server

**On Windows (PowerShell):**

```powershell
python -m streamlit run app.py
```

Or if `streamlit` is in your PATH:

```powershell
streamlit run app.py
```

**On macOS/Linux:**

```bash
python3 -m streamlit run app.py
```

Or:

```bash
streamlit run app.py
```

#### Step 2: Access the Web Interface

After running the command, you should see output similar to:

```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

1. Open your web browser
2. Navigate to `http://localhost:8501`
3. The application will load with the Botpresso-styled interface

#### Step 3: Extract URLs

1. Enter a sitemap URL in the input field (e.g., `https://example.com/sitemap.xml`)
2. Click the **"▶ Extract URLs"** button
3. Wait for the extraction to complete (progress will be shown)
4. View the results in the table below
5. Use pagination controls to navigate through large result sets
6. Click **"Download CSV"** to save the results

#### Step 4: Stop the Server

To stop the Streamlit server, press `Ctrl + C` in the terminal.

### Method 2: Command-Line Tool

For quick extractions or automation, use the command-line tool.

#### Basic Usage

```bash
python sitemap_extractor.py <sitemap_url>
```

**On Windows (PowerShell):**

```powershell
python sitemap_extractor.py https://example.com/sitemap.xml
```

**On macOS/Linux:**

```bash
python3 sitemap_extractor.py https://example.com/sitemap.xml
```

#### Example Commands

**Process a simple sitemap:**
```bash
python sitemap_extractor.py https://www.example.com/sitemap.xml
```

**Process a sitemap index:**
```bash
python sitemap_extractor.py https://www.example.com/sitemap_index.xml
```

The tool automatically detects and handles both sitemap indexes and URL sets.

#### Output

The command-line tool will:
- Process the sitemap recursively
- Extract all HTML URLs
- Save results to `sitemap_urls.csv` in the current directory
- Display progress in the terminal

## 📖 Usage Guide

### Web Application Features

#### Main Interface

- **Sitemap URL Input**: Enter the XML sitemap URL you want to process
- **Extract Button**: Click to start the extraction process
- **Progress Indicators**: Real-time updates during extraction
- **Results Table**: View all extracted URLs in a paginated table
- **Pagination Controls**: Navigate through pages of results
  - Previous/Next buttons
  - Page number input with +/- controls
  - Items per page selector
- **Download Button**: Export results as CSV

#### Sidebar Features

- **Settings**: Toggle detailed progress display
- **Statistics**: View extraction metrics
- **Navigation**: Access different sections of the app

### Command-Line Options

The CLI tool accepts a single argument:

```bash
python sitemap_extractor.py <sitemap_url>
```

**Arguments:**
- `<sitemap_url>`: The URL of the XML sitemap to process (required)

**Behavior:**
- Automatically detects sitemap type (index or URL set)
- Recursively processes nested sitemaps
- Filters out non-HTML resources
- Removes duplicate URLs
- Saves results to `sitemap_urls.csv`

## 📁 Project Structure

```
.
├── app.py                    # Streamlit web application (main UI)
├── sitemap_extractor.py      # Command-line tool
├── requirements.txt          # Python dependencies
├── README.md                 # This file
└── sitemap_urls.csv          # Output file (generated after extraction)
```

### File Descriptions

- **`app.py`**: Main Streamlit application with Botpresso design system styling
- **`sitemap_extractor.py`**: Standalone CLI tool for sitemap extraction
- **`requirements.txt`**: List of required Python packages
- **`sitemap_urls.csv`**: Generated CSV file containing extracted URLs

## 📄 Output Format

Both tools generate a CSV file (`sitemap_urls.csv`) with a single column:

```csv
URL
https://example.com/page1
https://example.com/page2
https://example.com/page3
```

The CSV file:
- Contains one URL per line
- Has a header row with "URL"
- Uses UTF-8 encoding
- Can be opened in Excel, Google Sheets, or any CSV reader

## 🎯 Supported File Types

The tool filters out non-HTML resources including:

- **Images**: jpg, jpeg, png, gif, svg, webp, ico, bmp
- **Documents**: pdf, doc, docx, xls, xlsx, ppt, pptx
- **Videos**: mp4, avi, mov, wmv, flv, webm, mkv
- **Audio files**: mp3, wav, ogg, aac, flac
- **XML/RSS feeds**: xml, rss, atom
- **Archives**: zip, rar, 7z, tar, gz
- **Assets**: css, js, json, txt
- **Other**: fonts, binaries, executables

Only URLs ending with `.html`, `.htm`, or no extension (assumed HTML) are extracted.

## 🔍 Troubleshooting

### Common Issues and Solutions

#### Issue: `streamlit: command not found` or `streamlit is not recognized`

**Solution:**
Use the Python module syntax instead:

```bash
python -m streamlit run app.py
```

Or install Streamlit globally:

```bash
pip install streamlit
```

#### Issue: `ModuleNotFoundError: No module named 'requests'`

**Solution:**
Install the requirements:

```bash
pip install -r requirements.txt
```

#### Issue: Port 8501 is already in use

**Solution:**
Streamlit will automatically try the next available port (8502, 8503, etc.). Alternatively, specify a different port:

```bash
streamlit run app.py --server.port 8502
```

#### Issue: Connection timeout when processing sitemaps

**Solution:**
- Check your internet connection
- Verify the sitemap URL is accessible
- Some sitemaps may have rate limiting - wait a few minutes and try again
- The tool includes automatic retry logic (up to 3 retries)

#### Issue: CSV file is empty or contains no URLs

**Possible causes:**
- The sitemap contains no HTML URLs (only images, PDFs, etc.)
- The sitemap URL is incorrect or inaccessible
- Network issues prevented successful extraction

**Solution:**
- Verify the sitemap URL in a browser
- Check the terminal/console for error messages
- Try a different sitemap URL

#### Issue: Permission denied when installing packages

**Solution (Windows):**
1. Run PowerShell as Administrator
2. Or use: `pip install --user -r requirements.txt`

**Solution (macOS/Linux):**
```bash
sudo pip3 install -r requirements.txt
```

Or better, use a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Getting Help

If you encounter issues not listed here:

1. Check the terminal/console output for error messages
2. Verify all dependencies are installed: `pip list`
3. Ensure Python version is 3.7 or higher: `python --version`
4. Try running with verbose output (check Streamlit logs)

## 📋 Requirements

### Python Version
- **Minimum**: Python 3.7
- **Recommended**: Python 3.8 or higher

### Python Packages

The following packages are required (see `requirements.txt`):

- **requests** (>=2.31.0) - HTTP library for fetching sitemaps
- **beautifulsoup4** (>=4.12.0) - HTML/XML parsing
- **pandas** (>=2.0.0) - Data manipulation and CSV export
- **lxml** (>=4.9.0) - Fast XML parser
- **streamlit** (>=1.28.0) - Web framework (for web UI only)

### System Requirements

- **RAM**: Minimum 512MB, recommended 1GB+
- **Disk Space**: Minimal (< 50MB for installation)
- **Network**: Internet connection required for:
  - Installing packages
  - Accessing sitemap URLs
  - Processing remote sitemaps

## 🎨 Design System

This project uses the **Botpresso Design System** with the following color palette:

- **Primary Blue**: `#5046E5`
- **Primary Green**: `#71D997`
- **Primary Red**: `#EF1E3B`
- **Light Blue Accent**: `#EFF3FF`
- **Light Green Accent**: `#EEFCF3`
- **Light Red Accent**: `#FFEFEF`

## 📝 Examples

### Example 1: Extract URLs from a Simple Sitemap

**Web UI:**
1. Open `http://localhost:8501`
2. Enter: `https://www.example.com/sitemap.xml`
3. Click "Extract URLs"
4. Download the CSV file

**CLI:**
```bash
python sitemap_extractor.py https://www.example.com/sitemap.xml
```

### Example 2: Process a Large Sitemap Index

**Web UI:**
1. Enter: `https://www.example.com/sitemap_index.xml`
2. The tool will automatically process all nested sitemaps
3. Use pagination to navigate through results

**CLI:**
```bash
python sitemap_extractor.py https://www.example.com/sitemap_index.xml
```

### Example 3: Process Multiple Sitemaps

For multiple sitemaps, run the CLI tool multiple times or use the web UI for each sitemap URL.

## 🔄 Updates and Maintenance

To update dependencies:

```bash
pip install --upgrade -r requirements.txt
```

To check for outdated packages:

```bash
pip list --outdated
```

## 📄 License

This project is provided as-is for educational and personal use.

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

---

**Happy URL Extracting! 🚀**

For questions or issues, please check the troubleshooting section or review the code comments in the source files.
#   X M L - E x t r a c t o r - T o o l  
 