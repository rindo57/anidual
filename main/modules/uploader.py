import asyncio

import os

import time
import random
import pixeldrain

import aiohttp

import requests

import aiofiles

from main.modules.utils import format_time, get_duration, get_epnum, get_filesize, status_text, tags_generator, get_messages, b64_to_str, str_to_b64, send_media_and_reply, get_durationx

from main.modules.anilist import get_anime_name

from main.modules.anilist import get_anime_img

from main.modules.db import present_user, add_user, is_fid_in_db, save_file_in_db

from main.modules.thumbnail import generate_thumbnail

from config import UPLOADS_ID

from pyrogram import Client, filters

from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, InputMediaVideo, InputMediaAudio, InputMediaDocument

from main.modules.progress import progress_for_pyrogram

from os.path import isfile

import os

import time

from main import app, status

from pyrogram.errors import FloodWait

from main.inline import button1

async def upload_video(msg: Message, file, id, tit, name, ttl, main, subtitle, nyaasize):
    try:
        fuk = isfile(file)
        if fuk:
            r = msg
            c_time = time.time()
            duration = get_duration(file)
            durationx = get_durationx(file)
            size = get_filesize(file)
            ep_num = get_epnum(name)
            rest = tit
            filed = os.path.basename(file)
            print('filed: ', filed)
            filed = filed.replace("[1080p Web-DL]", "[Web][720p x265 10Bit][Opus][Erai-raws]")
            fukpath = "downloads/" + filed
            caption = f"{filed}"

            kayo_id = -1001373634390
            gay_id = 1159872623
            upid = int(main.id)
            print(upid)
            x = await app.edit_message_media(
                chat_id=kayo_id,
                message_id=upid,
                media=InputMediaDocument(file),
                file_name=filed
            )
            await asyncio.sleep(3)
            hash = "".join([random.choice(ascii_letters + digits) for n in range(50)])
            await save_file_in_db(filed, hash, upid)
            gcaption = f"`{filed}: https://robot.anidlserverv1.me.in/beta/{hash}`" + "\n" + f"__({tit})__" + "\n" + "━━━━━━━━━━━━━━━━━━━" + "\n" + f"- **Subtitle**: `{subtitle}`"
            await x.edit_caption(gcaption)
    except Exception:
        await app.send_message(kayo_id, text="Something Went Wrong!")


    try:
        
            
            await r.delete()

            os.remove(file)

            os.remove(thumbnail)

    except:

        pass

    return x.id
