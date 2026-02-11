import csv
import io
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.models import Operator, RiskScore

router = APIRouter(prefix="/upload", tags=["upload"])
security = HTTPBearer()

JWT_SECRET = "dev-secret-change-me"
JWT_ALGORITHM = "HS256"


def _compute_risk(operator_type: str, location: str) -> float:
    type_weights = {"upstream": 65, "midstream": 45, "downstream": 35}
    base = type_weights.get(operator_type.lower(), 50)
    location_factor = min(len(location.strip()) * 1.5, 35)
    return round(min(base + location_factor, 100), 2)


def _verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    try:
        return jwt.decode(credentials.credentials, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        ) from exc


@router.post("", summary="Upload CSV and process operator risk scores")
async def upload_csv(
    file: UploadFile = File(...),
    _token_payload: dict = Depends(_verify_token),
    db: AsyncSession = Depends(get_db),
) -> dict:
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are accepted")

    content = await file.read()
    text_stream = io.StringIO(content.decode("utf-8"))
    reader = csv.DictReader(text_stream)

    required_columns = {"name", "type", "location"}
    if not reader.fieldnames or not required_columns.issubset(set(reader.fieldnames)):
        raise HTTPException(
            status_code=400,
            detail="CSV must include name,type,location columns",
        )

    processed = 0
    for row in reader:
        name = (row.get("name") or "").strip()
        operator_type = (row.get("type") or "").strip().lower()
        location = (row.get("location") or "").strip()

        if not name or operator_type not in {"upstream", "midstream", "downstream"} or not location:
            continue

        existing_operator_result = await db.execute(
            select(Operator).where(Operator.name == name, Operator.location == location)
        )
        operator = existing_operator_result.scalar_one_or_none()

        if operator is None:
            operator = Operator(name=name, type=operator_type, location=location)
            db.add(operator)
            await db.flush()
        else:
            operator.type = operator_type

        score_value = _compute_risk(operator_type, location)

        existing_score_result = await db.execute(
            select(RiskScore).where(RiskScore.operator_id == operator.id)
        )
        existing_score = existing_score_result.scalar_one_or_none()

        if existing_score is None:
            db.add(
                RiskScore(
                    operator_id=operator.id,
                    score=score_value,
                    updated_at=datetime.utcnow(),
                )
            )
        else:
            existing_score.score = score_value
            existing_score.updated_at = datetime.utcnow()

        processed += 1

    await db.commit()

    return {"processed": processed, "message": "CSV uploaded and risk scores updated"}


@router.post("/token", summary="Get a demo JWT token")
async def create_demo_token(username: str, password: str) -> dict:
    if username != "admin" or password != "admin123":
        raise HTTPException(status_code=401, detail="Invalid credentials")

    expire = datetime.utcnow() + timedelta(hours=8)
    token = jwt.encode({"sub": username, "exp": expire}, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}
