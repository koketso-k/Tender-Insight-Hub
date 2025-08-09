from fastapi import APIRouter

router = APIRouter()

@router.get("/tenders")
def list_tenders():
    return {"tenders": ["Tender 1", "Tender 2", "Tender 3"]}
