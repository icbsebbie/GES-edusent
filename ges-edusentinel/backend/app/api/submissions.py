import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import DataSubmission, User
from ..schemas import SubmissionCreate
from ..deps import get_current_user
from ..org_tree import is_in_subtree

router = APIRouter(prefix="/submissions")

@router.post("")
def submit(req: SubmissionCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if not is_in_subtree(db, user.org_unit_id, req.org_unit_id):
        raise HTTPException(status_code=403, detail="Out of scope")

    s = DataSubmission(
        org_unit_id=req.org_unit_id,
        term_id=req.term_id,
        dataset=req.dataset,
        payload_json=json.dumps(req.payload),
    )
    db.add(s); db.commit(); db.refresh(s)
    return {"id": s.id, "submitted_at": s.submitted_at.isoformat()}

@router.get("")
def list_submissions(term_id: int, dataset: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    q = db.query(DataSubmission).filter(DataSubmission.term_id == term_id, DataSubmission.dataset == dataset).all()
    # Filter by scope
    out = []
    for s in q:
        if is_in_subtree(db, user.org_unit_id, s.org_unit_id):
            out.append({
                "id": s.id,
                "org_unit_id": s.org_unit_id,
                "term_id": s.term_id,
                "dataset": s.dataset,
                "submitted_at": s.submitted_at.isoformat()
            })
    return out
