"""..."""

import uvicorn
from requests.exceptions import HTTPError
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


from api.v1.router import api_router


app = FastAPI()


@app.exception_handler(HTTPError)
async def http_error_handler(request: Request, exc: HTTPError):
    status_code = exc.response.status_code if exc.response else 400
    detail = exc.response.text if exc.response else str(exc)
    return JSONResponse(status_code=status_code, content={"detail": detail})


app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8003)
