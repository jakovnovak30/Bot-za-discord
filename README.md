# Bot-za-discord 

O botu
---
* jednostavni kod za bot koji pušta muziku
* ima dvije verzije:
	1. "bot2.py" -> pušta samo muziku koja je spremljena lokalno
	2. "bot3.py" -> može preuzeti muziku s interneta ako ne nađe pjesmu koja je spremljena na računalu i ima dovoljno sličan naslov (koristi se SequenceMatcher iz difflib modulea) 

![Demonstracija bota](/slike/demonstracija.png)

Sadržaj
---
* [Requirements](#Requirements)
	* [Potrebni moduli za python3](#Sljedeći-moduli-za-python3)
* [Instalacija](#Instalacija-bota)
	* [Imate git CLI](#Ako-imate-git-CLI)
	* [Nemate git CLI](#Ako-nemate-git-CLI)
* [Postavke](#Postavljanje-postavki)
	* [Nemam token za bot!](#Što-ako-nemam-token?)
* [Korištenje](#Korištenje-bota)
	* [Imate youtube-dl CLI](#Ako-imate-youtube-dl-CLI)
	* [Nemate youtube-dl CLI](#Ako-nemate-youtube-dl-CLI)

Requirements
---
* python3
* youtube-dl CLI (za "bot3.py")
#### Sljedeći moduli za python3
	* discord.py>=1.6.0
	* discord>=1.0.1
	* python-dotenv>=0.17.0
	* tube_dl>=5.1.0

Instalacija bota
---
#### Ako imate git CLI
	* otvorite terminal u mapi u koju želite spremiti bota
	* upišite git clone https://github.com/jakovnovak30/Bot-za-discord.git u terminal
	* izmjenite potrebni tekst u datoteci "postavke.env"

![Preuzimanje s git CLI-om](/slike/download2.png)

#### Ako nemate git CLI
	* pritisnite zeleni gumb "Code" i preuzmite ZIP verziju ovog repositorija
	* izmjenite tekst u datoteci "postavke.env" nakon što ste raspakirali ZIP u željenu mapu

![Preuzimanje bez git CLI-a](/slike/download.png)

Postavljanje postavki
---
* otvorite datoteku "postavke.env"
* na prvu liniju upišite ime servera na kojem ćete koristiti bot 
* na drugu liniju upišite token bota
* na trećoj liniji napišite put do mape u kojoj imate spremljene pjesme na vašem računalu

![Postavke](/slike/postavke.png)

#### Što ako nemam token?
	* otvorite stranicu https://discord.com/developers/applications
	* napravite novu aplikaciju s botom
	* na kartici OAuth2 dodajte bot u svoj server

![Primjer bota na discordovoj stranici](/slike/discordapi.png)

Korištenje bota
---
#### Ako imate youtube-dl CLI
	* pokrenite program "bot3.py"
	* možete puštati muziku s kompjutera i muziku s interneta
	* muzika s interneta će se spremiti u mapu koju ste odredili u datoteci "postavke.env"
#### Ako nemate youtube-dl CLI
	* pokrenite program "bot2.py"
	* možete puštati samo muziku koja je na kompjuteru spremljena

* napišite "<help" u voice channel da biste vidjeli popis naredbi

Sretno!
