import spotipy  # Make sure to install Spotipy
import spotipy.util as util
import os
import subprocess
import time
import configparser
import signal
from spotipy.oauth2 import SpotifyOAuth

# Constants for timing
WAIT_TIME = 3
AD_CLOSE_WAIT_TIME = 1.7
application = None

class Song:
    """Class to represent a song with relevant details."""

    def __init__(self, name, album, artist):
        self.name = name
        self.album = album
        self.artist = artist

    @classmethod
    def from_spotify_data(cls, item):
        """Create a Song instance from Spotify item data."""
        name = item['name']
        album = item['album']['name']
        artist = item['album']['artists'][0]['name']
        return cls(name, album, artist)

    def display(self):
        """Print song details to the console."""
        print(f" Song: '{self.name}'")
        print(f" Album: '{self.album}'")
        print(f" Artist: '{self.artist}'")
        print("--------------------------")

# Signal handler for graceful exit
def signal_handler(sig, frame):
    closing()

# Function to handle application closure
def closing():
    print("\nClosing all processes...\n")
    if application is not None:
        application.terminate()
    exit(0)

# Main functionality to skip ads on Spotify
def main():
    global application
    song_data = sp.current_playback()

    # If Spotify is not running, launch it
    if song_data is None:
        try:
            print("Launching Spotify automatically...")
            application = subprocess.Popen(["spotify"])  # Command to launch Spotify
            time.sleep(WAIT_TIME)
        except Exception as e:
            print(f"Error launching process: {e}")
            return

    current_song = Song.from_spotify_data(song_data['item']) if song_data and song_data.get('item') else None

    # Display current song information if available
    if current_song:
        print("--------------------------")
        current_song.display()

    while True:
        current_data = sp.current_playback()

        # Check if Spotify is playing something
        if current_data is None:
            current_data = sp.current_playback()
            current_song = Song.from_spotify_data(current_data['item']) if current_data and current_data.get('item') else None
            if current_song:
                print("--------------------------")
                current_song.display()
            continue

        # Check if the current playback is an ad
        if current_data['item'] is None and current_data['currently_playing_type'] != 'episode':
            print("\nAdvertising detected...\n")
            print(current_data)

            time.sleep(AD_CLOSE_WAIT_TIME)  # Wait before closing the ad

            os.system("pkill spotify")  # Terminate Spotify
            application = subprocess.Popen(["spotify"])  # Relaunch Spotify
            time.sleep(WAIT_TIME)

        # Detect song changes
        if (current_data['item'] and current_data['item']['name'] and
                current_song and current_song.name and current_data['item']['name'] != current_song.name):
            current_song = Song.from_spotify_data(current_data['item'])
            current_song.display()

        time.sleep(WAIT_TIME)

# Function to handle exceptions
def check_exception():
    try:
        main()
    except Exception as e:
        print(f"Handled error: {str(e)}")
        sp = spotipy.Spotify(auth_manager=sp_oauth)  # Reinitialize Spotipy
        check_exception()

if __name__ == '__main__':
    # Config parser for reading Spotify credentials
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Set up Spotify API credentials
    CLIENT_ID = config['spotify']['client_id']
    CLIENT_SECRET = config['spotify']['client_secret']
    REDIRECT_URI = config['spotify']['redirect_uri']
    SCOPE = 'user-read-playback-state user-read-currently-playing'

    # Authorize user and obtain token
    username = config['spotify']['username']
    token = util.prompt_for_user_token(username, SCOPE, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)

    # Initialize Spotify client with OAuth
    sp_oauth = SpotifyOAuth(username=username,
                            client_id=CLIENT_ID,
                            client_secret=CLIENT_SECRET,
                            redirect_uri=REDIRECT_URI)
    sp = spotipy.Spotify(auth_manager=sp_oauth)

    # Set up signal handling for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)

    # Start the main process with exception handling
    check_exception()
    closing()  # Close application on exit
