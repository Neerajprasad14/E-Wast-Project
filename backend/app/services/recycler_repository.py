"""CSV-backed demo repository. Replace with SQLAlchemy/PostGIS implementation in production."""
import csv
from functools import lru_cache
from pathlib import Path
from app.schemas.analysis import RecyclerResponse


DATA_PATH = Path(__file__).resolve().parents[3] / "data" / "recyclers.csv"


@lru_cache
def get_recyclers() -> list[RecyclerResponse]:
    with DATA_PATH.open(encoding="utf-8", newline="") as file:
        records = []
        for row in csv.DictReader(file):
            records.append(RecyclerResponse(
                id=row["id"], name=row["name"], address=row["address"], city=row["city"], state=row["state"],
                latitude=float(row["latitude"]), longitude=float(row["longitude"]),
                accepted_waste_types=[item.strip() for item in row["accepted_waste_types"].split("|")],
                pickup_available=row["pickup_available"].lower() == "true", verified=row["verified"].lower() == "true",
                authorization_status=row["authorization_status"], verification_source=row["verification_source"] or None,
                last_verified=row["last_verified"] or None, opening_hours=row["opening_hours"] or None,
                phone=row["phone"] or None, email=row["email"] or None, website=row["website"] or None,
                rating=float(row["rating"]) if row["rating"] else None,
            ))
        return records
