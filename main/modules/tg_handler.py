
import asyncio
import time
import aiohttp
import requests
import aiofiles
import sys
from main.modules.compressor import compress_video, compress_video720p, compress_video1080p
from pymediainfo import MediaInfo
from main.modules.utils import episode_linker, get_duration, get_epnum, status_text, get_filesize, b64_to_str, str_to_b64, send_media_and_reply, get_durationx

from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from main.modules.uploader import upload_video, upload_video720p, upload_video1080p
from main.modules.thumbnail import generate_thumbnail

import os

from main.modules.db import del_anime, save_uploads, is_fid_in_db, is_tit_in_db, save_480p, save_720p, save_1080p

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
                
                id, name, video = await start_uploading(i)
                print("Title: ", i["title"])
                
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

                await status.edit(await status_text(f"Floodwait... Sleeping For {flood_time} Seconds"),reply_markup=button1)

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
    "en": "ENG",
    "pt-BR": "POR-BR",
    "es-419": "SPA-LA",
    "es": "SPA",
    "ar": "ARA",
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
    "vi": "VIE",
    "hi": "HIN",
    "te": "TEL",
    "uk": "UKR",
    "hu": "HUN",
    "cs": "CES",
    "hr": "HRV",
    "ms": "MAY",
    "sk": "SLK",
    "fil": "FIL"
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
        
def esl(video_path):
    media_info = MediaInfo.parse(video_path)
    
    subtitle_languages = []
    for track in media_info.tracks:
        if track.track_type == 'Text':
            subtitle_languages.append(track.language)
    
    return subtitle_languages
    
async def start_uploading(data):

    try:
        if data["480p"]=='0':
            title = data["title"]
            dbtit = data["title"]
            link = data["link"]
            size = data["size"]
            size = size.replace("GB", " GiB")
            nyaasize = size
            name, ext = title.split(".")

            name += f" [AniDL]." + ext

            KAYO_ID =  -1001895203720
            uj_id = 1159872623
            DATABASE_ID = -1001895203720
            bin_id = -1002062055380
            name = name.replace(f" [AniDL].","").replace(ext,"").strip()
            zumba = title.replace("[AniDL] ", "")
            zumba = zumba.replace("S2", "Season 2")
            zumba = zumba.replace("S3", "Season 3")
            zumba = zumba.replace("S4", "Season 4")
            zumba = zumba.replace("S5", "Season 5")
            zumba = zumba.replace("S6", "Season 6")
            zumba = zumba.replace("S7", "Season 7")
            zumba = zumba.replace("S8", "Season 8")
            zumba = zumba.replace("S9", "Season 9")
            zumba = zumba.replace("S10", "Season 10")
            id, img, tit, alink = await get_anime_img(get_anime_name(zumba))
            
            msg = await app.send_photo(bin_id,photo=img,caption=title)

            print("Downloading --> ",name)
            
            await asyncio.sleep(5)
            
            file = await downloader(msg,link,size,title)

            await msg.edit(f"Download Complete : {name}")
            print("Encoding --> ",name)

            duration = get_duration(file)
            durationx = get_durationx(file)
            filed = os.path.basename(file)
            newname = title.replace(".mkv", "[480p x265 10Bit][Dual-Audio ~ Opus].mkv")
            newname = newname.replace(".mp4", "[480p x265 10Bit][Opus].mkv")
            filed = filed.replace(filed, newname)
            fpath = "downloads/" + filed
    
            os.rename(file,"video.mkv")

            main = await app.send_photo(KAYO_ID,photo=img, caption=newname)
            video_path="video.mkv"
        
            audio_language = get_audio_languages(video_path)
            joinaud = ", ".join(audio_language)
            if joinaud:
                print("Audio Track Language:", joinaud)
            else:
                print("Failed to get audio language.")
            subtitle_languages = esl(video_path)
        
            if subtitle_languages:
                print("Subtitle Track Language:", subtitle_languages)
            else:
                print("Failed to get subtitle language.")
            joinsub = ", ".join(subtitle_languages)
            exsub = joinsub.replace("][", ", ")
            exsub = exsub.replace("[", "")
            exsub = exsub.replace("]", "")  
            subtitle = exsub
            msubtitle = replace_text_with_mapping(subtitle, mapping)
            print(msubtitle)
        
            compressed = await compress_video(duration,main,newname)
    

            if compressed == "None" or compressed == None:

                print("Encoding Failed Uploading The Original File")

                os.rename("video.mkv",fpath)

            else:

                os.rename("out.mkv",fpath)
  
            print("Uploading --> ",name)
            video = await upload_video(msg,title,img,fpath,id,tit,name,size,main,msubtitle,nyaasize,joinaud, alink)
            print("480title: ", data["title"])
            save_480p(data["title"])
   
            print(data["title"])
            titlev2 = data["title"]
            stit = titlev2.replace("[AniDL] ", "")
            newname720 = titlev2.replace(".mkv", "[720p x265 10Bit][Dual-Audio ~ Opus].mkv")
            newname720 = newname720.replace(".mp4", "[720p x265 10Bit][Opus].mkv")
            id, img, tit, alink = await get_anime_img(get_anime_name(stit))
            msg2 = await app.send_photo(bin_id,photo=img,caption=newname720)
            fpath = "downloads/" + newname720
    
            main2 = await app.send_photo(KAYO_ID,photo=img, caption=f"**newname720**")
            compressed2 = await compress_video720p(duration,main2,newname720)
    

            if compressed2 == "None" or compressed2 == None:

                print("Encoding Failed Uploading The Original File")

                os.rename("video.mkv",fpath)

            else:

                os.rename("out.mkv",fpath)
  
            print("Uploading --> ",name)
            video = await upload_video720p(msg2,title,img,fpath,id,tit,name,size,main2,msubtitle,nyaasize,joinaud, alink)
            save_720p(data["title"])
            await asyncio.sleep(5)
# 1080p 
            newname1080 = titlev2.replace(".mkv", "[1080p x265 10Bit][Dual-Audio ~ AAC].mkv")
            newname1080 = newname1080.replace(".mp4", "[1080p x265 10Bit][AAC].mkv")
            msg3 = await app.send_photo(bin_id,photo=img,caption=newname1080)
            main3 = await app.send_photo(KAYO_ID,photo=img, caption=newname1080)
            fpath = "downloads/" + newname1080
            compressed3 = await compress_video1080p(duration,main3,newname1080)
    

            if compressed3 == "None" or compressed3 == None:

                print("Encoding Failed Uploading The Original File")

                os.rename("video.mkv",fpath)

            else:

                os.rename("out.mkv",fpath)
  
            print("Uploading --> ",name)
            video = await upload_video1080p(msg3,title,img,fpath,id,tit,name,size,main3,msubtitle,nyaasize,joinaud, alink)
            save_1080p(data["title"])
            try:
                os.remove("video.mkv")
                os.remove("out.mkv")
                os.remove(file)
                os.remove(fpath)
            except:
                pass  

        
        elif data["480p"]=='01':
            title = data["title"]
            dbtit = data["title"]
            link = data["link"]
            size = data["size"]
            size = size.replace("GB", " GiB")
            nyaasize = size
            
            name, ext = title.split(".")

            name += f" [AniDL]." + ext

            KAYO_ID =  -1001895203720
            uj_id = 1159872623
            DATABASE_ID = -1001895203720
            bin_id = -1002062055380
            name = name.replace(f" [AniDL].","").replace(ext,"").strip()
            zumba = title.replace("[AniDL] ", "")
            zumba = zumba.replace("S2", "Season 2")
            zumba = zumba.replace("S3", "Season 3")
            zumba = zumba.replace("S4", "Season 4")
            zumba = zumba.replace("S5", "Season 5")
            zumba = zumba.replace("S6", "Season 6")
            zumba = zumba.replace("S7", "Season 7")
            zumba = zumba.replace("S8", "Season 8")
            zumba = zumba.replace("S9", "Season 9")
            zumba = zumba.replace("S10", "Season 10")
            id, img, tit, alink = await get_anime_img(get_anime_name(zumba))
            msg = await app.send_photo(bin_id,photo=img,caption=title)

            print("Downloading --> ",name)
            
            await asyncio.sleep(5)
            
            file = await downloader(msg,link,size,title)

            await msg.edit(f"Download Complete : {name}")
            print("Encoding --> ",name)

            duration = get_duration(file)
            durationx = get_durationx(file)
            filed = os.path.basename(file)
            newname720 = title.replace(".mkv", "[720p x265 10Bit][Dual-Audio ~ Opus].mkv")
            newname720 = newname720.replace(".mp4", "[720p x265 10Bit][Opus].mkv")
            filed = filed.replace(filed, newname720)
            fpath = "downloads/" + filed 
    
            os.rename(file,"video.mkv")
            main = await app.send_photo(KAYO_ID,photo=img, caption=newname720)
            video_path="video.mkv"
        
            audio_language = get_audio_languages(video_path)
            joinaud = ", ".join(audio_language)
            if joinaud:
                print("Audio Track Language:", joinaud)
            else:
                print("Failed to get audio language.")
            subtitle_languages = esl(video_path)
        
            if subtitle_languages:
                print("Subtitle Track Language:", subtitle_languages)
            else:
                print("Failed to get subtitle language.")
            joinsub = ", ".join(subtitle_languages)
            exsub = joinsub.replace("][", ", ")
            exsub = exsub.replace("[", "")
            exsub = exsub.replace("]", "")  
            subtitle = exsub
            msubtitle = replace_text_with_mapping(subtitle, mapping)
            print(msubtitle)
            compressed = await compress_video720p(duration,main,newname720)
    

            if compressed == "None" or compressed == None:

                print("Encoding Failed Uploading The Original File")

                os.rename("video.mkv",fpath)

            else:

                os.rename("out.mkv",fpath)
  
            print("Uploading --> ",name)
            video = await upload_video720p(msg,title,img,fpath,id,tit,name,size,main,msubtitle,nyaasize,joinaud, alink)
            save_720p(data["title"])
#1080p 

            newname1080 = title.replace(".mkv", "[1080p x265 10Bit][Dual-Audio ~ AAC].mkv")
            newname1080 = newname1080.replace(".mp4", "[1080p x265 10Bit][AAC].mkv")
            msg3 = await app.send_photo(bin_id,photo=img,caption=newname1080)
            main3 = await app.send_photo(KAYO_ID,photo=img, caption=newname1080)
            fpath = "downloads/" + newname1080
            compressed3 = await compress_video1080p(duration,main3,newname1080)
    

            if compressed3 == "None" or compressed3 == None:

                print("Encoding Failed Uploading The Original File")

                os.rename("video.mkv",fpath)

            else:

                os.rename("out.mkv",fpath)
  
            print("Uploading --> ",name)
            video = await upload_video1080p(msg3,title,img,fpath,id,tit,name,size,main3,msubtitle,nyaasize,joinaud, alink)
            save_1080p(data["title"])
            try:
                os.remove("video.mkv")
                os.remove("out.mkv")
                os.remove(file)
                os.remove(fpath)
            except:
                pass  

        #1080p
        elif data["480p"]=='012':
            title = data["title"]
            dbtit = data["title"]
            link = data["link"]
            size = data["size"]
            size = size.replace("GB", " GiB")
            nyaasize = size

            name, ext = title.split(".")

            name += f" [AniDL]." + ext

            KAYO_ID =  -1001895203720
            uj_id = 1159872623
            DATABASE_ID = -1001895203720
            bin_id = -1002062055380
            name = name.replace(f" [AniDL].","").replace(ext,"").strip()
            zumba = title.replace("[AniDL] ", "")
            zumba = zumba.replace("S2", "Season 2")
            zumba = zumba.replace("S3", "Season 3")
            zumba = zumba.replace("S4", "Season 4")
            zumba = zumba.replace("S5", "Season 5")
            zumba = zumba.replace("S6", "Season 6")
            zumba = zumba.replace("S7", "Season 7")
            zumba = zumba.replace("S8", "Season 8")
            zumba = zumba.replace("S9", "Season 9")
            zumba = zumba.replace("S10", "Season 10")
            id, img, tit, alink = await get_anime_img(get_anime_name(zumba))
            msg = await app.send_photo(bin_id,photo=img,caption=title)

            print("Downloading --> ",name)
            
            await asyncio.sleep(5)
            
            file = await downloader(msg,link,size,title)

            await msg.edit(f"Download Complete : {name}")
            print("Encoding --> ",name)

            duration = get_duration(file)
            durationx = get_durationx(file)
            filed = os.path.basename(file)
            newname1080 = title.replace(".mkv", "[1080p x265 10Bit][Dual-Audio ~ AAC].mkv")
            newname1080 = newname1080.replace(".mp4", "[1080p x265 10Bit][AAC].mkv")
            filed = filed.replace(filed, newname1080)
            fpath = "downloads/" + filed 
    

            fpath = "downloads/" + filed  
    
            os.rename(file,"video.mkv")
            main = await app.send_photo(KAYO_ID,photo=img, caption=newname1080)
            video_path="video.mkv"
        
            audio_language = get_audio_languages(video_path)
            joinaud = ", ".join(audio_language)
            if joinaud:
                print("Audio Track Language:", joinaud)
            else:
                print("Failed to get audio language.")
            subtitle_languages = esl(video_path)
        
            if subtitle_languages:
                print("Subtitle Track Language:", subtitle_languages)
            else:
                print("Failed to get subtitle language.")
            joinsub = ", ".join(subtitle_languages)
            exsub = joinsub.replace("][", ", ")
            exsub = exsub.replace("[", "")
            exsub = exsub.replace("]", "")  
            subtitle = exsub
            msubtitle = replace_text_with_mapping(subtitle, mapping)
            print(msubtitle)

            compressed = await compress_video1080p(duration,main,newname1080)
    

            if compressed == "None" or compressed == None:

                print("Encoding Failed Uploading The Original File")

                os.rename("video.mkv",fpath)

            else:

                os.rename("out.mkv",fpath)
  
            print("Uploading --> ",name)
            video = await upload_video1080p(msg,title,img,fpath,id,tit,name,size,main,msubtitle,nyaasize,joinaud, alink)
            save_1080p(data["title"])
            try:
                os.remove("video.mkv")
                os.remove("out.mkv")
                os.remove(file)
                os.remove(fpath)
            except:

                pass  
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
        
    return id, name, video

    
