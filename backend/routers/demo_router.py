from fastapi import APIRouter

router = APIRouter(
    prefix="/demo",
    tags=["demo"]
)

@router.get("/")
def test_route():
    return {"message":"Ceci est une route test "}

@router.get("/othertest")
def other():
    return{"message":"a other one"}