from sqlalchemy.orm import Session
from sqlalchemy import select, func
from typing import List
import json

from app.config import settings
from app.models.planner import Planner
from app.redis_client import redis_client
from app.schemas.planner import PlannerResponse, PlannerUpdate, PlannerCreate


class PlannerService:
    def get_all_planners_from_db(self, db: Session) -> List[Planner]:
        return db.scalars(select(Planner).where(Planner.deleted_at.is_(None))).all()

    def get_all_planners(self, db: Session) -> List[Planner]:
        cached_date = redis_client.get("planners")
        if cached_date:
            return [Planner(**item) for item in json.loads(cached_date)]

        planners = self.get_all_planners_from_db(db)
        planners_response_data = [PlannerResponse.model_validate(c).model_dump(mode='json') for c in planners]
        redis_client.setex("planners", settings.REDIS_CACHE_EXPIRE_SECONDS, json.dumps(planners_response_data))

        return planners

    def update(self, db: Session, db_planner: Planner, req: PlannerUpdate) ->  Planner:
        update_data = req.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_planner, field, value)

        db.add(db_planner)
        db.commit()
        db.refresh(db_planner)

        redis_client.delete("planners")

        return db_planner

    def destroy(self, db: Session, id: int) -> bool:
        planner = db.scalars(select(Planner).where(Planner.id == id)).first()
        if not planner:
            return False

        planner.deleted_at = func.now()

        db.add(planner)
        db.commit()
        db.refresh(planner)

        redis_client.delete("planners")

        return True

    def create_planner(self, db: Session, req: PlannerCreate) -> Planner:
        db_planner = Planner(**req.model_dump())
        db.add(db_planner)
        db.commit()
        db.refresh(db_planner)

        redis_client.delete("planners")
        return db_planner
