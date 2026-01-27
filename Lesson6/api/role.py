from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from repositories.roles import RoleRepository
from schemas.role import RoleCreate, RoleRead
from services.roles import RoleService

role_router = APIRouter(prefix="/roles", tags=["roles"])


@role_router.post("/create", response_model=RoleRead)
async def create_role(
        role_create: RoleCreate,
        db: Session = Depends(get_db)
):
    service = RoleService(RoleRepository())

    try:
        return service.create_role(db, role_create)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@role_router.get("/{name}", response_model=RoleRead)
async def get_role_by_name(
        name: str, db:
        Session = Depends(get_db)
):
    service = RoleService(RoleRepository())
    try:
        return service.find_role_by_name(db, name)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@role_router.put("/{role_id}/id", response_model=RoleRead)
async def update_role_by_id(
        role_id: int,
        db: Session = Depends(get_db)
):
    service = RoleService(RoleRepository())
    try:
        return service.find_role_by_id(db, role_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))