import sys

from ..client.api import ForgeClient
from .commands import get_command, health_command, run_command

USAGE = """usage: forge <command> [args]

commands:
  run <code> [--language LANG] [--stdin DATA] [--version VER]
             [--timeout MS] [--memory MB] [--wait]
  get <execution_id>
  health
"""


def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]

    if not argv:
        print(USAGE, end="")
        return 1

    command = argv[0]
    args = argv[1:]

    if command in ("-h", "--help", "help"):
        print(USAGE, end="")
        return 0

    client = ForgeClient()

    if command == "run":
        return run_command(client, args)
    if command == "get":
        return get_command(client, args)
    if command == "health":
        return health_command(client, args)

    print(f"unknown command: {command}")
    print(USAGE, end="")
    return 1


if __name__ == "__main__":
    sys.exit(main())