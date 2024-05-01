from fastapi import FastAPI, exceptions
from fastapi.responses import JSONResponse
from pydantic import ValidationError
import json
import logging
import sys
from src.api import example
from starlette.middleware.cors import CORSMiddleware

description = """
Todo...
"""

app = FastAPI(
    title="PolyChats",
    description=description,
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Jesus Angel Avalos-Regalado",
        "email": "javalosr@calpoly.edu",
    },
)


app.add_middleware(
    CORSMiddleware,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)

# include routes
app.include_router(example.router)


@app.exception_handler(exceptions.RequestValidationError)
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    logging.error(f"The client sent invalid data!: {exc}")
    exc_json = json.loads(exc.json())
    response = {"message": [], "data": None}
    for error in exc_json:
        response['message'].append(f"{error['loc']}: {error['msg']}")

    return JSONResponse(response, status_code=422)


@app.get("/")
async def root():
    return {"message": "Welcome to [poly]Chats."}
