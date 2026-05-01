import json
from collections import defaultdict
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import OrgUnit, DataSubmission, User, OrgUnitType
from ..deps import get_current_user
from ..org_tree import is_in_subtree
from ..agents.tasks import deepscan_task

router = APIRouter(prefix="/analytics")

@router.get("/completion")
def completion(term_id: int, dataset: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    # Completion for SCHOOL units in user's subtree
    schools = db.query(OrgUnit).filter(OrgUnit.type == OrgUnitType.SCHOOL).all()
    schools = [s for s in schools if is_in_subtree(db, user.org_unit_id, s.id)]

    subs = db.query(DataSubmission).filter(DataSubmission.term_id == term_id, DataSubmission.dataset == dataset).all()
    submitted = {s.org_unit_id for s in subs if is_in_subtree(db, user.org_unit_id, s.org_unit_id)}

    total = len(schools)
    done = sum(1 for s in schools if s.id in submitted)
    return {"term_id": term_id, "dataset": dataset, "total_schools": total, "submitted": done, "completion_rate": (done/total if total else 0)}

@router.get("/indicator-summary")
def indicator_summary(term_id: int, dataset: str, indicator_key: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    subs = db.query(DataSubmission).filter(DataSubmission.term_id == term_id, DataSubmission.dataset == dataset).all()
    vals = []
    for s in subs:
        if not is_in_subtree(db, user.org_unit_id, s.org_unit_id):
            continue
        payload = json.loads(s.payload_json)
        v = payload.get(indicator_key)
        if isinstance(v, (int, float)):
            vals.append(v)
    if not vals:
        raise HTTPException(404, "No numeric values found")
    return {"count": len(vals), "min": min(vals), "max": max(vals), "mean": sum(vals)/len(vals)}

@router.post("/deepscan")
def deepscan(term_id: int, dataset: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    job = deepscan_task.delay(user.org_unit_id, term_id, dataset)
    return {"job_id": job.id, "status": "queued"}
