from dao.BaseDAO import BaseDAO
from models.MetaMaskModel import MetaMaskModel

class MetaMaskDAO(BaseDAO):
    model = MetaMaskModel

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