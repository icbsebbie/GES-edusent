from sqlalchemy.orm import Session
from .db import SessionLocal, engine, Base
from .models import OrgUnit, OrgUnitType, User, Role
from .security import hash_password

def run():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()

    # Create HQ if not exists
    hq = db.query(OrgUnit).filter(OrgUnit.type == OrgUnitType.HQ).first()
    if not hq:
        hq = OrgUnit(name="GES HQ", type=OrgUnitType.HQ, parent_id=None)
        db.add(hq); db.commit(); db.refresh(hq)

    # Create admin user
    admin = db.query(User).filter(User.email == "admin@ges.local").first()
    if not admin:
        admin = User(
            email="admin@ges.local",
            full_name="HQ Admin",
            password_hash=hash_password("admin123"),
            role=Role.HQ_ADMIN,
            org_unit_id=hq.id,
        )
        db.add(admin); db.commit()

    db.close()

if __name__ == "__main__":
    run()
