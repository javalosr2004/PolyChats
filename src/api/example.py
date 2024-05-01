from fastapi import APIRouter, Depends
from pydantic import BaseModel

router = APIRouter(
    prefix="/example",
    tags=["example"],
)


@router.get("/")
def example():
    return {"message": "hello world"}
