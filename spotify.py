import spotipy                      # da scaricare ('sarebbe consigliato creare un ambiente virtuale')
import spotipy.util as util
import os
import time
import configparser


# Con questo programma molto base salteremo la pubblicità su Spotify per account non premium ;)


# Config parser
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


def print_canzone(song):
    if(song == None or song['item'] == None):
        return
    
    if(song['item']['name'] != None):
        print("Canzone: '" + song['item']['name'])
    
    if(song['item']['album']['name'] != None):
        print("Album: '" + song['item']['album']['name'])
    
    if(song['item']['album']['artists'][0]['name'] != None):
        print("Autore: '" + song['item']['album']['artists'][0]['name'] + "'\n")
    
    return


def main():
    # Creazione dell'oggetto Spotipy
    sp = spotipy.Spotify(auth=token)

    song = sp.current_playback()

    # Nel caso l'applicazione fosse chiusa, viene aperta automaticamente forkando un processo
    if(song == None):
        os.popen("spotify")
        print("Apertura automatica di Spotify")

    if(song != None and song['item'] != None):
        print_canzone(song)

    while True:
        current = sp.current_playback()
        
        if(current == None or song == None):
            current = sp.current_playback()
            song = current
            print_canzone(song)
            continue
        
        if(current['item'] == None):
            print("Pubblicità\n")
            time.sleep(2)    # TODO: da rimuovere
            os.popen("pkill spotify")       # chiude il processo
            os.popen("spotify")             # apre di nuovo il processo
            #sp.start_playback()            # riprende la canzone in automatico pero' e' una funzione premium
            time.sleep(10)
        
        if(current['item'] != None and current['item']['name'] != song['item']['name']):
            song = current
            print_canzone(song)

        time.sleep(3)

    return

if(__name__ == '__main__'):
    main()
    
