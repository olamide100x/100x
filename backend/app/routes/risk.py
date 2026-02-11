from fastapi import APIRouter, Depends
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.models import Operator, RiskScore

router = APIRouter(prefix="/risk", tags=["risk"])


@router.get("", summary="Fetch all operator risk scores")
async def get_risk_scores(db: AsyncSession = Depends(get_db)) -> list[dict]:
    query = (
        select(Operator, RiskScore)
        .join(RiskScore, RiskScore.operator_id == Operator.id)
        .order_by(desc(RiskScore.updated_at))
    )
    result = await db.execute(query)

    rows: list[dict] = []
    for operator, score in result.all():
        rows.append(
            {
                "operator_id": operator.id,
                "name": operator.name,
                "type": operator.type,
                "location": operator.location,
                "risk_score": score.score,
                "updated_at": score.updated_at.isoformat() if score.updated_at else None,
            }
        )

    return rows
