from typing import List
from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from bojojo.models.Scheduled_Run import ScheduledRun
from bojojo.repositories import repository


class ScheduledRunRepository(repository):

    def __init__(self, session: Session):
        self.session = session    

    
    def get(self, id: int) -> ScheduledRun:
        try:
            return self.session.execute(select(ScheduledRun).where(ScheduledRun.id==id)).scalars().first()
        except SQLAlchemyError as e:
            raise e
        
    
    def getAll(self) -> List[ScheduledRun]:
        try:
            return self.session.execute(select(ScheduledRun)).scalars().all()
        except SQLAlchemyError as e:
            raise e
        
    
    def add(self, scheduleRun: ScheduledRun) -> ScheduledRun:
        try:
            nw_run = self.session.execute(
                insert(ScheduledRun)
                .values(
                    creation_date=scheduleRun.creation_date,
                    job_title_id=scheduleRun.job_title_id,
                    job_board_id=scheduleRun.job_board_id,
                    run_date=scheduleRun.run_date,
                    run_time=scheduleRun.run_time,
                    run_type=scheduleRun.run_type,
                    recurring=scheduleRun.recurring,
                    easy_apply_only=scheduleRun.easy_apply_only
                )
                .returning(ScheduledRun)
            )
            self.session.commit()
            return nw_run
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        
    
    def update(self, scheduledRun: ScheduledRun) -> ScheduledRun:
        try:
            results = self.session.execute(
                update(ScheduledRun)
                .where(ScheduledRun.id==scheduledRun.id)
                .values(
                    creation_date=scheduledRun.creation_date,
                    job_title_id=scheduledRun.job_title_id,
                    job_board_id=scheduledRun.job_board_id,
                    run_date=scheduledRun.run_date,
                    run_time=scheduledRun.run_time,
                    run_type=scheduledRun.run_type,
                    recurring=scheduledRun.recurring,
                    easy_apply_only=scheduledRun.easy_apply_only
                )
                .returning(ScheduledRun)
            )
            self.session.commit()
            return results
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        
    
    def delete(self, scheduledRun: ScheduledRun) -> ScheduledRun:
        try:
            result = self.session.execute(delete(ScheduledRun).where(ScheduledRun.id==scheduledRun.id).returning(ScheduledRun))
            self.session.commit()
            return result
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e