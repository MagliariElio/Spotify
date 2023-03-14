# Spotify
Nel repository è presente un programma molto grezzo che 
tenta di saltare le pubblicità di un account spotify non premium.

## Requisiti
<li> spotipy </>
<li> spotify </>
<li> connessione ad internet </>

Ovviamente, dovrà essere già installata l'applicazione Spotify e perfettamente funzionante.
Verrà utilizzta la libreria spotipy, pertanto sarà necessario installare prima 
la libreria semplicemente con il gestore dei pacchetti [pip](https://docs.python.org/3/installing/index.html) o pip3, a seconda
della versione installata di python.

**comando**: pip3 install [spotipy](https://spotipy.readthedocs.io/en/2.22.1/)

Da prendere in considerazione anche un ambiente virtuale, facilmente utilizzabile
attraverso il gestore dei pacchetti [conda](https://docs.conda.io/en/latest/).

L'unico piccolo inconveniente è che sarà necessario (per ora) dover rimettere in
play la canzone al momento successivo della pubblicità.

## Sistema Operativo
L'applicazione è stata sviluppata in ambiente Linux(Debian), quindi non sarà garantito il suo
corretto funzionamento su altri sistemi operativi.
