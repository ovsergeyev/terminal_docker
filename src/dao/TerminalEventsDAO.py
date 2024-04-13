from dao.BaseDAO import BaseDAO
from database import async_session_maker
from sqlalchemy import select, insert, delete, text, update
from models.TerminalEventModel import TerminalEventModel
from datetime import datetime

class TerminalEventsDAO(BaseDAO):
    model = TerminalEventModel

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