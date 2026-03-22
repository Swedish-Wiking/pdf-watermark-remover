# PDF Watermark Remover

A command-line interface (CLI) tool written in Python that losslessly finds and removes specific text-based watermarks from PDF files (e.g., personalized order numbers and dates).

## Features

* **Interactive Menu:** User-friendly prompts allow you to choose between default watermark patterns, exact text removal, or custom Regex patterns on the fly.
* **Flexible Automation:** Bypass the menu entirely using command-line flags (`-t` for text, `-p` for regex) for fast, automated batch processing.
* **Lossless Redaction:** Deletes the text object directly from the PDF's underlying code without drawing ugly white boxes over background illustrations.
* **Batch Processing:** Supports processing individual files, multiple files at once, or entire directories via recursive search.
* **Rich UI:** Features dynamic progress bars showing both overall completion and individual page-scanning progress.

## Prerequisites

* **Python 3.10** or newer. You can download it from [python.org](https://www.python.org/downloads/).
  * *Note for Windows users:* Make sure to check **"Add Python to PATH"** during installation.

## Installation

### 1. Clone or Download the Repository

Download the repository as a ZIP or clone it via Git, then navigate into the folder:

```bash
git clone [https://github.com/your-username/pdf-watermark-remover.git](https://github.com/your-username/pdf-watermark-remover.git)
cd pdf-watermark-remover
```

### 2. Create a Virtual Environment (.venv)

It is highly recommended to run the script inside a virtual environment to avoid package conflicts with other projects.

```bash
python -m venv .venv
```

### 3. Activate the Virtual Environment

Depending on your operating system, activate the environment using one of the following commands:

* **Windows (Command Prompt / PowerShell):**

  ```bash
  .venv\Scripts\activate
  ```

* **macOS / Linux:**

  ```bash
  source .venv/bin/activate
  ```

*(You will know it is activated when you see `(.venv)` at the beginning of your terminal prompt.)*

### 4. Install Dependencies

The script relies on `pymupdf` for PDF manipulation and `rich` for the terminal interface. Install them via your requirements file:

```bash
pip install -r requirements.txt
```

---

## Usage

The script is executed from the terminal. You can pass individual files, multiple files, or entire folders as arguments. The script will automatically filter for `.pdf` files, process them, and save a clean copy appended with `_clean.pdf` in the same directory. **Your original files are never modified.**

### Interactive Mode

If you only provide file paths, the script will launch an interactive menu asking what you want to remove:

```bash
python main.py "path/to/book.pdf"
```

### Fast Mode (Command-Line Flags)

You can skip the interactive menu by providing the search parameters directly in your command.

**1. Remove exact text:**
Use the `-t` or `--text` flag to remove a specific string of text. The script will safely handle any special characters.

```bash
python main.py "path/to/folder/" -t "This book belongs to John Doe"
```

**2. Remove using a custom Regex pattern:**
Use the `-p` or `--pattern` flag to find and remove dynamic text using Regular Expressions.

```bash
python main.py "book.pdf" -p "Order:.*?(?:förbjuden\.?)"
```

---

## How It Works Under the Hood

The script uses the `PyMuPDF` library to read the document page by page. When using Regex, it utilizes the `re.DOTALL` flag, which allows it to dynamically find the watermark regardless of whether the text is split across multiple hidden lines in the PDF source code. It targets the exact coordinates of that string and applies a redaction annotation without fill colors, effectively wiping the text from existence while leaving the background untouched.
