import pymongo
from dao.MetaMaskDAO import MetaMaskDAO
from dao.TerminalAkksDAO import TerminalAkksDAO
from dao.TerminalEventsDAO import TerminalEventsDAO
from schemas.STerminalAkk import STerminalAkk
from schemas.STerminalEvent import STerminalEvent, TerminalEventEnum
from rich import print
from datetime import datetime, timedelta
from os import environ

# {
#   "id": 0,
#   "words": [],
#   "error_words": [],
#   "revision": 0
# }

class Terminal:
  def __init__(self, id):
    self.id = id
    self.client = pymongo.MongoClient(environ['MONGO_URI'])
    self.words = []
    self.error_words = []
    self.revision = self.init_session()
    print("revision", self.revision)
    print("words", self.words)
    print("error words", self.error_words)

  def init_session(self):
    revision = 0
    query = {
      "id": self.id
    }
    response = None
    try:
      response = self.client.terminal.words.find_one(query, sort=[("revision", -1)])
      revision = response['revision'] + 1
      self.words = response['words']
      self.error_words = response['error_words']
    except:
      pass
    print(response)
    # result = None
    # response = self.client.terminal.words.find(query).sort({"revision": -1}).limit(1)
    # for el in response:
    #   result = el
    # print(result)
    # if not result:
    #   print('this is test')
    return revision
  
  @classmethod
  async def complete_akk(cls, address, points, winrate):
    akks = await TerminalAkksDAO.find_all()
    akk = None
    for el in akks:
      if el["address"] == address:
        akk = el
        break

    terminal_akk = STerminalAkk(
      address=akk.address,
      proxy=akk.proxy,
      is_completed=True,
      issued=akk.issued,
      winrate=int(winrate.replace("%", "")),
      points=points,
      created_at=akk.created_at,
      updated_at=datetime.now(),
    )

    await TerminalAkksDAO.update(terminal_akk)

    event = STerminalEvent(
      address=address,
      type=TerminalEventEnum.COMPLETE.value,
      message="Аккаунт обработан"
    )

    await cls.add_event(event)

  @classmethod
  async def get_akk(cls):
    result = {
      "address": None,
      "sid": None,
      "password": None,
      "proxy": None
    }
    akks = await TerminalAkksDAO.find_all()
    for akk in akks:
      issued_date = None
      time_diff = None
      if akk['issued']:
        issued_date = akk['issued'].date()
        time_diff = datetime.now() - akk['issued']
        if not akk["is_completed"]:
          print("!!!!!!!!!!!!!!!", time_diff)
      if (not issued_date or time_diff > timedelta(hours=25)) or (not akk["is_completed"] and time_diff > timedelta(minutes=10)):
        print(akk["address"])
        wallet = await MetaMaskDAO.find_one_or_none(address=akk["address"])
        result["address"] = akk["address"]
        result["sid"] = wallet["sid"]
        result["password"] = wallet["password"]
        result["proxy"] = akk["proxy"]

        terminal_akk = STerminalAkk(
            address=akk.address,
            proxy=akk.proxy,
            is_completed=False,
            issued=datetime.now(),
            winrate=akk.winrate,
            points=akk.points,
            created_at=akk.created_at,
            updated_at=datetime.now(),
        )

        await TerminalAkksDAO.update(terminal_akk)

        event = STerminalEvent(
          address=akk.address,
          type=TerminalEventEnum.ISSUE.value,
          message="Выдан аккаунт"
        )

        await cls.add_event(event)
        break
    return result

  #test akk - 0x06c89C1fc5bc66d59c40eC0eeeeC65068a192253

  @classmethod
  async def get_test_akk(cls, address):
    result = {
      "address": None,
      "sid": None,
      "password": None,
      "proxy": None
    }
    akks = await TerminalAkksDAO.find_all()
    for akk in akks:
      if akk["address"] == address:
        wallet = await MetaMaskDAO.find_one_or_none(address=akk["address"])
        result["address"] = akk["address"]
        result["sid"] = wallet["sid"]
        result["password"] = wallet["password"]
        result["proxy"] = akk["proxy"]

        break
    return result

  @classmethod
  async def add_event(cls, event:STerminalEvent):
    await TerminalEventsDAO.add(
      address=event.address,
      type=event.type,
      message=event.message,
      created_at=datetime.now()
    )

  @classmethod
  async def set_akk_proxy(cls, metamask_address, proxy):
    akk = await TerminalAkksDAO.find_one_or_none(address=metamask_address)
    akk = STerminalAkk(
      address=akk["address"],
      proxy=proxy,
      is_completed=akk["is_completed"],
      issued=akk["issued"],
      winrate=akk["winrate"],
      points=akk["points"],
      created_at=akk["created_at"],
      updated_at=datetime.now()
    )
    await TerminalAkksDAO.update(akk)

  @classmethod
  async def clear_akk_proxy(cls, metamask_address):
    akk = await TerminalAkksDAO.find_one_or_none(address=metamask_address)
    akk = STerminalAkk(
      address=akk["address"],
      proxy=None,
      is_completed=akk["is_completed"],
      issued=akk["issued"],
      winrate=akk["winrate"],
      points=akk["points"],
      created_at=akk["created_at"],
      updated_at=datetime.now()
    )
    await TerminalAkksDAO.update(akk)

  @classmethod
  async def clear_akks_proxies(cls):
    all_akks = await TerminalAkksDAO.find_all()
    for akk in all_akks:
      if akk["proxy"]:
        akk = STerminalAkk(
          address=akk["address"],
          proxy=None,
          is_completed=akk["is_completed"],
          issued=akk["issued"],
          winrate=akk["winrate"],
          points=akk["points"],
          created_at=akk["created_at"],
          updated_at=datetime.now()
        )
        await TerminalAkksDAO.update(akk)

  @classmethod
  async def register_akks(cls, limit=None):
    wallets = await MetaMaskDAO.find_all()
    count = 0
    for wallet in wallets:
      if limit and count == limit:
        break
      existed_akk = await TerminalAkksDAO.find_one_or_none(address=wallet["address"])
      # print(existed_akk)
      if not existed_akk:
        count += 1
        akk = STerminalAkk(
          address=wallet["address"],
          proxy=None,
          is_completed=None,
          issued=None,
          winrate=None,
          points=None,
          created_at=datetime.now(),
          updated_at=datetime.now()
        )
        await TerminalAkksDAO.add(
          address=akk.address,
          proxy=akk.proxy,
          is_completed=akk.is_completed,
          issued=akk.issued,
          winrate=akk.winrate,
          points=akk.points,
          created_at=akk.created_at,
          updated_at=akk.updated_at,
        )

  def add_words(self, words):
    self.words = words
    self.__save_session()

  def __save_session(self):
    db_words = {
      "id": self.id,
      "words": self.words,
      "error_words": self.error_words,
      "revision": self.revision
    }
    self.client.terminal.words.insert_one(db_words)
    self.revision += 1

  def add_word(self, word, count):
    words = []
    error_words = []
    word_dict = self.__get_word_dict()
    for key in word_dict.keys():
      if key == word:
        error_words.append(key)
        continue
      print(word_dict[key])
      if self.__diff_words(word, key) == count:
        words.append(key)
      else:
        error_words.append(key)
    self.words = words
    self.error_words = error_words
    self.__save_session()
    print('words', words)
    print('error_words', error_words)

  def get_word(self):
    score_dict = self.__get_score_dict()
    max_score = 0
    result = None
    for key in score_dict.keys():
      if max_score < score_dict[key]:
        max_score = score_dict[key]
        result = key
    return result

  def __get_score_dict(self):
    word_dict = self.__get_word_dict()
    score_dict = {}
    for key in word_dict.keys():
      score = 0
      params = word_dict[key]
      for el in params:
        if el:
          score +=1
      score_dict[key] = score
    print(score_dict)
    return score_dict

  def __get_word_dict(self):
    word_dict = {}
    for word in self.words:
      params = self.__check_word(word)
      word_dict[word] = params
    print(word_dict)
    return word_dict

  def __check_word(self, word):
    params = []
    for el in self.words:
      if el == word:
        param = '-'
      else:
        param = self.__diff_words(word, el)
      params.append(param)
    return params

  def __diff_words(self, word1, word2):
    score = 0
    position = 0
    for letter in word1:
      if letter == word2[position]:
        score += 1
      position +=1

    return score