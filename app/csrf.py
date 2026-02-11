from fastapi import Request, Form, HTTPException, Depends


async def csrf_protect(request: Request, csrf_token: str = Form(...)) -> None:
    session_token = request.session.get("csrf_token")
    if not session_token or csrf_token != session_token:
        raise HTTPException(status_code=400, detail="Invalid CSRF token")


def csrf_dependency():
    return Depends(csrf_protect)
