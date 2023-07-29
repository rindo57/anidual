import asyncio

import os

import time

import pixeldrain

import aiohttp

import requests

import aiofiles

from main.modules.utils import format_time, get_duration, get_epnum, get_filesize, status_text, tags_generator, get_messages, b64_to_str, str_to_b64, send_media_and_reply, get_durationx

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

async def upload_video(msg: Message,file,id,tit,name,ttl,sourcetext,untext,subtitle,nyaasize):

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

            thumbnail = await generate_thumbnail(id,file)

            filed = os.path.basename(file)

            filed = filed.replace("[1080p Web-DL]", "[720p x265] @animxt")

            fukpath = "downloads/" + filed

            caption = f"{filed}"

            caption = caption.replace("[720p x265] @animxt.mkv", "") 

            gcaption=f"**{caption}**" + "\n" +  f"__({tit})__" + "\n" + "━━━━━━━━━━━━━━━━━━━" + "\n" + "✓  `720p x265 10Bit`" + "\n" + f"✓  `{subtitle} ~ Subs`" + "\n" + "#Encoded #HEVC"

            kayo_id = -1001642923224

            gay_id = 1159872623

            x = await app.send_document(

                kayo_id,

            document=file,

            caption=gcaption,

            file_name=filed,

            force_document=True,

                

            thumb=thumbnail

            )

            os.rename(file,fukpath)

            server = requests.get(url="https://api.gofile.io/getServer").json()["data"]["server"]

            uploadxz = requests.post(url=f"https://{server}.gofile.io/uploadFile", files={"upload_file": open(fukpath, 'rb')}).json()

            directlink = uploadxz["data"]["downloadPage"]

            da_url = "https://da.gd/"

            gotn_urlx = f"https://tnshort.net/api?api=fea911843f6e7bec739708f3e562b56184342089&url={directlink}&format=text"

            gofinalx = requests.get(gotn_urlx)

            go_textx = gofinalx.text

            gourlx = go_textx

            gofile_urlx = f"{da_url}shorten"

            goresponsex = requests.get(gofile_urlx, params={"url": gourlx})

            gofuk_textx = goresponsex.text.strip()
            repz = pixeldrain.upload_file(fukpath)
            if repz["success"]:              
                datax = pixeldrain.info(repz["id"])   
            else:
                print("Failed!")
            ddl = f"https://pixeldrain.com/api/file/{datax['id']}"
            pxtn_urlx = f"https://tnshort.net/api?api=fea911843f6e7bec739708f3e562b56184342089&url={ddl}&format=text"

            pxfinalx = requests.get(pxtn_urlx)

            px_textx = pxfinalx.text

            pxurlx = px_textx

            pxfile_urlx = f"{da_url}shorten"

            pxresponsex = requests.get(pxfile_urlx, params={"url": pxurlx})

            pxfuk_textx = pxresponsex.text.strip()
 
            file_er_id = str(x.message_id)

            share_link = f"https://telegram.me/somayukibot?start=animxt_{str_to_b64(file_er_id)}"            

            enshare_link = f"https://tnlinks.in/api?api=1458ad61946fd6f5b8a93161c9cfd94733813566&url={share_link}&format=text"

            fukshare = requests.get(enshare_link)

            tshare = fukshare.text

            cshare = tshare

            xshare_url = f"{da_url}shorten"

            tgshare = requests.get(xshare_url, params={"url": cshare})

            teleshare = tgshare.text.strip()            

            repl_markup=InlineKeyboardMarkup(

                [

                    [

                         InlineKeyboardButton(

                            text="🐌TG FILE",

                            url=teleshare,

                        ),

                         InlineKeyboardButton(

                              text="🚀GoFile",

                              url=gofuk_textx,

                        ),
  
                    ],
                    [
                        InlineKeyboardButton(
                            text="🚀Pixeldrain",
                            url=pxfuk_textx,
                        ),
                    ],
                ],
            )

            encodetext =  f"{sourcetext}" "\n" + f"**‣ File Size**: `{size}`" + "\n" + f"**‣ Duration**: {durationx}" + "\n" + f"**‣ Downloads**: [🔗Telegram File]({teleshare}) [🔗Gofile]({gofuk_textx}) [🔗Pixeldrain]({pxfuk_textx})"

            await asyncio.sleep(5)

            entext = await untext.edit(encodetext, disable_web_page_preview=True, reply_markup=repl_markup)

    except Exception:

            await app.send_message(kayo_id, text="Something Went Wrong!")

    try:

            await r.delete()

            os.remove(file)

            os.remove(thumbnail)

    except:

        pass

    return x.message_id
