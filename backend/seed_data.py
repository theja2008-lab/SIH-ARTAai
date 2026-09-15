"""
ARTINO Seed Data Script.
Pre-populates database with default artisan profiles (Kuppuswamy demo) if needed.
"""
from app.core.database import SessionLocal, Base, engine
from app.models.models import Artisan

Base.metadata.create_all(bind=engine)

def seed_db():
    db = SessionLocal()
    existing = db.query(Artisan).filter(Artisan.id == "ART-0001").first()
    if not existing:
        kuppuswamy = Artisan(
            id="ART-0001",
            name="Kuppuswamy",
            age=45,
            preferred_language="ta",
            experience_years=25,
            craft_expertise="Traditional Wood Craft",
            identity_status="DEMO_MATCHED"
        )
        db.add(kuppuswamy)
        db.commit()
        print("[ARTINO] Seeded demo artisan profile ART-0001 (Kuppuswamy).")
    db.close()

if __name__ == "__main__":
    seed_db()
