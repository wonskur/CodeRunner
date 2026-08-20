from fastapi import Header, HTTPException


def require_api_key(x_api_key: str = Header(default="")) -> None:
    if not x_api_key:
        raise HTTPException(status_code=401, detail="missing api key")