from sqlalchemy import text
from sqlalchemy.orm import Session

def is_in_subtree(db: Session, root_id: int, target_id: int) -> bool:
    if root_id == target_id:
        return True
    q = text("""
    WITH RECURSIVE tree AS (
      SELECT id, parent_id FROM org_units WHERE id = :root
      UNION ALL
      SELECT ou.id, ou.parent_id
      FROM org_units ou
      JOIN tree t ON ou.parent_id = t.id
    )
    SELECT 1 FROM tree WHERE id = :target LIMIT 1
    """)
    r = db.execute(q, {"root": root_id, "target": target_id}).scalar()
    return bool(r)
