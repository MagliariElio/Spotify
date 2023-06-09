import spotipy                      # da scaricare ('sarebbe consigliato creare un ambiente virtuale')
import spotipy.util as util
import os
import subprocess
import time
import configparser
import signal
from spotipy.oauth2 import SpotifyOAuth


# Con questo programma molto base salteremo la pubblicità su Spotify per account non premium ;)


tempo_attesa = 3
tempo_attesa_chiusura_pubblicita = 1.7
application = None

# Gestione eventi keyboard
def signal_handler(sig, frame):
    closing()
    
# Semplice funzione che raccoglie la logica di chiusura
def closing():
    print("\nClosing all process\n")
    if(application != None):
        application.terminate()
    exit(1)

# Piccolo template per stampare su console, avrebbe bisogno di controlli maggiori sull'input
def print_canzone(song):
    if(song == None or song['item'] == None):
        return
    
    if(song['item']['name'] != None):
        print(" Song: '" + song['item']['name'] + "'")
    
    if(song['item']['album']['name'] != None):
        print(" Album: '" + song['item']['album']['name'] + "'")
    
    if(song['item']['album']['artists'][0]['name'] != None):
        print(" Author: '" + song['item']['album']['artists'][0]['name'] + "'")
    
    print("--------------------------")
    
    return


def main():
    # Creazione dell'oggetto Spotipy
    song = sp.current_playback()

    # Nel caso l'applicazione fosse chiusa, viene aperta automaticamente forkando un processo
    if(song == None):
        try:
            print("Automatic opening of Spotify")
            application = subprocess.Popen(["spotify"])                         # comando da terminale per aprire spotify
            time.sleep(tempo_attesa)
        except:
            print("")                                   # non fare nulla

    if(song != None and song['item'] != None):
        print("--------------------------")
        print_canzone(song)

    while True:
        current = sp.current_playback()
        
        if(current == None or song == None):
            current = sp.current_playback()
            song = current
            if(song != None):
                print("--------------------------")
                print_canzone(song)
            continue
        
        if(current['item'] == None):
            print("\nAdvertising\n")
            print(current)
            
            time.sleep(tempo_attesa_chiusura_pubblicita)            # tempo necessario per far saltare in automatico all'applicazione alla prossima canzone, 
                                                                    # altrimenti bisognerebbe usare il metodo start_playback() ma è una funzione degli account premiumt 
            
            os.popen("pkill spotify")                               # chiude il processo
            application = subprocess.Popen(["spotify"])               # apre di nuovo il processo
            #sp.start_playback()                                    # riprende la canzone in automatico pero' e' una funzione premium
            time.sleep(tempo_attesa)
        
        if(current['item'] != None and current['item']['name'] != song['item']['name']):
            song = current
            print_canzone(song)

        time.sleep(tempo_attesa)

    return


def check_exception():
    # Main
    try:
        main()
    except Exception as e:
        print("Errore gestito: ", str(e))
        sp_oauth.refresh_access_token(token)
        check_exception()
    return



if(__name__ == '__main__'):
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
    
    # Autenticazione
    sp_oauth = SpotifyOAuth(username=username,
                                                        client_id=CLIENT_ID,
                                                        client_secret=CLIENT_SECRET,
                                                        redirect_uri=REDIRECT_URI)
    sp = spotipy.Spotify(auth_manager=sp_oauth)

    # Dichiarazione gestione eventi
    signal.signal(signal.SIGINT, signal_handler)
    
    check_exception()           # modo veloce per gestire le eccezioni e lasciarlo in stato di running
    closing()                   # chiusura applicazione