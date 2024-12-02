from http import HTTPStatus

from fastapi import APIRouter, Body, Depends, HTTPException

from insurance_calc.db.models.user import User
from insurance_calc.utils.auth import obtain_token
from insurance_calc.web.api.auth import schema
from insurance_calc.web.api.auth.service import UserService, get_user_service

router = APIRouter()


@router.post("/access-token", response_model=schema.Token)
async def login_access_token(
    payload: schema.LoginPayload = Body(..., description="User login credentials"),
    user_service: UserService = Depends(get_user_service),
) -> schema.Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """

    user: User | None = await user_service.authenticate(
        username=payload.username, password=payload.password
    )

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Incorrect username or password",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="User is not active",
        )

    return schema.Token(access_token=obtain_token(user))
