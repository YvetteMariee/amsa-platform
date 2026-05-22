from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.services.auth_service import authenticate_user, create_access_token

router = APIRouter()


@router.post('/auth/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail='Invalid credentials')
    token = create_access_token({"sub": user.username, "role": user.role, "user_id": user.id})
    return {"access_token": token, "token_type": "bearer"}
