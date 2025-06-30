from fastapi import APIRouter, Depends, HTTPException, status, Form, File, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import List, Optional, Union
import json
from app.database.connection import get_db
from app.schemas.planner import PlannerResponse, PlannerCreate, PlannerUpdate
from app.services.planner_service import PlannerService

from app.security import get_current_active_user
from app.models.planner import Planner
from app.models.user import User

router = APIRouter(
    prefix="/planners",
    tags=["planners"]
)

planner_service = PlannerService()

@router.get("/", response_model=List[PlannerResponse])
async def index(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    planners = planner_service.get_all_planners(db)
    return planners

@router.post("/", response_model=PlannerResponse, status_code=status.HTTP_201_CREATED)
async def store(req: PlannerCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    planner_create_data = PlannerCreate(recipe_id=req.recipe_id, user_id=current_user.id, date=req.date)
    planner = planner_service.create_planner(db, planner_create_data)
    return planner

@router.put("/{id}", response_model=PlannerResponse, status_code=status.HTTP_200_OK)
async def update(id: int, req: PlannerUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    existing_planner = db.scalars(select(Planner).where(Planner.id == id)).first()
    if not existing_planner:
        raise HTTPException(status_code=404, detail="Plan not found")
    planner = planner_service.update(db, existing_planner, req)
    return planner

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def destroy(id: int, db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    deleted = planner_service.destroy(db, id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Plan with id {id} not found")
    return