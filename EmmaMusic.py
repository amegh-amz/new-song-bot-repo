from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
import youtube_dl
from youtube_search import YoutubeSearch
import requests

import os
from config import BOT_TOKEN, API_HASH, API_ID, HEROKU_APP

bot = Client('MissRose',
      bot_token = BOT_TOKEN,
      api_id = API_ID,
      api_hash = API_HASH)

## Extra Fns -------------------------------

# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))


## Commands --------------------------------
@bot.on_message(filters.command(['start']))
def start(client, message):
    amegh ="**Hi Bro,\n\nI Can Download Song's From YouTube.\nI Can Only Work In My Owners Group.**"
    message.reply_text(
        text=amegh, 
        quote=False,
        reply_markup=InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton('Music 🎸', url='http://t.me/mt_music_24'),
                    InlineKeyboardButton('Movie', url='https://t.me/MovieTownChat')
                ],
                [
                    InlineKeyboardButton('Owner', url='https://t.me/AmzMtAccount')
                ]]
))
 
@bot.on_message(filters.command(['mt', 'song', 'music', 'yt']) & (filters.chat("mt_music_24") | filters.user("AmzMtAccount")))
def a(client, message):
    query = ''
    for i in message.command[1:]:
        query += ' ' + str(i)
    print(query)
    m = message.reply('`Searching Your Music....`')
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = []
        count = 0
        while len(results) == 0 and count < 6:
            if count>0:
                time.sleep(1)
            results = YoutubeSearch(query, max_results=1).to_dict()
            count += 1
        # results = YoutubeSearch(query, max_results=1).to_dict()
        try:
            link = f"https://youtube.com{results[0]['url_suffix']}"
            # print(results)
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            duration = results[0]["duration"]

            ## UNCOMMENT THIS IF YOU WANT A LIMIT ON DURATION. CHANGE 1800 TO YOUR OWN PREFFERED DURATION AND EDIT THE MESSAGE (30 minutes cap) LIMIT IN SECONDS
            # if time_to_seconds(duration) >= 1800:  # duration limit
            #     m.edit("Exceeded 30mins cap")
            #     return

            views = results[0]["views"]
            thumb_name = f'thumb{message.message_id}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)

        except Exception as e:
            print(e)
            m.edit('Found nothing. Try changing the spelling a little.')
            return
    except Exception as e:
        m.edit(
            "✖️ Found Nothing. Sorry.\n\nTry another keywork or maybe spell it properly."
        )
        print(str(e))
        return
    m.edit("`Downloading...`")
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f'**✣ Title**: **[{title[:35]}]({link})**\n**✣ Uploaded By : [MT Musics](http://t.me/mt_music_24)**'
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        m.edit("`Uploading Your Music...`")
        message.reply_chat_action("upload_audio")
        message.reply_audio(audio_file, caption=rep, parse_mode='md',quote=False, title=title, duration=dur, thumb=thumb_name)
        m.delete()
    except Exception as e:
        m.edit('**🐞 Download Error.\nSorry {message.from.user.mention},**\nThere Is An Error In Uploading Your Music.Im Trying To Fix It Please Request This Song After A Minute.')
        HEROKU_APP.restart()
        print("Bot Restarted | Errors Fixed")
       
    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)

bot.run()
