import os
import heroku3

API_ID = 6624445
API_HASH = "d7bf4c140d85cf1338afb2a5a27e7cb8"
BOT_TOKEN = "1836226590:AAH6d3_X1GOrgUtoJP6e3gJn7vE-N-sUvVM" 

HEROKU_KEY = "f8d39ab5-43d1-4025-82f3-62abff82590c"
HEROKU_NAME = "emma-song-bot"


HEROKU_CONN = heroku3.from_key(HEROKU_KEY)
HEROKU_APP = HEROKU_CONN.apps()[HEROKU_NAME]

    
