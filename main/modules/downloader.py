import asyncio
import os
from pyrogram.types import Message
from main.modules.progress import get_progress_text

async def downloader(message: Message, link: str, total: int, name: str):
    # Prepare the aria2 command
    command = f'aria2c "{link}" --dir=downloads/ --out="{name}"'
    
    # Start the download using asyncio.create_subprocess_shell
    process = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    
    await message.edit('Downloading...')
    
    # Monitor the download progress
    while True:
        line = await process.stderr.readline()
        if not line:
            break
        
        # Assuming aria2c output format: [#x/#z]
        progress_str = line.decode().strip()
        progress_parts = progress_str[1:-1].split('/')
        if len(progress_parts) == 2:
            current, total_size = int(progress_parts[0]), int(progress_parts[1])
            progress = current / total_size
        else:
            progress = 0.0
        
        # Update message with progress information
        text = get_progress_text(name, 'Downloading', progress, 0, total)
        await message.edit(text=text)
    
    # Wait for the process to complete
    await process.wait()
    
    return f'downloads/{name}'


"""
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

  while (handle.status().state != lt.torrent_status.seeding):
    
    s = handle.status()
    
    state_str = ['queued', 'checking', 'downloading metadata', 'downloading', 'finished', 'seeding', 'allocating']
    
    try:
      text = get_progress_text(
          name, 
          str(state_str[s.state]).capitalize(), 
          s.progress,
          s.download_rate,
          total
        )
      await r.edit(
        text=text
      )
    except:
      pass

    await asyncio.sleep(10)
  
  return "downloads/" + trgt
"""
