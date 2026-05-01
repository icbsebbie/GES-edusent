from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import AcademicYear, Term, User
from ..schemas import AcademicYearCreate, TermCreate
from ..deps import get_current_user

router = APIRouter(prefix="/academics")

@router.post("/years")
def create_year(req: AcademicYearCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    y = AcademicYear(**req.model_dump())
    db.add(y); db.commit(); db.refresh(y)
    return {"id": y.id, **req.model_dump()}

@router.post("/terms")
def create_term(req: TermCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    t = Term(**req.model_dump())
    db.add(t); db.commit(); db.refresh(t)
    return {"id": t.id, **req.model_dump()}

@router.get("/terms")
def list_terms(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    terms = db.query(Term).all()
    return [{"id": t.id, "academic_year_id": t.academic_year_id, "name": t.name} for t in terms]
