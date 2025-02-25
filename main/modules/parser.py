import asyncio
from main.modules.utils import status_text
from main import status
from main.modules.db import get_animesdb, get_uploads, save_animedb
import feedparser
from main import queue
from main.inline import button1
import re
import requests
from bs4 import BeautifulSoup
import requests
import anitopy
mapping = {
    "English": "us",
    "English [Forced]": "us",
    "Japanese": "jp",
    "Arabic": "ar",
    "Arabic (Saudi Arabia)": "sa",
    "Catalan": "cat",
    "Czech": "cz",
    "Danish": "dk",
    "German": "de",
    "Greek": "gr",
    "Spanish (Latin American)": "mx",
    "Spanish (European)": "es",
    "Basque": "eus",
    "Finnish": "fi",
    "Filipino": "ph",
    "French": "fr",
    "Galician": "gl",
    "Hebrew": "il",
    "Hindi": "in",
    "Croatian": "hr",
    "Hungarian": "hu",
    "Indonesian": "id",
    "Italian": "it",
    "Korean": "kr",
    "Malay": "my",
    "Norwegian Bokmål": "no",
    "Dutch": "nl",
    "Polish": "pl",
    "Portuguese (Brazilian)": "br",
    "Portuguese (European)": "pt",
    "Romanian": "ro",
    "Russian": "ru",
    "French (European)": "fr",
    "Swedish": "se",
    "Thai": "th",
    "Turkish": "tr",
    "Ukrainian": "ua",
    "Vietnamese": "vn",
    "Chinese (Hong Kong)": "cn",
    "Chinese": "cn",
    "Chinese (Simplified)": "cn",
    "Chinese (Traditional)": "tw"
}

def map_language(language):
    return mapping.get(language.strip(), language.strip())  # Default to original if not found

def extract_audio_subtitles(url):
    try:
        # Fetching the webpage content
        url = url.replace("download", "view")
        url = url.replace(".torrent", "")
        url = url.replace("nyaa.si", "nyaa-proxy.vercel.app")
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        # Extracting title
        title = soup.find("title").text.strip()

        # Extracting the torrent description
        torrent_description_div = soup.find("div", id="torrent-description")
        if not torrent_description_div:
            return title, [], []

        # Initialize variables to store audio and subtitle details
        audio_languages = set()
        subtitle_languages = set()

        # Get the text content of the div
        description_text = torrent_description_div.get_text(separator="\n")
        description_text = description_text.replace("**", "").replace("`", "").replace(" [Dubtitle]", "").replace(" [SDH]", "").replace(" [CC]", "").replace("Chinese (China)", "Chinese").replace("English (BILI)", "en").replace("English (HIDI)", "en").replace("Indonesian (BILI)","Indonesian").replace("Thai (BILI)","Thai")

        # Extracting audio details
        audio_match = re.search(r"Audios \(\d+\):(.*?)(?:\n|$)", description_text, re.DOTALL)
        if audio_match:
            audio_raw = audio_match.group(1)
            audio_languages = {map_language(audio.split(",")[0].strip()) for audio in audio_raw.split("│")}

        # Extracting subtitle details
        subtitle_match = re.search(r"Subtitles \(\d+\):(.*?)(?:\n|$)", description_text, re.DOTALL)
        if subtitle_match:
            subtitle_raw = subtitle_match.group(1)
            subtitle_languages = {map_language(subtitle.split(",")[0].strip()) for subtitle in subtitle_raw.split("│")}

        # Convert sets to comma-separated strings and filter out empty values
        audio_languages = ", ".join(sorted(filter(None, audio_languages)))
        subtitle_languages = "][".join(sorted(filter(None, subtitle_languages)))
        subtitle_languages = f"[{subtitle_languages}]"

        return subtitle_languages

    except requests.RequestException as e:
        print("Error fetching URL:", e)
        return None
        
def trim_title(title: str):
    title = title.replace("NieR:Automata Ver1.1a", "NieR Automata Ver1_1a")
    title = title.replace("Dr.", "Dr")
    title = title.replace("Kimi wa Meido-sama.", "Kimi wa Meido-sama")    
    title = title.replace("Zenshuu.", "Zenshuu")    
    pattern = r"^(.*?)\s*(S\d+E\d+)\s*(.*?)\s\d{3,4}p\s(.*?)\sWEB-DL.*?\((.*?),.*?\)$"
    pattern2 = r"^(.*?)\s*(S\d+E\d+)\s*(.*?)\s\d{3,4}p\s(.*?)\sWEB-DL.*?\((.*?)\)$"
    match = re.match(pattern, title)
    match2 = re.match(pattern2, title)
    if match:
        titler, episode, extra, source, at = match.groups()
        if at=="Dual-Audio":
            if source=="HIDI":
                source = source.replace("HIDI", "HIDIVE")
                title = f"{titler.strip()} - {episode.strip()} [Web ~ {source.strip()}]"
            else:
                title = f"{titler.strip()} - {episode.strip()} [Web ~ {source.strip()}]"
        else:
            if source=="HIDI":
                source = source.replace("HIDI", "HIDIVE")
                title = f"{at.strip()} - {episode.strip()} [Web ~ {source.strip()}]"
            else:
                title = f"{at.strip()} - {episode.strip()} [Web ~ {source.strip()}]"
    elif match2:
        titler, episode, extra, source, at = match2.groups()
        if at=="Dual-Audio":
            if source=="HIDI":
                source = source.replace("HIDI", "HIDIVE")
                title = f"{titler.strip()} - {episode.strip()} [Web ~ {source.strip()}]"
            else:
                title = f"{titler.strip()} - {episode.strip()} [Web ~ {source.strip()}]"
        else:
            if source=="HIDI":
                source = source.replace("HIDI", "HIDIVE")
                title = f"{at.strip()} - {episode.strip()} [Web ~ {source.strip()}]"
            else:
                title = f"{at.strip()} - {episode.strip()} [Web ~ {source.strip()}]"
    title = title.replace("[YouDeer]", "")
    title = title.replace("Shi Cao", "Shicao")
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

def trim_etitle(title):
    filename_content = anitopy.parse(title)
    print(filename_content)
    eng_title = filename_content["anime_title"]
    return eng_title

def trim_titlex(title: str):
    # Updated regex pattern to capture required groups
    title = title.replace("BLEACH S01E27", "BLEACH S01E01")
    title = title.replace("BLEACH S01E28", "BLEACH S01E02")
    title = title.replace("BLEACH Thousand Year Blood War S01E29", "BLEACH S01E03")
    title = title.replace("BLEACH Thousand Year Blood War S01E30", "BLEACH S01E04")
    title = title.replace("BLEACH Thousand Year Blood War S01E31", "BLEACH S01E05")
    title = title.replace("BLEACH Thousand Year Blood War S01E32", "BLEACH S01E06")
    title = title.replace("BLEACH Thousand Year Blood War S01E33", "BLEACH S01E07")
    title = title.replace("BLEACH Thousand Year Blood War S01E34", "BLEACH S01E08")
    title = title.replace("BLEACH Thousand Year Blood War S01E35", "BLEACH S01E09")
    title = title.replace("BLEACH Thousand Year Blood War S01E36", "BLEACH S01E10")
    title = title.replace("BLEACH Thousand Year Blood War S01E37", "BLEACH S01E11")
    title = title.replace("BLEACH Thousand Year Blood War S01E38", "BLEACH S01E12")
    title = title.replace("BLEACH Thousand Year Blood War S01E39", "BLEACH S01E13")
    
    pattern = r"^BLEACH S(\d{2})E(\d{2}) (.*?)(?: \d{3,4}p AMZN WEB-DL DDP\d\.\d H \d{3}-[A-Z]+ \(Bleach: Sennen Kessen-hen, Multi-Subs\))$"
    match = re.match(pattern, title)
    
    if match:
        season, episode, extra = match.groups()
        
        # Constructing the new title format
        title = f"Bleach - Sennen Kessen Hen - Soukoku Tan - {int(episode):02d} [Web ~ AMZN]"
        print(title)
    title = title +".mp4"
    return title

        
def multi_sub(title: str):
    subtitle = title.split()[-1] 
    return subtitle

def parse():
    a = feedparser.parse("https://www.siftrss.com/f/BoR8BQAzjA1")
    ny = feedparser.parse('''https://siftrss.com/f/13VVy8RQYK8''')
    b = a["entries"]
    
    c = ny["entries"]

    data = []    

    for i in b:
        item = {}
        item['title'] = trim_title(i['title'])
        item['entitle'] = trim_etitle(i['title'])
        item['subtitle'] = extract_audio_subtitles(i['link'])
        item['size'] = i['nyaa_size']  
        item['uploaded'] = '0'
        item['pending'] = '480p + 720p + 1080p'
        item['link'] = "magnet:?xt=urn:btih:" + i['nyaa_infohash']
        data.append(item)
        data.reverse()
    for i in c:
        item = {}
        item['title'] = trim_title(i['title']) 
        item['entitle'] = trim_etitle(i['title'])
        item['subtitle'] = extract_audio_subtitles(i['link'])
        item['size'] = i['nyaa_size']   
        item['link'] = "magnet:?xt=urn:btih:" + i['nyaa_infohash']
        item['uploaded'] = '0'
        item['pending'] = '480p + 720p + 1080p'
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

        await asyncio.sleep(120)
