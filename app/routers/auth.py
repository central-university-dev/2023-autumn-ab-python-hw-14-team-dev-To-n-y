from fastapi import APIRouter

from ..models.user import User

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/login")
async def login(user: User) -> bool:
    # implement auth
    print(user)
    return True


@router.post("/register")
async def register(user: User) -> bool:
    # implement auth
    print(user)
    return False
