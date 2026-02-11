from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.routes import admin, analytics, assets, auth, incidents, organizations, reports, risk_scores
from .core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(assets.router, prefix=f"{settings.API_V1_STR}/assets", tags=["assets"])
app.include_router(
    organizations.router,
    prefix=f"{settings.API_V1_STR}/organizations",
    tags=["organizations"],
)
app.include_router(
    risk_scores.router,
    prefix=f"{settings.API_V1_STR}/risk-scores",
    tags=["risk-scores"],
)
app.include_router(incidents.router, prefix=f"{settings.API_V1_STR}/incidents", tags=["incidents"])
app.include_router(reports.router, prefix=f"{settings.API_V1_STR}/reports", tags=["reports"])
app.include_router(
    analytics.router,
    prefix=f"{settings.API_V1_STR}/analytics",
    tags=["analytics"],
)
app.include_router(admin.router, prefix=f"{settings.API_V1_STR}/admin", tags=["admin"])


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Oil & Gas Risk Intelligence API", "version": settings.VERSION}


@app.get(f"{settings.API_V1_STR}/health")
async def health_check() -> dict[str, str]:
    return {"status": "healthy"}
