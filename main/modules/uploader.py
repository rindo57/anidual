import asyncio
import os
import time
import aiohttp
import requests
import aiofiles


from main.modules.utils import format_time, get_duration, get_epnum, get_filesize, status_text, tags_generator, get_messages, b64_to_str, str_to_b64, send_media_and_reply

from main.modules.anilist import get_anime_name

from main.modules.anilist import get_anime_img

from main.modules.db import present_user, add_user
from main.modules.thumbnail import generate_thumbnail

from config import UPLOADS_ID

from pyrogram import Client, filters

from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from main.modules.progress import progress_for_pyrogram

from os.path import isfile

import os

import time

from main import app, status

from pyrogram.errors import FloodWait

from main.inline import button1

async def upload_video(msg: Message,file,id,tit,name,ttl):

    try:

    

        fuk = isfile(file)

        if fuk:

            r = msg

            c_time = time.time()

            duration = get_duration(file)

            size = get_filesize(file)

            ep_num = get_epnum(name)
            
            rest = tit

            thumbnail = await generate_thumbnail(id,file)

            tags = tags_generator(tit)

            buttons = InlineKeyboardMarkup([

                [

                    InlineKeyboardButton(text="Info", url="https://t.me/AnimeXT"),

                    InlineKeyboardButton(text="Comments", url=f"https://t.me/ANIMECHATTERBOX")

                ]

            ])
            filed = os.path.basename(file)
            filed = filed.replace("(1080p)", "[720p x265]")
            fukpath = "downloads/" + filed
            caption = f"{name}"
            caption = caption.replace("(1080p)", "") 
            gcaption=f"**{caption}**" + "\n" + "✓  `720p x265 10Bit`" + "\n" + "✓  `English Sub`" + "\n" + f"__({tit})__" + "\n" + "#Encoded #HEVC"
            kayo_id = -1001948444792
            linkx_id = -1001578240792
            x = await app.send_document(

                kayo_id,

            document=file,

            caption=gcaption,

            file_name=filed,

            force_document=True,
                
            thumb=thumbnail,

            progress=progress_for_pyrogram,
 
            progress_args=(

                os.path.basename(file),

                r,

                c_time,

                ttl

            )

            )             
            file_er_id = str(x.id)
            share_link = f"https://t.me/zoroloverobot?start=animxt_{str_to_b64(file_er_id)}"
            CH_edit = await app.edit_message_reply_markup(kayo_id, x.message_id,
                                                          reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(
                                                              "Telegram File", url=share_link)]]))
    except Exception:
            await app.send_message(kayo_id, text="Something Went Wrong!")
    try:

            await r.delete()

            os.remove(file)

            os.remove(thumbnail)

    except:

        pass

    return x.message_id

@app.on_message(filters.command("start") & filters.private)
async def start(bot, cmd: Message):
    usr_cmd = cmd.text.split("_", 1)[-1]
    if usr_cmd == "/start":
       await cmd.reply_text("Yo baka!")
    else:
        try:
            try:
                file_id = int(b64_to_str(usr_cmd).split("_")[-1])
            except (Error, UnicodeDecodeError):
                file_id = int(usr_cmd.split("_")[-1])
            GetMessage = await bot.get_messages(kayo_id, message_ids=file_id)
            message_ids = []
            if GetMessage.text:
                message_ids = GetMessage.text.split(" ")
                _response_msg = await cmd.reply_text(
                    text=f"**Total Files:** `{len(message_ids)}`",
                    quote=True,
                    disable_web_page_preview=True
                )
            else:
                message_ids.append(int(GetMessage.id))
            for i in range(len(message_ids)):
                await send_media_and_reply(bot, user_id=cmd.from_user.id, file_id=int(message_ids[i]))
        except Exception as err:
            await cmd.reply_text(f"Something went wrong!\n\n**Error:** `Bitch`")
