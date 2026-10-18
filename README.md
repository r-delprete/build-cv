# Build CV

A Python tool that generates a structured CV in PDF format from JSON data.

## Overview

**Build CV** generates PDF CVs from structured JSON data. It separates content, configuration, styling, and document-generation logic into dedicated modules, making the codebase easier to maintain and extend.

A command-line interface lets users specify the input data, output PDF, and profile photo without modifying the source code.

## Features

- **JSON-based content:** Keep CV data separate from the generation logic.
- **Command-line interface:** Customize input, output, and profile photo paths.
- **Modular architecture:** Build individual CV sections through dedicated modules.
- **PDF generation:** Create formatted CV documents programmatically.
- **Profile photo processing:** Prepare the profile photo for inclusion in the document.
- **Centralized data handling:** Parse CV data into structured Python objects.
- **Configuration:** Customize document layout and typography through application settings.
- **Tests:** Test configuration and CV data handling.

## Tech Stack

- Python
- JSON
- `argparse`
- ReportLab
- pytest

## Getting Started

### Prerequisites

- Python
- Git

### Installation

Clone the repository:

```bash
git clone https://github.com/r-delprete/build-cv.git
cd build-cv
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it.

**Linux and macOS**

```bash
source .venv/bin/activate
```

**Windows (PowerShell)**

```powershell
.venv\Scripts\Activate.ps1
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

## Usage

Generate a CV using the default paths:

```bash
python main.py
```

By default, the application uses:

- **CV data:** `data/cv.example.json`
- **Output PDF:** `output/cv.example.pdf`
- **Profile photo:** `assets/cv-pic.example.png`

### Command-line options

Display the available options and their default values:

```bash
python main.py --help
```

| Argument | Description | Default |
|---|---|---|
| `--cv PATH` | Path to the input CV JSON file. | `data/cv.example.json` |
| `--output PATH` | Path for the generated PDF. | `output/cv.example.pdf` |
| `--photo PATH` | Path to the profile photo. | `assets/cv-pic.example.png` |
| `-h`, `--help` | Display help and exit. | — |

### Examples

Use a custom CV data file:

```bash
python main.py --cv data/cv.json
```

Specify an output file:

```bash
python main.py --output output/my-cv.pdf
```

Use a custom profile photo:

```bash
python main.py --photo assets/profile.png
```

Specify all paths:

```bash
python main.py \
    --cv data/cv.json \
    --output output/my-cv.pdf \
    --photo assets/profile.png
```

Each path can be overridden independently.

## Configuration

### CV data

The example file `data/cv.example.json` demonstrates the expected structure of the CV data.

Use it as a starting point to create your own JSON file, then pass its path with `--cv`.

### Application settings

The `config.json` file contains the application's configurable settings, such as document layout and typography.

Review this file and `config.py` to understand the available settings and their defaults.

### Profile photo

The default profile photo is `assets/cv-pic.example.png`.

Provide a different image with `--photo` to use your own profile picture.

## Project Structure

```text
build-cv/
├── assets/
│   └── cv-pic.example.png
├── builder/
│   ├── __init__.py
│   ├── courses.py
│   ├── document.py
│   ├── education.py
│   ├── experience.py
│   ├── fonts.py
│   ├── header.py
│   ├── languages.py
│   ├── profile.py
│   ├── publications.py
│   ├── skills.py
│   └── soft_skills.py
├── data/
│   └── cv.example.json
├── tests/
│   ├── test_config.py
│   └── test_cv_data.py
├── config.json
├── config.py
├── cv_data.py
├── main.py
├── requirements.txt
├── run.sh
├── styles.py
└── README.md
```

## Development

Run the test suite from the project root:

```bash
python -m pytest -v
```

When contributing changes, keep CV data handling, configuration, and PDF generation logic separated into their respective modules.

## License

See the `LICENSE` file for the terms under which this project can be used, modified, and distributed.
