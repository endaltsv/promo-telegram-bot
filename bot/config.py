import os

from aiogram import Dispatcher, Bot, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

from bot.middlewares.delete_message import DeleteMessageMiddleware
from bot.middlewares.update_user import UserUpdateMiddleware


load_dotenv()
TOKEN = os.getenv("TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

dp = Dispatcher()
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

router = Router()
router.message.middleware(UserUpdateMiddleware())
router.message.middleware(DeleteMessageMiddleware())

form_router = Router()
support_router = Router()
dp.include_router(form_router)
dp.include_router(support_router)


dp.include_router(router)
