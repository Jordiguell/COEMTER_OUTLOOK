import argparse
from . import db
from .headless import run_auto
from .watcher import watch_folder
from .gui import crear_interficie


def main():
    parser = argparse.ArgumentParser(description='Programa Coemter')
    parser.add_argument('--auto', help='process PDF headlessly')
    parser.add_argument('--watch', action='store_true', help='watch folder for PDFs')
    args = parser.parse_args()

    db.init_db()

    if args.auto:
        raise SystemExit(run_auto(args.auto))
    elif args.watch:
        watch_folder()
    else:
        root = crear_interficie()
        root.mainloop()

if __name__ == '__main__':
    main()
