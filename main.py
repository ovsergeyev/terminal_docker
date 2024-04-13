import asyncio
from app.classes.Crypto import Crypto
from app.classes.Terminal import Terminal
from app.schemas.STerminalEvent import STerminalEvent
from rich import print
from datetime import datetime


async def tasks():
    crypto = Crypto()
    # await crypto.check_metamask_duplicate()
    # await crypto.add_metamask('this is sid', 'this is pass')
    # terminal = Terminal()
    # await Terminal.register_akks(50)
    await Terminal.set_akks_proxy()
    await Terminal.clear_akks_proxy()
    # await Terminal.get_akk()
    # event = STerminalEvent(
    #     address="test",
    #     type="testType",
    #     message="что то там добавил",
    #     created_at=datetime.now()
    # )
    # await Terminal.add_event(event)



asyncio.get_event_loop().run_until_complete(tasks())
