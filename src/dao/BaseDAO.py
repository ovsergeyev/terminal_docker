from sqlalchemy import select, insert, delete, text, update
from database import async_session_maker
from datetime import datetime

class BaseDAO:
    model = None

    # @classmethod
    # async def find_by_id(cls, model_id: int):
    #     async with async_session_maker() as session:
    #         query = select(cls.model.__table__.columns).filter_by(id=model_id)
    #         result = await session.execute(query)
    #         return result.mappings().one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data).returning(cls.model.id)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def delete_by_uid(cls, uid):
        async with async_session_maker() as session:
            query = delete(cls.model).where(cls.model.uid==uid)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def set_updated_at_by_uid(cls, uid, updated_at=None):
        if not updated_at:
            updated_at = datetime.utcnow()

        async with async_session_maker() as session:
            query = update(cls.model).where(uid==uid).values(updated_at=updated_at)
            await session.execute(query)
            await session.commit()


    @classmethod
    async def text_query(cls, sql):
        async with async_session_maker() as session:
            result = await session.execute(text(sql))
            await session.commit()
            return result.mappings().all()
