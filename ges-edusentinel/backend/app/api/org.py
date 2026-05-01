from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import OrgUnit, OrgUnitType, User, Role
from ..deps import get_current_user
from ..org_tree import is_in_subtree

router = APIRouter(prefix="/org")

@router.get("/children/{org_unit_id}")
def children(org_unit_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if not is_in_subtree(db, user.org_unit_id, org_unit_id):
        raise HTTPException(status_code=403, detail="Out of scope")
    rows = db.query(OrgUnit).filter(OrgUnit.parent_id == org_unit_id).all()
    return [{"id": r.id, "name": r.name, "type": r.type.value, "parent_id": r.parent_id} for r in rows]

@router.post("/create")
def create_org_unit(payload: dict, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    # Minimal: only admins can create under their subtree
    if user.role == Role.VIEWER:
        raise HTTPException(status_code=403, detail="Not allowed")
    name = payload.get("name")
    type_ = payload.get("type")
    parent_id = payload.get("parent_id")
    if not name or not type_:
        raise HTTPException(400, "name/type required")
    if parent_id is not None and not is_in_subtree(db, user.org_unit_id, int(parent_id)):
        raise HTTPException(status_code=403, detail="Parent out of scope")

    ou = OrgUnit(name=name, type=OrgUnitType(type_), parent_id=parent_id)
    db.add(ou); db.commit(); db.refresh(ou)
    return {"id": ou.id, "name": ou.name, "type": ou.type.value, "parent_id": ou.parent_id}
