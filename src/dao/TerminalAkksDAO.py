from dao.BaseDAO import BaseDAO
from database import async_session_maker
from sqlalchemy import select, insert, delete, text, update
from models.TerminalAcountModel import TerminalAcountModel
from schemas.STerminalAkk import STerminalAkk
from datetime import datetime

class TerminalAkksDAO(BaseDAO):
    model = TerminalAcountModel

    @classmethod
    async def update(cls, terminal_akk:STerminalAkk):
        async with async_session_maker() as session:
            query = update(cls.model).where(cls.model.address==terminal_akk.address).values(
                address=terminal_akk.address,
                proxy=terminal_akk.proxy,
                is_completed=terminal_akk.is_completed,
                issued=terminal_akk.issued,
                winrate=terminal_akk.winrate,
                points=terminal_akk.points,
                created_at=terminal_akk.created_at,
                updated_at=terminal_akk.updated_at,
            )
            await session.execute(query)
            await session.commit()

    # @classmethod
    # async def get_gender_by_name(cls, name):
    #     result = None
    #     if not name:
    #         return result

    #     name_str = name.replace(' ', '')
    #     if name:
    #         # print('name', name)
    #         try:
    #             res = await cls.find_one_or_none(name=name_str.lower())
    #         except:
    #             res = None
    #         # print('res', res)
    #         if res:
    #             result = res.get('gender', None)

    #         if result:
    #             result = result.upper()

    #     return result