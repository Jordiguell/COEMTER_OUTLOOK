# Programa Coemter

A utility to process Coemter orders from PDF files. It can run with a GUI or in headless mode.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

GUI mode:

```bash
python -m programa_coemter
```

Process a PDF automatically:

```bash
python -m programa_coemter --auto path/to/order.pdf
```

Watch folder for new PDFs:

```bash
python -m programa_coemter --watch
```

See `programa_coemter/watcher.py` for configuring as a service or scheduled task.
