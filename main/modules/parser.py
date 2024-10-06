import asyncio
from main.modules.utils import status_text
from main import status
from main.modules.db import get_animesdb, get_uploads, save_animedb
import feedparser
from main import queue
from main.inline import button1
import re
def trim_title(title: str):
    title = title.replace("NieR:Automata Ver1.1a", "NieR Automata Ver1_1a")
    pattern = r"^(.*?)\s*(S\d+E\d+)\s*(.*?)\s\d{3,4}p\s(.*?)\sWEB-DL.*?\((.*?),.*?\)$"
    match = re.match(pattern, title)
    if match:
        titler, episode, extra, source, at = match.groups()
        if at=="Dual-Audio":
            if source=="HIDI":
                source = source.replace("HIDI", "HIDIVE")
                title = f"[AniDL] {titler.strip()} - {episode.strip()} [Web ~ {source.strip()}]"
            else:
                title = f"[AniDL] {titler.strip()} - {episode.strip()} [Web ~ {source.strip()}]"
        else:
            if source=="HIDI":
                source = source.replace("HIDI", "HIDIVE")
                title = f"[AniDL] {at.strip()} - {episode.strip()} [Web ~ {source.strip()}]"
            else:
                title = f"[AniDL] {at.strip()} - {episode.strip()} [Web ~ {source.strip()}]"
    title = title.replace("[YouDeer]", "[AniDL]")
    title = title.replace("(WEB 1080p Dual Audio) | My Deer Friend Nokotan", "[Web ~ YouDeer]")
    title = title.replace(" - S01E", " - ")
    title = title.replace(" - S02E", " S2 - ")
    title = title.replace(" - S03E", " S3 - ")
    title = title.replace(" - S04E", " S4 - ")
    title = title.replace(" - S05E", " S5 - ")
    title = title.replace(" - S06E", " S6 - ")
    title = title.replace(" - S07E", " S7 - ")
    title = title.replace(" - S08E", " S8 - ")
    title = title.replace(" - S09E", " S9 - ")
    title = title.replace(" - S10E", " S10 - ")
    title = title +".mkv"
    return title

def trim_titlex(title: str):
    # Updated regex pattern to capture required groups
    title = title.replace("BLEACH S01E27", "BLEACH S01E01")
    title = title.replace("BLEACH S01E28", "BLEACH S01E02")
    title = title.replace("BLEACH S01E29", "BLEACH S01E03")
    title = title.replace("BLEACH S01E30", "BLEACH S01E04")
    title = title.replace("BLEACH S01E31", "BLEACH S01E05")
    title = title.replace("BLEACH S01E32", "BLEACH S01E06")
    title = title.replace("BLEACH S01E33", "BLEACH S01E07")
    title = title.replace("BLEACH S01E34", "BLEACH S01E08")
    title = title.replace("BLEACH S01E35", "BLEACH S01E09")
    title = title.replace("BLEACH S01E36", "BLEACH S01E10")
    title = title.replace("BLEACH S01E37", "BLEACH S01E11")
    title = title.replace("BLEACH S01E38", "BLEACH S01E12")
    title = title.replace("BLEACH S01E39", "BLEACH S01E13")
    pattern = r"^BLEACH S(\d{2})E(\d{2}) (.*?)(?: \d{3,4}p AMZN WEB-DL DDP\d\.\d H \d{3}-[A-Z]+ \(Multi-Subs\))$"
    match = re.match(pattern, title)
    
    if match:
        season, episode, extra = match.groups()
        
        # Constructing the new title format
        title = f"[AniDL] Bleach - Sennen Kessen Hen - Soukoku Tan - {int(episode):02d} [Web ~ AMZN]"
        print(title)
    title = title +".mp4"
    return title

        
def multi_sub(title: str):
    subtitle = title.split()[-1] 
    return subtitle

def parse():
    a = feedparser.parse("https://www.siftrss.com/f/BoR8BQAzjA1")
    ny = feedparser.parse('''https://nyaa.si/?page=rss&q=%22BLEACH%22%201080p%20AMZN%20WEB-DL%20DDP2.0%20H%20264-VARYG%20-Blood''')
    b = a["entries"]
    
    c = ny["entries"]

    data = []    

    for i in b:
        item = {}
        item['title'] = trim_title(i['title'])
        item['size'] = i['nyaa_size']  
        item['480p'] = '0'
        item['link'] = "magnet:?xt=urn:btih:" + i['nyaa_infohash']
        data.append(item)
        data.reverse()
    for i in c:
        item = {}
        item['title'] = trim_titlex(i['title'])        
        item['subtitle'] = "us"
        item['size'] = i['nyaa_size']   
        item['link'] = "magnet:?xt=urn:btih:" + i['nyaa_infohash']
        item['480p'] = '0'
        data.append(item)
        data.reverse()
    return data

async def auto_parser():
    while True:
        try:
            await status.edit(await status_text("Parsing Rss, Fetching Magnet Links..."),reply_markup=button1)
        except:
            pass

        rss = parse()
        data = await get_animesdb()
        uploaded = await get_uploads()

        saved_anime = []
        for i in data:
            saved_anime.append(i["name"])

        uanimes = []
        for i in uploaded:
            uanimes.append(i["name"])
        
        for i in rss:
            if i["title"] not in uanimes and i["title"] not in saved_anime:
               # if ".mkv" in i["title"] or ".mp4" in i["title"]:
                    title = i["title"]
                    await save_animedb(title,i)

        data = await get_animesdb()
        for i in data:
            if i["data"] not in queue:
                queue.append(i["data"])    
                print("Saved ", i["name"])   

        try:
            await status.edit(await status_text("Idle..."),reply_markup=button1)
        except:
            pass

        await asyncio.sleep(60)
