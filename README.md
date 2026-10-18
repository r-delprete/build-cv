# Build CV

A Python tool that generates a structured CV in PDF format from JSON data.

## Overview

**Build CV** is a Python project for generating a PDF CV from structured data.

It separates CV content, configuration, and document-generation logic into dedicated modules, making the project easier to maintain and extend.

The command-line interface allows users to control the generation process through arguments rather than modifying the source code.

## Features

- **JSON-based data:** Store CV content separately from the generation logic.
- **Command-line interface:** Configure the generation process using command-line arguments.
- **Modular architecture:** Organize CV sections into dedicated modules.
- **PDF generation:** Generate a formatted CV programmatically.
- **Profile photo processing:** Prepare the profile picture for use in the document.
- **Centralized data handling:** Keep CV data structures and access logic in a dedicated module.
- **Tests:** Include tests for configuration and CV data handling.

## Tech Stack

- Python
- JSON
- `argparse` for command-line argument parsing
- PDF generation libraries and supporting Python packages

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

Create and activate a virtual environment:

```bash
python -m venv .venv
```

On Linux and macOS:

```bash
source .venv/bin/activate
```

On Windows (PowerShell):

```powershell
.venv\Scripts\Activate.ps1
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Generate the CV using the default configuration:

```bash
python main.py
```

By default, the script uses the following files:

- **CV data:** `data/cv.example.json`
- **Output PDF:** `output/cv.example.pdf`
- **Profile photo:** `assets/cv-pic.example.png`

### Command-line options

To display all available options and their default values, run:

```bash
python main.py --help
```

| Argument | Description | Default |
|---|---|---|
| `--cv PATH` | Path to the JSON file containing the CV data. | `data/cv.example.json` |
| `--output PATH` | Path where the generated PDF will be saved. | `output/cv.example.pdf` |
| `--photo PATH` | Path to the profile photo. | `assets/cv-pic.example.png` |
| `-h`, `--help` | Display the help message and exit. | — |

### Examples

**Use a custom CV data file:**

```bash
python main.py --cv data/cv.json
```

**Specify a custom output path:**

```bash
python main.py --output output/my-cv.pdf
```

**Use a custom profile photo:**

```bash
python main.py --photo assets/profile.png
```

**Customize all paths:**

```bash
python main.py \
    --cv data/cv.json \
    --output output/my-cv.pdf \
    --photo assets/profile.png
```

The paths can be specified independently, so you only need to override the defaults you want to change.

## Configuration

### CV data

The CV content is stored in a JSON file. The repository includes an example file:

```text
data/cv.example.json
```

Use it as a reference when creating your own CV data file. Pass its path through the `--cv` argument.

### Output PDF

The generated document is saved to `output/cv.example.pdf` by default. Use `--output` to specify a different filename or destination.

### Profile photo

The default profile photo is `assets/cv-pic.example.png`. To use another image, provide its path through the `--photo` argument.

## Configuration

### CV data

The CV content is stored in a JSON file. Use the example file as a starting point:

```text
data/cv.example.json
```

Create your own data file following the same structure, then pass its path using the corresponding command-line option, if supported.

### Application settings

The project also includes a configuration file:

```text
config.json
```

Consult the available command-line options and configuration defaults to determine which settings can be overridden when running the script.

### Profile picture

The repository includes an example profile picture:

```text
assets/cv-pic.example.png
```

Use your own image according to the path and format expected by the application.

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

The codebase separates CV data management, configuration, document generation, and individual CV sections.

Tests are available for configuration and CV data handling. Run them using your preferred test runner, such as `pytest`, if it is installed and configured for the project.

## License

No license has been specified yet. Add a `LICENSE` file to define the terms under which others may use, modify, or distribute this project.