import asyncio
import time
import os
import glob
from main import ses
import libtorrent as lt
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from main.modules.progress import *
from main.modules.utils import get_progress_text


async def downloader(message: Message, link: str,total,name):
  params = {
  'save_path': 'downloads/',
  'storage_mode': lt.storage_mode_t(2),}

  handle = lt.add_magnet_uri(ses, link, params)
  ses.start_dht()

  r = message
  await r.edit('Downloading Metadata...')
    
  while (not handle.has_metadata()):    
    await asyncio.sleep(1)

  await r.edit(f'Got Metadata, Starting Download Of **{str(name)}**...')

  trgt = str(handle.name())
  print(trgt)
  
  return "downloads/" + trgt
