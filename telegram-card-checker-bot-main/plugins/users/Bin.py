import re
import csv
import os
import requests

from pyrogram import filters
from pyromod import Client
from pyrogram.types import Message

from utilsdf.db import Database
from utilsdf.functions import get_text_from_pyrogram
from utilsdf.vars import PREFIXES

# ✅ FUNCIÓN PARA BUSCAR EN CSV (adaptada a tu formato)
def search_bin_in_csv(bin_number):
    """Busca información del BIN en el archivo CSV"""
    # Obtener la ruta del directorio actual del script
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_file = os.path.join(current_dir, "bin.csv")
    
    if not os.path.exists(csv_file):
        print(f"Archivo CSV no encontrado en: {csv_file}")
        return None
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['number'] == bin_number:
                    return {
                        'brand': row['vendor'],
                        'type': row['type'] if row['type'] else "UNAVAILABLE",
                        'level': row['level'] if row['level'] else "UNAVAILABLE",
                        'bank': row['bank'],
                        'country': row['country'],
                        'country_code': row['country'],  # Tu CSV no tiene código separado
                        'emoji': row['flag']
                    }
        return None
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return None

@Client.on_message(filters.command("bin", PREFIXES))
async def bin_f(client: Client, m: Message):
    user_id = m.from_user.id

    with Database() as db:
        if not db.is_authorized(user_id, m.chat.id):
            return await m.reply(
                "𝑻𝒉𝒊𝒔 𝒄𝒉𝒂𝒕 𝒊𝒔 𝒏𝒐𝒕 𝒂𝒑𝒑𝒓𝒐𝒗𝒆𝒅 𝒕𝒐 𝒖𝒔𝒆 𝒕𝒉𝒊𝒔 𝒃𝒐𝒕.",
                quote=True
            )

        user_info = db.get_info_user(user_id)

    text = get_text_from_pyrogram(m)

    if not text:
        return await m.reply(
            "♻️ Format → <code>/bin 541590</code>",
            quote=True
        )

    bin_match = re.search(r"\d{6}", text)

    if not bin_match:
        return await m.reply("⚠️ Invalid BIN", quote=True)

    BIN = bin_match.group()

    # 🔎 Buscar en CSV
    bin_info = search_bin_in_csv(BIN)

    if bin_info:
        vendor = bin_info["brand"]
        typea = bin_info["type"]
        level = bin_info["level"]
        bank = bin_info["bank"]
        country = bin_info["country"]
        code = bin_info["country_code"]
        emoji = bin_info["emoji"]
    else:
        # fallback API
        try:
            req = requests.get(
                f"https://lookup.binlist.net/{BIN}",
                timeout=10
            ).json()

            vendor = req.get("brand", "Unknown")
            typea = req.get("type", "Unknown")
            level = req.get("prepaid", "Unknown")

            bank = req.get("bank", {}).get("name", "Unknown")

            country = req.get("country", {}).get("name", "Unknown")
            code = req.get("country", {}).get("alpha2", "XX")
            emoji = req.get("country", {}).get("emoji", "🏳️")

        except Exception as e:
            print(f"API Error: {e}")
            return await m.reply("❌ BIN not found", quote=True)

    rol = user_info["RANK"].capitalize()
    nick = user_info["NICK"]

    await m.reply(
        f"""<b>
 〔 𝙑𝘼𝙇𝙄𝘿 𝘽𝙄𝙉 〕

⧉  𝘽𝙄𝙉      ⇢ <code>{BIN}</code>
⧉  𝙄𝙉𝙁𝙊     ⇢ <code>{vendor} ⨯ {typea} ⨯ {level}</code>
⧉  𝘽𝘼𝙉𝙆     ⇢ <code>{bank}</code>
⧉  𝘾𝙊𝙐𝙉𝙏𝙍𝙔  ⇢ <code>{country} | {code} | {emoji}</code>

𝘾𝙝𝙚𝙘𝙠𝙚𝙙 <a href='tg://user?id={m.from_user.id}'>{m.from_user.first_name}</a> [{rol}] -» <code>{nick}</code>

</b>""",
        quote=True
    )