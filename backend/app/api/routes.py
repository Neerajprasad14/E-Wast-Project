from fastapi import APIRouter, File, Form, Header, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from app.agents.location_agent import LocationAgent
from app.agents.orchestrator import EWasteAdvisorOrchestrator
from app.agents.recycler_locator_agent import RecyclerLocatorAgent
from app.schemas.analysis import AnalyzeResponse, RecyclerResponse
from app.schemas.auth import AuthResponse, LoginRequest, RegisterRequest, UserResponse
from app.db import SessionLocal
from app.models import User
from app.services.auth import get_user_for_token, hash_password, issue_session, revoke_session, verify_password
from app.services.recycler_repository import get_recyclers

router = APIRouter(prefix="/api")
orchestrator, locator, location_agent = EWasteAdvisorOrchestrator(), RecyclerLocatorAgent(), LocationAgent()
ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}


def database_error(error: Exception) -> HTTPException:
    return HTTPException(503, "Database is unavailable. Start PostgreSQL, create the ewaste_advisor database, and set DATABASE_URL in backend/.env.")


def bearer_token(authorization: str | None) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, "Please sign in to continue.")
    return authorization.removeprefix("Bearer ").strip()

@router.get("/health")
async def health() -> dict[str, str]: return {"status": "ok"}


@router.post("/auth/register", response_model=AuthResponse, status_code=201)
async def register(payload: RegisterRequest) -> AuthResponse:
    db = SessionLocal()
    try:
        email = str(payload.email).lower()
        if db.scalar(select(User).where(User.email == email)):
            raise HTTPException(409, "An account already exists for this email.")
        user = User(full_name=payload.full_name.strip(), email=email, password_hash=hash_password(payload.password))
        db.add(user)
        db.commit()
        db.refresh(user)
        token = issue_session(db, user)
        return AuthResponse(token=token, user=UserResponse(id=user.id, full_name=user.full_name, email=user.email))
    except HTTPException:
        raise
    except SQLAlchemyError as error:
        raise database_error(error) from error
    finally:
        db.close()


@router.post("/auth/login", response_model=AuthResponse)
async def login(payload: LoginRequest) -> AuthResponse:
    db = SessionLocal()
    try:
        user = db.scalar(select(User).where(User.email == str(payload.email).lower()))
        if not user or not verify_password(payload.password, user.password_hash):
            raise HTTPException(401, "Incorrect email or password.")
        token = issue_session(db, user)
        return AuthResponse(token=token, user=UserResponse(id=user.id, full_name=user.full_name, email=user.email))
    except HTTPException:
        raise
    except SQLAlchemyError as error:
        raise database_error(error) from error
    finally:
        db.close()


@router.get("/auth/me", response_model=UserResponse)
async def current_user(authorization: str | None = Header(None)) -> UserResponse:
    db = SessionLocal()
    try:
        user = get_user_for_token(db, bearer_token(authorization))
        if not user:
            raise HTTPException(401, "Your session has expired. Please sign in again.")
        return UserResponse(id=user.id, full_name=user.full_name, email=user.email)
    except HTTPException:
        raise
    except SQLAlchemyError as error:
        raise database_error(error) from error
    finally:
        db.close()


@router.post("/auth/logout", status_code=204)
async def logout(authorization: str | None = Header(None)) -> None:
    db = SessionLocal()
    try:
        revoke_session(db, bearer_token(authorization))
    except SQLAlchemyError as error:
        raise database_error(error) from error
    finally:
        db.close()

@router.get("/waste-categories")
async def waste_categories() -> list[str]: return ["Computers", "Laptops", "Mobile Phones", "Tablets", "Televisions", "Monitors", "Printers", "Batteries", "Chargers", "Cables", "PCBs", "Small Appliances", "Large Appliances", "Other E-Waste", "Unknown"]

@router.get("/states")
async def states() -> list[str]: return sorted({item.state for item in get_recyclers()})

@router.get("/cities")
async def cities(state: str | None = None) -> list[str]: return sorted({item.city for item in get_recyclers() if not state or item.state.lower() == state.lower()})

@router.get("/recyclers", response_model=list[RecyclerResponse])
async def recyclers(city: str | None = None, state: str | None = None) -> list[RecyclerResponse]: return [item for item in get_recyclers() if (not city or item.city.lower() == city.lower()) and (not state or item.state.lower() == state.lower())]

@router.get("/recyclers/nearby", response_model=list[RecyclerResponse])
async def nearby_recyclers(latitude: float, longitude: float, radius_km: float = 25, waste_type: str | None = None, verified_only: bool = False) -> list[RecyclerResponse]:
    location_agent.resolve(latitude, longitude, None, None)
    if not 1 <= radius_km <= 250: raise HTTPException(422, "radius_km must be between 1 and 250")
    return locator.search(latitude, longitude, radius_km, waste_type, verified_only)

@router.get("/recyclers/{recycler_id}", response_model=RecyclerResponse)
async def recycler_detail(recycler_id: str) -> RecyclerResponse:
    for item in get_recyclers():
        if item.id == recycler_id: return item
    raise HTTPException(404, "Recycler not found")

@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(image: UploadFile = File(...), latitude: float | None = Form(None), longitude: float | None = Form(None)) -> AnalyzeResponse:
    if image.content_type not in ALLOWED_TYPES: raise HTTPException(415, "Upload a PNG, JPEG, or WebP image.")
    content = await image.read()
    if not content: raise HTTPException(422, "The uploaded image is empty.")
    if len(content) > 10 * 1024 * 1024: raise HTTPException(413, "Image must be 10 MB or smaller.")
    location_agent.resolve(latitude, longitude, None, None)
    return await orchestrator.analyze(content, image.filename or "upload.jpg", latitude, longitude)
