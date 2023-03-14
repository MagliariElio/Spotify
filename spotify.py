import spotipy
import spotipy.util as util
import os
import time
import configparser


# con questo programma salteremo la pubblicità in spotify ;)


#config parser
config = configparser.ConfigParser()
config.read('config.ini')

# Impostazione delle credenziali di accesso
CLIENT_ID = config['spotify']['client_id']
CLIENT_SECRET = config['spotify']['client_secret']
REDIRECT_URI = config['spotify']['redirect_uri']
SCOPE = 'user-read-playback-state user-read-currently-playing'

# Autorizzazione dell'utente
username = config['spotify']['username']
token = util.prompt_for_user_token(username, SCOPE, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)

# Creazione dell'oggetto Spotipy
sp = spotipy.Spotify(auth=token)

song = sp.current_playback()
if(song['item'] != None):
    print("\nCanzone: '" + song['item']['name'] + "'\nAlbum: '" + song['item']['album']['name'] + "'\nAutore: '" + song['item']['album']['artists'][0]['name'] + "'\n")

while True:
    current = sp.current_playback()
    
    if(current['item'] == None):
        os.popen("pkill spotify")       # chiude il processo
        os.popen("spotify")             # apre di nuovo il processo
        #sp.start_playback()             # riprende la canzone in automatico
        time.sleep(10)
    
    if(current['item'] != None and current['item']['name'] != song['item']['name']):
        song = current
        print("Canzone: '" + song['item']['name'] + "'\nAlbum: '" + song['item']['album']['name'] + "'\nAutore: '" + song['item']['album']['artists'][0]['name'] + "'\n")

    time.sleep(3)



