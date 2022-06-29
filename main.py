import sys


from chess.controllers import Application


def main(args):
    if len(args) < 2:
        print(f"Usage: {args[0]} <database path>")
        raise SystemExit(-1)
    # Unpack the args list to extract the database path from args[1]
    database_path, *_ = args[1:]
    app = Application(database_path)
    app.run()


if __name__ == "__main__":
    main(sys.argv)
