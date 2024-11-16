import asyncio
from bs4 import BeautifulSoup
import os
from string import ascii_letters, digits
import time
import random
import pixeldrain

import aiohttp

import requests

import aiofiles

from main.modules.utils import format_time, get_duration, get_epnum, get_filesize, status_text, tags_generator, get_messages, b64_to_str, str_to_b64, send_media_and_reply, get_durationx

from main.modules.anilist import get_anime_name

from main.modules.anilist import get_anime_img

from main.modules.db import present_user, add_user, is_fid_in_db, save_file_in_db, save_postid, get_postid, save_link480p, get_link480p, save_link720p, get_link720p, save_link1080p,  get_size480p,  get_size720p,  save_size480p, save_size720p

from main.modules.thumbnail import generate_thumbnail

from config import UPLOADS_ID

from pyrogram import Client, filters, enums

from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, InputMediaVideo, InputMediaAudio, InputMediaDocument

from main.modules.progress import progress_for_pyrogram

from os.path import isfile

import os

import time

from main import app, status

from pyrogram.errors import FloodWait

from main.inline import button1
import re
def extract_source(filename):
    pattern = r"\[Web ~ (.*?)\]"
    match = re.search(pattern, filename)
    if match:
        source = match.group(1)
        return source
    else:
        return None

async def upload_video(msg: Message, title, file, tit, name, ttl, main, subtitle, nyaasize, audio_info):

    
    try:
        fuk = isfile(file)
        if fuk:
            r = msg
            c_time = time.time()
            duration = get_duration(file)
            durationx = get_durationx(file)
            
            size480p = get_filesize(file)
            ep_num = get_epnum(name)
            print(ep_num)
            print("name: ", name)
            rest = tit
            filed = os.path.basename(file)
            print('filed: ', filed)
            source = extract_source(filed)
            print("src: ", source)
            anidltitle = filed.replace("[AniDL] ", "")
            anidltitle = anidltitle.replace(" [Web ~ AMZN][480p x265 10Bit][Dual-Audio ~ Opus].mkv", "")
            anidltitle = anidltitle.replace(" [Web ~ CR][480p x265 10Bit][Dual-Audio ~ Opus].mkv", "")
            anidltitle = anidltitle.replace(" [Web ~ HIDIVE][480p x265 10Bit][Dual-Audio ~ Opus].mkv", "")
            anidltitle = anidltitle.replace(" [Web ~ DSNP][480p x265 10Bit][Dual-Audio ~ Opus].mkv", "")
            anidltitle = anidltitle.replace(" [Web ~ HMAX][480p x265 10Bit][Dual-Audio ~ Opus].mkv", "")
            anidltitle = anidltitle.replace(" [Web ~ YouDeer][480p x265 10Bit][Dual-Audio ~ Opus].mkv", "")
            anidltitle = anidltitle.replace(" [Web ~ REPACK AMZN][480p x265 10Bit][Dual-Audio ~ Opus].mkv", "")
            anidltitle = anidltitle.replace(" [Web ~ MAX][480p x265 10Bit][Dual-Audio ~ Opus].mkv", "")
            anidltitle = anidltitle.replace(" [Web ~ NF][480p x265 10Bit][Dual-Audio ~ Opus].mkv", "")
            fukpath = "downloads/" + filed
            caption = f"{filed}"

            kayo_id = -1001895203720
            gay_id = 1159872623
            
    
            x = await app.send_document(
                kayo_id,
                file,
                file_name=filed,
                progress=progress_for_pyrogram,
                progress_args=(
                    filed,
                    r,
                    c_time,
                    ttl
            )
            )
            upid = int(x.id)
            print(upid)
            await asyncio.sleep(3)
            hash = "".join([random.choice(ascii_letters + digits) for n in range(50)])
            print("hash1:", hash)
            save_file_in_db(filed, hash, subtitle, audio_info, tit, size480p, upid)
            print(hash)
            ddlurl = f"https://anidl.ddlserverv1.me.in/beta/{hash}"
            gcaption = f"`📺 {filed}`\n\n`🔗 EP - {ep_num}:  https://anidl.ddlserverv1.me.in/beta/{hash}`" + "\n\n" + f"🔠 __{tit}__" + "\n" + "\n" + f"📝 `{subtitle}`"
            """cfurl = "http://localhost:8191/v1"
            headers = {"Content-Type": "application/json"}
            dataz = {
                "cmd": "request.get",
                "url": f"http://ouo.press/api/jezWr0hG?s={ddlurl}",
                "maxTimeout": 60000
            }
            responsez = requests.post(cfurl, headers=headers, json=dataz)
            html_content = responsez.json()['solution']['response']
            soup = BeautifulSoup(html_content, 'html.parser')"""
            ourl =  f"http://ouo.io/api/jezWr0hG?s={ddlurl}"
            resp = requests.get(ourl)
            extracted_url = resp.text
            print(extracted_url)
            da_url = "https://da.gd/"
            shorten_url = f"{da_url}shorten"
            response = requests.post(shorten_url, params={"url": extracted_url})
            flink = response.text.strip()
            
            print("title upload: ", title)
            save_link480p(title, flink)
            dl_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="🔗 Download Link", url=f"https://anidl.ddlserverv1.me.in/beta/{hash}")
                    ]
                ]
            )
            await app.edit_message_caption(
                chat_id=kayo_id,
                message_id=upid,
                caption=gcaption
            )
            await asyncio.sleep(3)
          
            anidl_id=-1001234112068
            xurl = f"https://anidl.ddlserverv1.me.in/beta/{hash}"
            anidlcap = f"<b>{anidltitle}</b>\n<i>({tit})</i>\n<blockquote><b><a href={flink}>🗂️ [Web ~ {source}][480p x265 10Bit CRF@23][JAP/ENG ~ Opus][Multiple Subs ~ {subtitle}]</a></b> || <code>{size480p}</code></blockquote>\n#airing #dual_audio #multi_subs"
            save_size480p(title, size480p)
            fmarkup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="🔗 480p",
                                url=flink,
                            ),
                        ],
                        [
                            InlineKeyboardButton(
                                text="🌐 AIRING ANIME",
                                url="https://anidl.org/airing-anime",
                            ),
                        ],
                        
                    ],
            )
            anidl_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="🔗 VISIT PAGE", url=f"https://anidl.org/airing-anime")
                    ]
                ]
            )
            await asyncio.sleep(3)
            post = await app.send_message(anidl_id,text=anidlcap, reply_markup=fmarkup, parse_mode=enums.ParseMode.HTML)
            postid = post.id
            print("title upload: ", title)
            save_postid(title, postid)
    except Exception:
        await app.send_message(kayo_id, text="Something Went Wrong!")


    try:
        
            
            await r.delete()

            os.remove(file)

            os.remove(thumbnail)

    except:

        pass

    return x.id

async def upload_video720p(msg: Message, title, file, tit, name, ttl, main, subtitle, nyaasize, audio_info):

    try:
        fuk = isfile(file)
        if fuk:
            r = msg
            c_time = time.time()
            duration = get_duration(file)
            durationx = get_durationx(file)
            size720p = get_filesize(file)
            ep_num = get_epnum(name)
            print(ep_num)
            rest = tit
            filed = os.path.basename(file)
            print('filed: ', filed)
            source = extract_source(filed)
            print('filed: ', filed)
            anidltitle = filed.replace("[AniDL] ", "")
            anidltitle = anidltitle.replace(" [Web ~ AMZN][720p x265 10Bit][Dual-Audio ~ Opus].mkv", "")
            anidltitle = anidltitle.replace(" [Web ~ CR][720p x265 10Bit][Dual-Audio ~ Opus].mkv", "")
            anidltitle = anidltitle.replace(" [Web ~ HIDIVE][720p x265 10Bit][Dual-Audio ~ Opus].mkv", "")
            anidltitle = anidltitle.replace(" [Web ~ DSNP][720p x265 10Bit][Dual-Audio ~ Opus].mkv", "")
            anidltitle = anidltitle.replace(" [Web ~ HMAX][720p x265 10Bit][Dual-Audio ~ Opus].mkv", "")
            anidltitle = anidltitle.replace(" [Web ~ YouDeer][720p x265 10Bit][Dual-Audio ~ Opus].mkv", "")
            anidltitle = anidltitle.replace(" [Web ~ REPACK AMZN][720p x265 10Bit][Dual-Audio ~ Opus].mkv", "")
            anidltitle = anidltitle.replace(" [Web ~ MAX][720p x265 10Bit][Dual-Audio ~ Opus].mkv", "")
            anidltitle = anidltitle.replace(" [Web ~ NF][720p x265 10Bit][Dual-Audio ~ Opus].mkv", "")
            fukpath = "downloads/" + filed
            caption = f"{filed}"

            kayo_id = -1001895203720
            gay_id = 1159872623
        
            x = await app.send_document(
                kayo_id,
                file,
                file_name=filed,
                progress=progress_for_pyrogram,
                progress_args=(
                    filed,
                    r,
                    c_time,
                    ttl
            )
            )
            upid = int(x.id)
            print(upid)
            await asyncio.sleep(3)
            hash = "".join([random.choice(ascii_letters + digits) for n in range(50)])
            save_file_in_db(filed, hash, subtitle, audio_info, tit, size720p, upid)
            print(hash)
            ddlurl = f"https://anidl.ddlserverv1.me.in/beta/{hash}"
            gcaption = f"`📺 {filed}`\n\n`🔗 EP - {ep_num}:  https://anidl.ddlserverv1.me.in/beta/{hash}`" + "\n\n" + f"🔠 __{tit}__" + "\n" + "\n" + f"📝 `{subtitle}`"
            ourl =  f"http://ouo.io/api/jezWr0hG?s={ddlurl}"
            resp = requests.get(ourl)
            extracted_url = resp.text
            print(extracted_url)
            da_url = "https://da.gd/"
            shorten_url = f"{da_url}shorten"
            response = requests.post(shorten_url, params={"url": extracted_url})
            fxlink = response.text.strip()
            
            save_link720p(title, fxlink)
            dl_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="🔗 Download Link", url=f"https://anidl.ddlserverv1.me.in/beta/{hash}")
                    ]
                ]
            )
            await app.edit_message_caption(
                chat_id=kayo_id,
                message_id=upid,
                caption=gcaption
            )
            await asyncio.sleep(3)
           
            anidl_id=-1001234112068
            print("check: ", title)
            code480p = await get_link480p(title)
            size480p = await get_size480p(title)
            dl480pcap = f"<b>{anidltitle}</b>\n<i>({tit})</i>\n<blockquote><b><a href={code480p}>🗂️ [Web ~ {source}][480p x265 10Bit CRF@23][JAP/ENG ~ Opus][Multiple Subs ~ {subtitle}]</a></b> || <code>{size480p}</code></blockquote>"
            anidlcap2 = dl480pcap + "\n" + f"<blockquote><b><a href={fxlink}>🗂️ [Web ~ {source}][720p x265 10Bit CRF@22][JAP/ENG ~ Opus][Multiple Subs ~ {subtitle}]</a></b> || <code>{size720p}</code></blockquote>\n#airing #dual_audio #multi_subs"
            save_size720p(title, size720p)
            fmarkup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="🔗 480p",
                                url=code480p,
                            ),
                            InlineKeyboardButton(
                                text="🔗 720p",
                                url=fxlink,
                            ),
                        ],
                        [
                            InlineKeyboardButton(
                                text="🌐 AIRING ANIME",
                                url="https://anidl.org/airing-anime",
                            ),
                        ],
                        
                    ],
            )
            await asyncio.sleep(3)
            postid = await get_postid(title)
            print(postid)
            await app.edit_message_text(anidl_id, postid, text=anidlcap2, reply_markup=fmarkup, parse_mode=enums.ParseMode.HTML)
    except Exception as e:
        await app.send_message(kayo_id, text="Something Went Wrong!" + "\n" + e)
    try:
        
            
            await r.delete()

            os.remove(file)

            os.remove(thumbnail)

    except:

        pass

async def upload_video1080p(msg: Message, title, file, tit, name, ttl, main, subtitle, nyaasize, audio_info):

    try:
        fuk = isfile(file)
        if fuk:
            r = msg
            c_time = time.time()
            duration = get_duration(file)
            durationx = get_durationx(file)
            size1080p = get_filesize(file)
            ep_num = get_epnum(name)
            print(ep_num)
            rest = tit
            filed = os.path.basename(file)
            source = extract_source(filed)
            print('filed: ', filed)
            anidltitle = filed.replace("[AniDL] ", "")
            anidltitle = anidltitle.replace(" [Web ~ AMZN][1080p x265 10Bit][Dual-Audio ~ AAC].mkv", "")
            anidltitle = anidltitle.replace(" [Web ~ CR][1080p x265 10Bit][Dual-Audio ~ AAC].mkv", "")
            anidltitle = anidltitle.replace(" [Web ~ HIDIVE][1080p x265 10Bit][Dual-Audio ~ AAC].mkv", "")
            anidltitle = anidltitle.replace(" [Web ~ DSNP][1080p x265 10Bit][Dual-Audio ~ AAC].mkv", "")
            anidltitle = anidltitle.replace(" [Web ~ HMAX][1080p x265 10Bit][Dual-Audio ~ AAC].mkv", "")
            anidltitle = anidltitle.replace(" [Web ~ YouDeer][1080p x265 10Bit][Dual-Audio ~ AAC].mkv", "")
            anidltitle = anidltitle.replace(" [Web ~ REPACK AMZN][1080p x265 10Bit][Dual-Audio ~ AAC].mkv", "")
            anidltitle = anidltitle.replace(" [Web ~ MAX][1080p x265 10Bit][Dual-Audio ~ AAC].mkv", "")
            anidltitle = anidltitle.replace(" [Web ~ NF][1080p x265 10Bit][Dual-Audio ~ AAC].mkv", "")
            fukpath = "downloads/" + filed
            caption = f"{filed}"

            kayo_id = -1001895203720
            gay_id = 1159872623
            upid = int(main.id)
         
            x = await app.send_document(
                kayo_id,
                file,
                file_name=filed,
                progress=progress_for_pyrogram,
                progress_args=(
                    filed,
                    r,
                    c_time,
                    ttl
            )
            )
            upid = int(x.id)
            print(upid)
            await asyncio.sleep(3)
            hash = "".join([random.choice(ascii_letters + digits) for n in range(50)])
            save_file_in_db(filed, hash, subtitle, audio_info, tit, size1080p, upid)
            print(hash)
            ddlurl = f"https://anidl.ddlserverv1.me.in/beta/{hash}"
            gcaption = f"`📺 {filed}`\n\n`🔗 EP - {ep_num}:  https://anidl.ddlserverv1.me.in/beta/{hash}`" + "\n\n" + f"🔠 __{tit}__" + "\n" + "\n" + f"📝 `{subtitle}`"
            ourl =  f"http://ouo.io/api/jezWr0hG?s={ddlurl}"
            resp = requests.get(ourl)
            extracted_url = resp.text
            print(extracted_url)
            da_url = "https://da.gd/"
            shorten_url = f"{da_url}shorten"
            response = requests.post(shorten_url, params={"url": extracted_url})
            fxylink = response.text.strip()
            
            save_link1080p(title, fxylink)
            dl_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="🔗 Download Link", url=f"https://anidl.ddlserverv1.me.in/beta/{hash}")
                    ]
                ]
            )
            await app.edit_message_caption(
                chat_id=kayo_id,
                message_id=upid,
                caption=gcaption
            )
            await asyncio.sleep(3)
         
            anidl_id=-1001234112068
            code480p = await get_link480p(title)
            print(code480p)
            code720p = await get_link720p(title)
            print(code720p)
            size480p = await get_size480p(title)
            size720p = await get_size720p(title)
            dl480pcap = f"<b>{anidltitle}</b>\n<i>({tit})</i>\n<blockquote><b><a href={code480p}>🗂️ [Web ~ {source}][480p x265 10Bit CRF@23][JAP/ENG ~ Opus][Multiple Subs ~ {subtitle}]</a></b> || <code>{size480p}</code></blockquote>"
            dl720pcap = f"\n<blockquote><b><a href={code720p}>🗂️ [Web ~ {source}][720p x265 10Bit CRF@22][JAP/ENG ~ Opus][Multiple Subs ~ {subtitle}]</a></b> || <code>{size720p}</code></blockquote>"
            anidlcap3 = dl480pcap + dl720pcap + "\n" + f"<blockquote><b><a href={fxylink}>🗂️ [Web ~ {source}][1080p x265 10Bit CRF@22][JAP/ENG ~ AAC][Multiple Subs ~ {subtitle}]</a></b> || <code>{size1080p}</code></blockquote>\n#airing #dual_audio #multi_subs"
            fmarkup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="🔗 480p",
                                url=code480p,
                            ),
                            InlineKeyboardButton(
                                text="🔗 720p",
                                url=code720p,
                            ),
                            InlineKeyboardButton(
                                text="🔗 1080p",
                                url=fxylink,
                            ),
                        ],
                        [
                            InlineKeyboardButton(
                                text="🌐 AIRING ANIME",
                                url="https://anidl.org/airing-anime",
                            ),
                        ],
                        
                    ],
            )
            fmarkup2=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="🔗 480p",
                                url=code480p,
                            ),
                            InlineKeyboardButton(
                                text="🔗 720p",
                                url=code720p,
                            ),
                            InlineKeyboardButton(
                                text="🔗 1080p",
                                url=fxylink,
                            ),
                        ],
                        [   
                            InlineKeyboardButton(
                                text="🍅",
                                url="https://t.me/TomClicker_bot/TomClicker?startapp=1425489930",
                            ),
                            InlineKeyboardButton(
                                text="🌐 AIRING ANIME",
                                url="https://anidl.org/airing-anime",
                            ),
                        
                        ],
                        
                    ],
            )
            await asyncio.sleep(3)
            print("title upload: ", title)
            postid = await get_postid(title)
            print(postid)
            ongid = -1001159872623
            await app.edit_message_text(anidl_id, postid, text=anidlcap3, reply_markup=fmarkup, parse_mode=enums.ParseMode.HTML)
            await asyncio.sleep(3)
            await app.copy_message(
                chat_id=ongid,
                from_chat_id=anidl_id,
                message_id=postid,
                reply_markup=fmarkup2
            )
    except Exception as e:
        await app.send_message(kayo_id, text="Something Went Wrong!" + "\n" + e)
    try:
        
            
            await r.delete()

            os.remove(file)

            os.remove(thumbnail)

    except:

        pass

    return x.id
