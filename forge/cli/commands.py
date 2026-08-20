import time

from ..client.api import ForgeClient
from .output import print_error, print_result


def run_command(client: ForgeClient, args: list[str]) -> int:
    if not args:
        print_error("missing code argument")
        return 1

    code = args[0]
    language = "python"
    stdin_data = ""
    version = None
    timeout_ms = None
    memory_mb = None
    wait = False

    i = 1
    while i < len(args):
        arg = args[i]
        if arg == "--language" and i + 1 < len(args):
            language = args[i + 1]
            i += 2
        elif arg == "--stdin" and i + 1 < len(args):
            stdin_data = args[i + 1]
            i += 2
        elif arg == "--version" and i + 1 < len(args):
            version = args[i + 1]
            i += 2
        elif arg == "--timeout" and i + 1 < len(args):
            timeout_ms = int(args[i + 1])
            i += 2
        elif arg == "--memory" and i + 1 < len(args):
            memory_mb = int(args[i + 1])
            i += 2
        elif arg == "--wait":
            wait = True
            i += 1
        else:
            print_error(f"unknown argument: {arg}")
            return 1

    try:
        created = client.execute(
            language=language,
            code=code,
            stdin=stdin_data,
            version=version,
            timeout_ms=timeout_ms,
            memory_mb=memory_mb,
        )
    except Exception as exc:
        print_error(str(exc))
        return 1

    if not wait:
        print_result(created)
        return 0

    execution_id = created["execution_id"]
    while True:
        result = client.get_result(execution_id)
        status = result.get("status", "")
        if status not in ("QUEUED", "RUNNING"):
            print_result(result)
            return 0
        time.sleep(0.2)


def get_command(client: ForgeClient, args: list[str]) -> int:
    if not args:
        print_error("missing execution_id argument")
        return 1
    try:
        result = client.get_result(args[0])
        print_result(result)
        return 0
    except Exception as exc:
        print_error(str(exc))
        return 1


def health_command(client: ForgeClient, args: list[str]) -> int:
    try:
        print_result(client.health())
        return 0
    except Exception as exc:
        print_error(str(exc))
        return 1