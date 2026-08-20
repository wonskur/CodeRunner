import json


def print_result(result: dict) -> None:
    print(json.dumps(result, indent=2, ensure_ascii=False))


def print_error(message: str) -> None:
    print(f"error: {message}")