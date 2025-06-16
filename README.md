# Programa Coemter

Utility to process Coemter order PDFs. It can run with a Tkinter GUI, in headless mode for a single PDF or as a folder watcher.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### GUI

```bash
python -m programa_coemter
```

### Headless

```bash
python -m programa_coemter --auto path/to/order.pdf
```

Exit code `1` means Sage was not ready.

### Watcher

```bash
python -m programa_coemter --watch
```

The watcher starts a process for every new PDF detected inside `pdf_folder`.
Failed runs are retried up to three times with five minutes delay.

### Windows Service

Install the watcher as a service:

```bat
python watcher_service.py install
python watcher_service.py start
```

Alternatively create a Scheduled Task that executes `python -m programa_coemter --watch` on workstation unlock or when a new file appears.
