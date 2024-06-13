import asyncio

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

from main.modules.db import present_user, add_user, is_fid_in_db, save_file_in_db, save_postid, get_postid, save_link480p, get_link480p, save_link720p, get_link720p, save_link1080p

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
async def upload_video(msg: Message, img, file, id, tit, name, ttl, main, subtitle, nyaasize, audio_info, alink):
    
    try:
        fuk = isfile(file)
        if fuk:
            r = msg
            c_time = time.time()
            duration = get_duration(file)
            durationx = get_durationx(file)
            size = get_filesize(file)
            ep_num = get_epnum(name)
            print(ep_num)
            rest = tit
            filed = os.path.basename(file)
            print('filed: ', filed)
            anidltitle = filed.replace("[AniDL] ", "")
            anidltitle = anidltitle.replace("[1080p Web-DL].mkv", "")
            filed = filed.replace("[1080p Web-DL]", "[Web][480p x265 10Bit][Opus][Erai-raws]")
            fukpath = "downloads/" + filed
            caption = f"{filed}"

            kayo_id = -1001895203720
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
            save_file_in_db(filed, hash, subtitle, img, audio_info, tit, alink, size, upid)
            print(hash)
            ddlurl = f"https://anidl.ddlserverv1.me.in/beta/{hash}"
            gcaption = f"`📺 {filed}`\n\n`🔗 EP - {ep_num}:  https://anidl.ddlserverv1.me.in/beta/{hash}`" + "\n\n" + f"🔠 __{tit}__" + "\n" + "\n" + f"📝 `{subtitle}`"
            da_url = "https://da.gd/"
            shorten_url = f"{da_url}shorten"
            response = requests.post(shorten_url, params={"url": ddlurl})
            dalink = response.text.strip()
            dalink = dalink.replace("https://", "")
            dalink = dalink.replace("http://", "")
            ouolink = f"http://ouo.press/qs/jezWr0hG?s={dalink}"
            ulvis = f"https://ulvis.net/api.php?url={ouolink}&private=1"
            result = requests.get(ulvis)
            flink = result.text
            save_link480p(name, flink)
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
            await app.edit_message_reply_markup(
                chat_id=kayo_id,
                message_id=upid,
                reply_markup=dl_markup
            )
            anidl_id=-1001234112068
            xurl = f"https://anidl.ddlserverv1.me.in/beta/{hash}"
            anidlcap = f"<b>{anidltitle}</b>\n<i>{tit}</i>\n<blockquote><b><a href={flink}>🗂️ [Web ~ Erai-raws][480p x265 10Bit CRF@23][JAP ~ Opus][Multiple Subs ~ {subtitle}]</a></b></blockquote>"
            
            fmarkup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="480p",
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
            print("name: ", name)
            save_postid(name, postid)
    except Exception:
        await app.send_message(kayo_id, text="Something Went Wrong!")


    try:
        
            
            await r.delete()

            os.remove(file)

            os.remove(thumbnail)

    except:

        pass

    return x.id

async def upload_video720p(msg: Message, img, file, id, tit, name, ttl, main, subtitle, nyaasize, audio_info, alink):
    global anidlcap2, fxlink
    try:
        fuk = isfile(file)
        if fuk:
            r = msg
            c_time = time.time()
            duration = get_duration(file)
            durationx = get_durationx(file)
            size = get_filesize(file)
            ep_num = get_epnum(name)
            print(ep_num)
            rest = tit
            filed = os.path.basename(file)
            print('filed: ', filed)
            anidltitle = filed.replace("[AniDL] ", "")
            anidltitle = anidltitle.replace("[1080p Web-DL].mkv", "")
            filed = filed.replace("[1080p Web-DL]", "[Web][720p x265 10Bit][Opus][Erai-raws]")
            fukpath = "downloads/" + filed
            caption = f"{filed}"

            kayo_id = -1001895203720
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
            save_file_in_db(filed, hash, subtitle, img, audio_info, tit, alink, size, upid)
            print(hash)
            ddlurl = f"https://anidl.ddlserverv1.me.in/beta/{hash}"
            gcaption = f"`📺 {filed}`\n\n`🔗 EP - {ep_num}:  https://anidl.ddlserverv1.me.in/beta/{hash}`" + "\n\n" + f"🔠 __{tit}__" + "\n" + "\n" + f"📝 `{subtitle}`"
            da_url = "https://da.gd/"
            shorten_url = f"{da_url}shorten"
            response = requests.post(shorten_url, params={"url": ddlurl})
            dalink = response.text.strip()
            dalink = dalink.replace("https://", "")
            dalink = dalink.replace("http://", "")
            ouolink = f"http://ouo.press/qs/jezWr0hG?s={dalink}"
            ulvis = f"https://ulvis.net/api.php?url={ouolink}&private=1"
            result = requests.get(ulvis)
            fxlink = result.text
            save_link720p(name, fxlink)
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
            await app.edit_message_reply_markup(
                chat_id=kayo_id,
                message_id=upid,
                reply_markup=dl_markup
            )
            anidl_id=-1001234112068
            filex = filed.replace("[AniDL] ", "")
            name480p = filex.replace("[Web][720p x265 10Bit][Opus][Erai-raws]", "[1080p Web-DL]")
            code480p = await get_link480p(name480p)
            dl480pcap = f"<b>{anidltitle}</b>\n<i>{tit}</i>\n<blockquote><b><a href={code480p}>🗂️ [Web ~ Erai-raws][480p x265 10Bit CRF@23][JAP ~ Opus][Multiple Subs ~ {subtitle}]</a></b></blockquote>"
            dl720pcap = f"\n<blockquote><b><a href={code720p}>🗂️ [Web ~ Erai-raws][720p x265 10Bit CRF@22][JAP ~ Opus][Multiple Subs ~ {subtitle}]</a></b></blockquote>"
            anidlcap2 = dl480p + "\n" + f"<blockquote><b><a href={fxlink}>🗂️ [Web ~ Erai-raws][720p x265 10Bit CRF@22][JAP ~ Opus][Multiple Subs ~ {subtitle}]</a></b></blockquote>"
            fmarkup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="480p",
                                url=code480p,
                            ),
                            InlineKeyboardButton(
                                text="720p",
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
            postid = await get_postid(name)
            await app.edit_message_text(anidl_id, postid, text=anidlcap2, reply_markup=fmarkup, parse_mode=enums.ParseMode.HTML)
    except Exception:
        await app.send_message(kayo_id, text="Something Went Wrong!")
    try:
        
            
            await r.delete()

            os.remove(file)

            os.remove(thumbnail)

    except:

        pass

async def upload_video1080p(msg: Message, img, file, id, tit, name, ttl, main, subtitle, nyaasize, audio_info, alink):
    
    try:
        fuk = isfile(file)
        if fuk:
            r = msg
            c_time = time.time()
            duration = get_duration(file)
            durationx = get_durationx(file)
            size = get_filesize(file)
            ep_num = get_epnum(name)
            print(ep_num)
            rest = tit
            filed = os.path.basename(file)
            print('filed: ', filed)
            anidltitle = filed.replace("[AniDL] ", "")
            anidltitle = anidltitle.replace("[1080p Web-DL].mkv", "")
            filed = filed.replace("[1080p Web-DL]", "[Web][1080p x265 10Bit][AAC][Erai-raws]")
            fukpath = "downloads/" + filed
            caption = f"{filed}"

            kayo_id = -1001895203720
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
            save_file_in_db(filed, hash, subtitle, img, audio_info, tit, alink, size, upid)
            print(hash)
            ddlurl = f"https://anidl.ddlserverv1.me.in/beta/{hash}"
            gcaption = f"`📺 {filed}`\n\n`🔗 EP - {ep_num}:  https://anidl.ddlserverv1.me.in/beta/{hash}`" + "\n\n" + f"🔠 __{tit}__" + "\n" + "\n" + f"📝 `{subtitle}`"
            da_url = "https://da.gd/"
            shorten_url = f"{da_url}shorten"
            response = requests.post(shorten_url, params={"url": ddlurl})
            dalink = response.text.strip()
            dalink = dalink.replace("https://", "")
            dalink = dalink.replace("http://", "")
            ouolink = f"http://ouo.press/qs/jezWr0hG?s={dalink}"
            ulvis = f"https://ulvis.net/api.php?url={ouolink}&private=1"
            result = requests.get(ulvis)
            fxylink = result.text
            save_link1080p(name, fxylink)
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
            await app.edit_message_reply_markup(
                chat_id=kayo_id,
                message_id=upid,
                reply_markup=dl_markup
            )
            anidl_id=-1001234112068
            filex = filed.replace("[AniDL] ", "")
            name480p = filex.replace("[Web][1080p x265 10Bit][AAC][Erai-raws]", "[1080p][Multiple Subtitle]")
            name720p = filex.replace("[Web][1080p x265 10Bit][AAC][Erai-raws]", "[1080p][Multiple Subtitle]")
            code480p = await get_link480p(name480p)
            code720p = await get_link720p(name720p)
            dl480pcap = f"<b>{anidltitle}</b>\n<i>{tit}</i>\n<blockquote><b><a href={code480p}>🗂️ [Web ~ Erai-raws][480p x265 10Bit CRF@23][JAP ~ Opus][Multiple Subs ~ {subtitle}]</a></b></blockquote>"
            dl720pcap = f"\n<blockquote><b><a href={code720p}>🗂️ [Web ~ Erai-raws][720p x265 10Bit CRF@22][JAP ~ Opus][Multiple Subs ~ {subtitle}]</a></b></blockquote>"
            anidlcap3 = dl480pcap + dl720pcap + "\n" + f"<blockquote><b><a href={fxylink}>🗂️ [Web ~ Erai-raws][1080p x265 10Bit CRF@22][JAP ~ AAC][Multiple Subs ~ {subtitle}]</a></b></blockquote>"
            fmarkup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="480p",
                                url=code480p,
                            ),
                            InlineKeyboardButton(
                                text="720p",
                                url=code720p,
                            ),
                            InlineKeyboardButton(
                                text="1080p",
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
            await asyncio.sleep(3)
            print("name: ", name)
            postid = await get_postid(name)
            await app.edit_message_text(anidl_id, postid, text=anidlcap3, reply_markup=fmarkup, parse_mode=enums.ParseMode.HTML)
    except Exception:
        await app.send_message(kayo_id, text="Something Went Wrong!")
    try:
        
            
            await r.delete()

            os.remove(file)

            os.remove(thumbnail)

    except:

        pass

    return x.id
