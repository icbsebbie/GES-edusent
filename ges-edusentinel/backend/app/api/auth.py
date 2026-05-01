from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import User
from ..schemas import LoginRequest, Token, UserOut
from ..security import verify_password, create_access_token

router = APIRouter(prefix="/auth")

@router.post("/login", response_model=Token)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email).first()
    if not user or not verify_password(req.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(sub=user.email, extra={"uid": user.id, "role": user.role.value, "org_unit_id": user.org_unit_id})
    return {"access_token": token}

@router.get("/me", response_model=UserOut)
def me(current: User = Depends(__import__("app.deps").deps.get_current_user)):
    ou = current.org_unit
    return {
        "id": current.id,
        "email": current.email,
        "full_name": current.full_name,
        "role": current.role.value,
        "org_unit": {"id": ou.id, "name": ou.name, "type": ou.type.value, "parent_id": ou.parent_id}
    }
