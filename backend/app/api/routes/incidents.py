from fastapi import APIRouter

router = APIRouter()


@router.get("/", summary="Placeholder endpoint")
def placeholder():
    return {"message": "Not implemented yet"}
