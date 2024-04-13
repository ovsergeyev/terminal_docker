from fastapi import FastAPI
from pydantic import BaseModel
from classes.Terminal import Terminal
from classes.Crypto import Crypto
from schemas.STerminalEvent import STerminalEvent
# from fastapi.middleware.cors import CORSMiddleware
import uuid

app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

class SStartWords(BaseModel):
  words: list[str]

class SAddWord(BaseModel):
  session_id: str
  word: str
  count: int

class SCreateMetamask(BaseModel):
  sid: str
  address: str
  password: str

class SComplete(BaseModel):
  address: str
  points: int
  winrate: str

@app.post("/complete_akk")
async def complete_akk(payload: SComplete):
  await Terminal.complete_akk(payload.address, payload.points, payload.winrate)

@app.post("/start_session")
async def start_session(payload: SStartWords):
  id = str(uuid.uuid4())
  terminal = Terminal(id)
  terminal.add_words(payload.words)
  word = terminal.get_word()
  return {
    "id": id,
    "word": word
  }

@app.post("/add_word")
async def add_word(payload: SAddWord):
  id = payload.session_id
  word = payload.word
  count = payload.count
  terminal = Terminal(id)
  terminal.add_word(word, count)
  result_word = terminal.get_word()
  return {
    "id": id,
    "word": result_word
  }

@app.get('/register_akks')
async def register_akks(count: int):
  await Terminal.register_akks(count)

@app.get('/set_akk_proxy')
async def set_akk_proxy(metamask_address: str, proxy: str):
  await Terminal.set_akk_proxy(metamask_address, proxy)

@app.get('/clear_akk_proxy')
async def clear_akk_proxy(metamask_address: str):
  await Terminal.clear_akk_proxy(metamask_address)

@app.get('/clear_proxies')
async def clear_proxies():
  await Terminal.clear_akks_proxies()

@app.get("/get_terminal_akk")
async def get_terminal_akk(address: str=None):
  if not address:
    return await Terminal.get_akk()
  else:
    return await Terminal.get_test_akk(address)

@app.post("/send_terminal_event")
async def send_terminal_event(event: STerminalEvent):
  await Terminal.add_event(event)

@app.post("/create_metamask")
async def create_metamask(payload: SCreateMetamask):
  crypto = Crypto()
  await crypto.add_metamask(payload.sid, payload.address, payload.password)

