from fastapi import APIRouter

router = APIRouter()

@router.get("/users")
def get_users():
    return [
        {"id": 1, "name": "John Doe"},
        {"id": 2, "name": "Jane Smith"}
    ]
