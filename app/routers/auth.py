from fastapi import APIRouter, Body, HTTPException
from starlette.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from ..models.user import User, UserLogin
from ..repo.user import UserRepo
from ..security import create_token, get_hashed_password, verify_password

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/login")
async def login(
        user: UserLogin = Body(..., embed=True),
):
    exist_user = UserRepo().get_user_by_email(user.email)
    if exist_user is None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="User not found!"
        )
    if not verify_password(user.password, str(exist_user.password)):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Invalid login or password",
        )
    token = create_token(
        {
            "id": exist_user.id,
            "email": exist_user.email,
            "username": exist_user.username,
        }
    )
    return JSONResponse(
        {
            "id": exist_user.id,
            "token": token,
        },
        status_code=200,
    )


@router.post("/register")
async def register(
        user: User = Body(..., embed=True),
):
    exist_user = UserRepo().get_user_by_email(user.email)
    if exist_user is not None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="User already exists!"
        )
    hashed_password = get_hashed_password(user.password)
    new_user_id = UserRepo().create_user(
        username=user.username, email=user.email, password=hashed_password
    )

    token = create_token(
        {
            "id": new_user_id,
            "email": user.email,
            "username": user.username,
        }
    )

    return JSONResponse(
        {
            "id": new_user_id,
            "name": user.username,
            "email": user.email,
            "token": token,
        },
        status_code=200,
    )
