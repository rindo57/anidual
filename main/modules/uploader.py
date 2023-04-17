import asyncio
import os
import time
import aiohttp
import requests
import aiofiles

from main.modules.utils import format_time, get_duration, get_epnum, get_filesize, status_text, tags_generator, encode, decode, get_messages

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
            
            converted_id = x.message_id * abs(kayo_id)
            string = f"get-{converted_id}"
            base64_string = await encode(string)
            link = f"https://t.me/zoroloverobot?start={base64_string}"
            await app.send_message(kayo_id,text={link})
    except Exception:
            await app.send_message(kayo_id, text="Something Went Wrong!")
@app.on_message(filters.command('start') & filters.private)
async def start_command(client: Client, message: Message):
    id = message.from_user.id
    if not await present_user(id):
        try:
            await add_user(id)
        except:
            pass
    text = message.text
    if len(text)>7:
        try:
            base64_string = text.split(" ", 1)[1]
        except:
            return
        string = await decode(base64_string)
        argument = string.split("-")
        if len(argument) == 3:
            try:
                start = int(int(argument[1]) / abs(kayo_id))
                end = int(int(argument[2]) / abs(kayo_id))
            except:
                return
            if start <= end:
                ids = range(start,end+1)
            else:
                ids = []
                i = start
                while True:
                    ids.append(i)
                    i -= 1
                    if i < end:
                        break
        elif len(argument) == 2:
            try:
                ids = [int(int(argument[1]) / abs(kayo_id))]
            except:
                return
        temp_msg = await message.reply("Please wait...")
        try:
            messages = await get_messages(app, ids)
        except:
            await message.reply_text("Something went wrong..!")
            return
        await temp_msg.delete()

        for msg in messages:


            try:
                await msg.copy(chat_id=message.from_user.id, caption = "@animxt", parse_mode = ParseMode.HTML)
                await asyncio.sleep(0.5)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await msg.copy(chat_id=message.from_user.id, caption = "@animxt", parse_mode = ParseMode.HTML)
            except:
                pass
        return
    else:
        await message.reply_text(text="Fuk error!")
    try:

            await r.delete()

            os.remove(file)
            
            os.remove(fukpath)

            os.remove(thumbnail)

    except:

        pass

    return x.message_id
