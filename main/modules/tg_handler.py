
import asyncio
import time
import aiohttp
import requests
import aiofiles
import sys
from main.modules.compressor import compress_video, compress_video720p, compress_video1080p
from pymediainfo import MediaInfo

from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from main.modules.utils import episode_linker, get_duration, get_epnum, status_text, get_filesize, b64_to_str, str_to_b64, send_media_and_reply, get_durationx, extract_title
from main.modules.uploader import upload_video, upload_video720p, upload_video1080p
from main.modules.thumbnail import generate_thumbnail

import os

from main.modules.db import del_anime, save_uploads, is_fid_in_db, is_tit_in_db, save_480p, save_720p, save_1080p, del_progress, pending_720p, pending_1080p, no_pending

from main.modules.downloader import downloader

from main.modules.anilist import get_anilist_data, get_anime_img, get_anime_name

from config import INDEX_USERNAME, UPLOADS_USERNAME, UPLOADS_ID, INDEX_ID, PROGRESS_ID, LINK_ID

from main import app, queue, status

from pyrogram.errors import FloodWait

from pyrogram import filters, enums

from main.inline import button1

status: Message

async def tg_handler():

    while True:

        try:
            if len(queue) != 0:

                i = queue[0]  

                i = queue.pop(0)
                
                name, video = await start_uploading(i)
                print("Title: ", i["title"])
                await del_anime(i["title"])
                await save_uploads(i["title"])
                await asyncio.sleep(30)


            else:                

                if "Idle..." in status.text:

                    try:

                        await status.edit(await status_text("Idle..."))

                    except:

                        pass

                await asyncio.sleep(30)

                

        except FloodWait as e:

            flood_time = int(e.x) + 5

            try:

                await status.edit(await status_text(f"Floodwait... Sleeping For {flood_time} Seconds"))

            except:

                pass

            await asyncio.sleep(flood_time)

        except:

            pass

def replace_text_with_mapping(subtitle, mapping):
    for original_text, replacement_text in mapping.items():
        subtitle = subtitle.replace(original_text, replacement_text)
    return subtitle


mapping = {
    "us": "ENG",
    "br": "POR-BR",
    "mx": "SPA-LA",
    "es": "SPA",
    "sa": "ARA",
    "fr": "FRE",
    "de": "GER",
    "it": "ITA",
    "ru": "RUS",
    "ja": "JPN",
    "pt": "POR",
    "pl": "POL",
    "nl": "DUT",
    "nb": "NOB",
    "fi": "FIN",
    "tr": "TUR",
    "sv": "SWE",
    "el": "GRE",
    "he": "HEB",
    "ro": "RUM",
    "id": "IND",
    "th": "THA",
    "ko": "KOR",
    "da": "DAN",
    "zh": "CHI",
    "bg": "BUL",
    "vn": "VIE",
    "hi": "HIN",
    "te": "TEL",
    "uk": "UKR",
    "hu": "HUN",
    "cs": "CES",
    "hr": "HRV",
    "my": "MAY",
    "sk": "SLK",
    "fil": "FIL",
    "cn": "CHI",
    "jp": "JAP",
    "no": "NOB",
    "se": "SWE",
    "gr": "GRE",
    "kr": "KOR",
    "dk": "DAN",
    "cz": "CES",
    "ph": "FIL",
    "UA": "UKR"
    
}

def get_audio_languages(video_path):
    try:
        media_info = MediaInfo.parse(video_path)
        audio_tracks = []
        for track in media_info.tracks:
            if track.track_type == 'Audio':
                audio_tracks.append(track.language)
        return audio_tracks
    except Exception as e:
        print(f"Error: {e}")
        return None
        

async def start_uploading(data):

    try:
        if data["uploaded"]=='0':
            title = data["title"]
            entitle = data["entitle"]
            dbtit = data["title"]
            link = data["link"]
            size = data["size"]
            size = size.replace("GB", " GiB")
            nyaasize = size
            subtitl = data["subtitle"]
            subtitle = replace_text_with_mapping(subtitl, mapping)
            name, ext = title.split(".")

            name += f" [AniDL]." + ext

            KAYO_ID =  -1001895203720
            uj_id = 1159872623
            DATABASE_ID = -1001895203720
            bin_id = -1002062055380
            name = name.replace(f" [AniDL].","").replace(ext,"").strip()
            zumba = title.replace("S2", "Season 2")
            msg = await app.send_message(bin_id,title)

            print("Downloading --> ",name)
           
            await asyncio.sleep(5)
            file = await downloader(msg,link,size,title)

            await msg.edit(f"Download Complete : {name}")
            print("Encoding --> ",name)

            duration = get_duration(file)
            durationx = get_durationx(file)
            #filed = os.path.basename(file)
            filed = title
            
            #filed = filed.replace("[1080p][Multiple Subtitle]", "[1080p Web-DL]")
            filed = filed.replace("[1080p]", "[1080p Web-DL]")
            
            fpath = "downloads/" + filed
            
            
            subtitle = subtitle.replace("][", ", ")
            subtitle = subtitle.replace("[", "")
            subtitle = subtitle.replace("]", "")     
            print(subtitle)
            os.rename(file,"video.mkv")
            titlx = filed.replace('.mkv', '[480p x265 10Bit][Dual-Audio ~ Opus].mkv')
            titm = f"**[AniDL] {titlx}**"
            tito = f"[AniDL] {titlx}"
            
            main = await app.send_message(KAYO_ID,titm)
            video_path="video.mkv"
        
            audio_language = get_audio_languages(video_path)
            joinaud = ", ".join(audio_language)
            if joinaud:
                print("Audio Track Language:", joinaud)
            else:
                print("Failed to get audio language.")
            pending_720p(data["title"])
            compressed = await compress_video(duration,main,tito)
            progtit = extract_title(tito)
            await del_progress(progtit)

            if compressed == "None" or compressed == None:

                print("Encoding Failed Uploading The Original File")

                os.rename("video.mkv",fpath)

            else:

                os.rename("out.mkv",fpath)
            await main.delete()
            print("Uploading --> ",name)
            video = await upload_video(msg,title,tito,fpath,entitle,name,size,subtitle,nyaasize,joinaud)
            print("480title: ", data["title"])
            
            save_480p(data["title"])
   
            print(data["title"])
            titlev2 = data["title"]
            #id, img, tit = await get_anime_img(get_anime_name(titlev2))
            msg2 = await app.send_message(bin_id,titlev2)
            titlev2 = titlev2.replace("[1080p]", "[1080p Web-DL]")
            
            titlx2 = titlev2.replace('.mkv', '[720p x265 10Bit][Dual-Audio ~ Opus].mkv')
           
            titm2 = f"**[AniDL] {titlx2}**"
            tito2 = f"[AniDL] {titlx2}"
            main2 = await app.send_message(KAYO_ID,titm2)
            pending_1080p(data["title"])
            compressed2 = await compress_video720p(duration,main2,tito2)
            progtit = extract_title(tito2)
            await del_progress(progtit)

            if compressed2 == "None" or compressed2 == None:

                print("Encoding Failed Uploading The Original File")

                os.rename("video.mkv",fpath)

            else:

                os.rename("out.mkv",fpath)
            await main2.delete()
            print("Uploading --> ",name)
            video = await upload_video720p(msg2,title,tito2,fpath,entitle,name,size,subtitle,nyaasize,joinaud)
            
            save_720p(data["title"])
            await asyncio.sleep(5)
# 1080p 

            msg3 = await app.send_message(bin_id,title)
            
            titlx3 = titlev2.replace('.mkv', '[1080p x265 10Bit][Dual-Audio ~ AAC].mkv')
           
            titm3 = f"**[AniDL] {titlx3}**"
            tito3 = f"[AniDL] {titlx3}"
            main3 = await app.send_message(KAYO_ID,titm3)
            no_pending(data["title"])
            compressed3 = await compress_video1080p(duration,main3,tito3)
            progtit = extract_title(tito3)
            await del_progress(progtit)

            if compressed3 == "None" or compressed3 == None:

                print("Encoding Failed Uploading The Original File")

                os.rename("video.mkv",fpath)

            else:

                os.rename("out.mkv",fpath)
            await main3.delete()
            print("Uploading --> ",name)
            video = await upload_video1080p(msg3,title,tito3,fpath,entitle,name,size,subtitle,nyaasize,joinaud)
           
            save_1080p(data["title"])
            try:
                os.remove("video.mkv")
                os.remove("out.mkv")
                os.remove(file)
                os.remove(fpath)
            except:
                pass  
            print("All format uploaded.")
            print("del " , name)
            await del_anime(name)
        elif data["uploaded"]=='480p':
            title = data["title"]
            entitle = data["entitle"]
            dbtit = data["title"]
            link = data["link"]
            size = data["size"]
            size = size.replace("GB", " GiB")
            nyaasize = size
            
            subtitl = data["subtitle"]
            subtitle = replace_text_with_mapping(subtitl, mapping)
            name, ext = title.split(".")

            name += f" [AniDL]." + ext

            KAYO_ID =  -1001895203720
            uj_id = 1159872623
            DATABASE_ID = -1001895203720
            bin_id = -1002062055380
            name = name.replace(f" [AniDL].","").replace(ext,"").strip()
           # id, img, tit = await get_anime_img(get_anime_name(title))
            msg = await app.send_message(bin_id,caption=title)

            print("Downloading --> ",name)
            #img,  = await get_anilist_data(title)
            await asyncio.sleep(5)
            await status.edit(await status_text(f"Downloading {name}"),reply_markup=button1)
            file = await downloader(msg,link,size,title)

            await msg.edit(f"Download Complete : {name}")
            print("Encoding --> ",name)

            duration = get_duration(file)
            durationx = get_durationx(file)
            #filed = os.path.basename(file)
            filed = title
            
            filed = filed.replace("[1080p]", "[1080p Web-DL]")
            razo = filed.replace("[1080p Web-DL]", "[720p x265] @animxt")
            fpath = "downloads/" + filed
            ghostname = name
            ghostname = ghostname.replace("[1080p][Multiple Subtitle]", "")
            ghostname = ghostname.replace("[1080p]", "")
            ghostname = ghostname.replace("2nd Season", "S2")
            ghostname = ghostname.replace("3rd Season", "S3")
            subtitle = subtitle.replace("][", ", ")
            subtitle = subtitle.replace("[", "")
            subtitle = subtitle.replace("]", "")     
    
            os.rename(file,"video.mkv")
            titlx = filed.replace('.mkv', '[720p x265 10Bit][Dual-Audio ~ Opus].mkv')
           
            titm = f"**[AniDL] {titlx}**"
            tito = f"[AniDL] {titlx}"
            main = await app.send_message(KAYO_ID,titm)
            video_path="video.mkv"
        
            audio_language = get_audio_languages(video_path)
            joinaud = ", ".join(audio_language)
            if joinaud:
                print("Audio Track Language:", joinaud)
            else:
                print("Failed to get audio language.")
            pending_1080p(data["title"])
            compressed = await compress_video720p(duration,main,tito)
            progtit = extract_title(tito)
            await del_progress(progtit)

            if compressed == "None" or compressed == None:

                print("Encoding Failed Uploading The Original File")

                os.rename("video.mkv",fpath)

            else:

                os.rename("out.mkv",fpath)
            await main.delete()
            print("Uploading --> ",name)
            video = await upload_video720p(msg,title,tito,fpath,entitle,name,size,main,subtitle,nyaasize,joinaud)
           
            save_720p(data["title"])
#1080p 

            msg3 = await app.send_message(bin_id,title)
            titlx3 = title.replace('.mkv', '[1080p x265 10Bit][Dual-Audio ~ AAC].mkv')
           
            titm3 = f"**[AniDL] {titlx3}**"
            tito3 = f"[AniDL] {titlx3}"
            main3 = await app.send_message(KAYO_ID,titm3)
            no_pending(data["title"])
            compressed = await compress_video1080p(duration,main3,tito3)
            progtit = extract_title(tito3)
            await del_progress(progtit)

            if compressed == "None" or compressed == None:

                print("Encoding Failed Uploading The Original File")

                os.rename("video.mkv",fpath)

            else:

                os.rename("out.mkv",fpath)
            await main3.delete()
            print("Uploading --> ",name)
            video = await upload_video1080p(msg3,title,tito3,fpath,entitle,name,size,subtitle,nyaasize,joinaud)
            
            save_1080p(data["title"])
            try:
                os.remove("video.mkv")
                os.remove("out.mkv")
                os.remove(file)
                os.remove(fpath)
            except:
                pass 
            print("All format uploaded.")
            print("del " , name)
            await del_anime(name)

        #1080p
        elif data["uploaded"]=='480p + 720p':
            title = data["title"]
            entitle = data["entitle"]
            dbtit = data["title"]
            link = data["link"]
            size = data["size"]
            size = size.replace("GB", " GiB")
            nyaasize = size
            subtitl = data["subtitle"]
            subtitle = replace_text_with_mapping(subtitl, mapping)
            name, ext = title.split(".")

            name += f" [AniDL]." + ext

            KAYO_ID =  -1001895203720
            uj_id = 1159872623
            DATABASE_ID = -1001895203720
            bin_id = -1002062055380
            name = name.replace(f" [AniDL].","").replace(ext,"").strip()
            #id, img, tit = await get_anime_img(get_anime_name(title))
            msg = await app.send_message(bin_id,title)

            print("Downloading --> ",name)
            #img,  = await get_anilist_data(title)
            await asyncio.sleep(5)
            await status.edit(await status_text(f"Downloading {name}"),reply_markup=button1)
            file = await downloader(msg,link,size,title)

            await msg.edit(f"Download Complete : {name}")
            print("Encoding --> ",name)

            duration = get_duration(file)
            durationx = get_durationx(file)
            #filed = os.path.basename(file)
            filed = title
            
            #filed = filed.replace("[1080p][Multiple Subtitle]", "[1080p Web-DL]")
            #filed = filed.replace("[1080p]", "[1080p Web-DL]")
            fpath = "downloads/" + filed
            ghostname = name
            ghostname = ghostname.replace("[1080p][Multiple Subtitle]", "")
            ghostname = ghostname.replace("[1080p]", "")
            ghostname = ghostname.replace("2nd Season", "S2")
            ghostname = ghostname.replace("3rd Season", "S3")
            subtitle = subtitle.replace("][", ", ")
            subtitle = subtitle.replace("[", "")
            subtitle = subtitle.replace("]", "")     
            print("hello")
            os.rename(file,"video.mkv")
            titlx = filed.replace('.mkv', '[1080p x265 10Bit][Dual-Audio ~ AAC].mkv')

           
            titm = f"**[AniDL] {titlx}**"
            tito = f"[AniDL] {titlx}"
            print('bye')
            main = await app.send_message(KAYO_ID,titm)
            video_path="video.mkv"
        
            audio_language = get_audio_languages(video_path)
            joinaud = ", ".join(audio_language)
            if joinaud:
                print("Audio Track Language:", joinaud)
            else:
                print("Failed to get audio language.")
            no_pending(data["title"])
            compressed = await compress_video1080p(duration,main,tito)
            progtit = extract_title(tito)
            await del_progress(progtit)

            if compressed == "None" or compressed == None:

                print("Encoding Failed Uploading The Original File")

                os.rename("video.mkv",fpath)

            else:

                os.rename("out.mkv",fpath)
            await main.delete()
            print("Uploading --> ",name)
            video = await upload_video1080p(msg,title,tito,fpath,entitle,name,size,subtitle,nyaasize,joinaud)
            
            save_1080p(data["title"])
            try:
                os.remove("video.mkv")
                os.remove("out.mkv")
                os.remove(file)
                os.remove(fpath)
            except:
                pass  
            print("All format uploaded.")
            print("del " , name)
            await del_anime(name)
        else:
            name = data["title"]
            print("All format uploaded.")
            print("del " , name)
            await del_anime(name)
            id = None
            name = None
            video = None

   
    except FloodWait as e:

        flood_time = int(e.x) + 5

        try:

            await status.edit(await status_text(f"Floodwait... Sleeping For {flood_time} Seconds"),reply_markup=button1)

        except:

            pass

        await asyncio.sleep(flood_time)
        
    return name, video

    
