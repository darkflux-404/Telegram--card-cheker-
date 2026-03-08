import logging
from os import getenv
from huepy import bad
from pyromod import Client
from pyrogram import filters
from pyrogram.enums import ParseMode, ChatMemberStatus
from pyrogram.types import CallbackQuery, Message
from utilsdf.functions import bot_on
from utilsdf.db import Database
from utilsdf.vars import PREFIXES

# 🔹 Cargar variables de entorno
API_ID = getenv('TELEGRAM_API_ID')
API_HASH = getenv('TELEGRAM_API_HASH')
BOT_TOKEN = getenv('TELEGRAM_BOT_TOKEN')
CHANNEL_LOGS = getenv('TELEGRAM_CHANNEL_LOGS')  # opcional

# 🔹 Validaciones básicas
if not API_ID or not API_HASH or not BOT_TOKEN:
    raise ValueError("Faltan variables de entorno obligatorias en Replit Secrets")

API_ID = int(API_ID)  # convertir a int solo después de validar

# 🔹 Inicializar el cliente Pyrogram
app = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="plugins"),
    parse_mode=ParseMode.HTML,
)

bot_on()
logging.basicConfig(level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.CRITICAL)


# 🔹 Callback queries
@app.on_callback_query()
async def warn_user(client: Client, callback_query: CallbackQuery):
    if callback_query.message.reply_to_message.from_user and (
        callback_query.from_user.id
        != callback_query.message.reply_to_message.from_user.id
    ):
        await callback_query.answer("Usa tu menu! ⚠️", show_alert=True)
        return
    await callback_query.continue_propagation()


# 🔹 Manejo de mensajes de usuarios
@app.on_message(filters.text)
async def user_ban(client: Client, m: Message):

    if not m.from_user or not m.text:
        return

    try:
        if not m.text[0] in PREFIXES:
            return
    except UnicodeDecodeError:
        return

    chat_id = m.chat.id
    with Database() as db:
        if chat_id == -1001494650944:
            async for member in m.chat.get_members():
                if not member.user:
                    continue
                if member.status == ChatMemberStatus.ADMINISTRATOR:
                    continue
                user_id = member.user.id
                if db.is_seller_or_admin(user_id):
                    continue
                is_premium = db.is_premium(user_id)
                if is_premium:
                    continue
                if db.user_has_credits(user_id):
                    continue
                await m.chat.ban_member(user_id)
                info = db.get_info_user(user_id)
                
                # 🔹 Enviar logs solo si CHANNEL_LOGS existe
                if CHANNEL_LOGS:
                    await client.send_message(CHANNEL_LOGS, f"<b>User eliminado: @{info['USERNAME']}</b>")

        user_id = m.from_user.id
        username = m.from_user.username
        db.remove_expireds_users()
        banned = db.is_ban(user_id)
        if banned:
            return
        db.register_user(user_id, username)
        await m.continue_propagation()


# 🔹 Ejecutar bot
if __name__ == "__main__":
    app.run()