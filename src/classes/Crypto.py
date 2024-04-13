from dao.MetaMaskDAO import MetaMaskDAO
from schemas.SMetaMask import SMetaMask
from datetime import datetime
from rich import print

class Crypto:
  def __init__(self):
    pass

  async def check_metamask_duplicate(self):
    wallets = await MetaMaskDAO.find_all()
    error_wallets = []
    addresses = set()
    for wallet in wallets:
      if wallet["address"] in addresses:
        error_wallets.append(wallet["address"])
      addresses.add(wallet["address"])
    print(error_wallets)

  async def add_metamask(self, sid, address, password):
    exist_akk = await MetaMaskDAO.find_one_or_none(address=address)
    if not exist_akk and address and sid and password:
      metamask = SMetaMask(
        sid=sid,
        address=address,
        password=password,
        created_at=datetime.now(),
        updated_at=datetime.now()
      )

      await MetaMaskDAO.add(
        sid=metamask.sid,
        address=metamask.address,
        password=metamask.password,
        created_at=metamask.created_at,
        updated_at=metamask.updated_at
      )