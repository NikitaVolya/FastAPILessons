from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.session import get_db
from repositories.departaments import DepartamentRepository
from schemas.departament import DepartamentRead, DepartamentCreate
from services.departaments import DepartamentService

departament_router = APIRouter(prefix="/departaments", tags=["departaments"])


@departament_router.post("/create", response_model=DepartamentRead)
async def create_departament(
        departament: DepartamentCreate,
        db: Session = Depends(get_db),
):
    service = DepartamentService(DepartamentRepository())
    try:
        return service.register(db, departament)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@departament_router.get("/{id}", response_model=DepartamentRead)
async def get_departament_by_id(
        id: int,
        db: Session = Depends(get_db),
):
    service = DepartamentService(DepartamentRepository())
    try:
        return service.find_departament_by_id(db, id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@departament_router.get("/name/{name}", response_model=DepartamentRead)
async def get_departament_by_name(
        name: str,
        db: Session = Depends(get_db),
):
    service = DepartamentService(DepartamentRepository())
    try:
        return service.find_departament_by_name(db, name)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@departament_router.get("", response_model=List[DepartamentRead])
async def get_departaments(
        db: Session = Depends(get_db)
):
    service = DepartamentService(DepartamentRepository())
    return service.get_all(db)