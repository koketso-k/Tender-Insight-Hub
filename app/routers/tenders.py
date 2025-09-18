from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import crud, models, schemas, database

router = APIRouter(prefix="/tenders", tags=["tenders"])
get_db = database.get_db

@router.post("/", response_model=schemas.TenderOut)
def create_tender(tender: schemas.TenderCreate, db: Session = Depends(get_db)):
    return crud.create_tender(db, tender)

@router.get("/", response_model=List[schemas.TenderOut])
def list_tenders(team_id: int, db: Session = Depends(get_db)):
    return crud.get_tenders(db, team_id)

@router.get("/{tender_id}", response_model=schemas.TenderOut)
def read_tender(tender_id: int, db: Session = Depends(get_db)):
    db_tender = crud.get_tender(db, tender_id)
    if not db_tender:
        raise HTTPException(status_code=404, detail="Tender not found")
    return db_tender

@router.put("/{tender_id}", response_model=schemas.TenderOut)
def update_tender(tender_id: int, tender: schemas.TenderUpdate, db: Session = Depends(get_db)):
    db_tender = crud.update_tender(db, tender_id, tender)
    if not db_tender:
        raise HTTPException(status_code=404, detail="Tender not found")
    return db_tender

@router.delete("/{tender_id}", response_model=schemas.TenderOut)
def delete_tender(tender_id: int, db: Session = Depends(get_db)):
    db_tender = crud.delete_tender(db, tender_id)
    if not db_tender:
        raise HTTPException(status_code=404, detail="Tender not found")
    return db_tender
