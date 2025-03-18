
## Inštalácia a spustenie

* Klonujte/stiahnite projekt z repozitára.
* Stiahnite a nainštalujte Python [z oficiálnej webovej stránky](https://www.python.org/downloads/).
* Stiahnite a nainštalujte [nástroj na prehliadanie SQLite databáz](https://sqlitebrowser.org/dl/).
* Prejdite do adresára projektu pomocou príkazového riadku alebo terminálu a vytvorte + aktivujte virtuálne prostredie pomocou príkazu:

```bash
python -m venv .venv
#aktivácia na Windows
.\.venv\Scripts\activate
#aktivácia na MacOS/Linux
source .venv/bin/activate
```
* Nainštalujte knižníce:
```bash
pip install -r requirements.txt
```
* Pre spustenie všetkých spiderov naraz prejdite do priečinka, ktorý obsahuje súbor *spiders_run.py*, a zadajte príkaz:
```bash
python spiders_run.py
```
* Pre spustenie vybraného spidera prejdite do priečinka */spiders* a zadajte príkaz (nahradíte *spider_name* názvom spidera):
```bash
scrapy crawl spider_name
```
* Pre kontrolu zoznamu cieľových stránok (pridávanie/mazanie) je potrebné prejsť do súboru *websites.json*. 
* Pre prehľad získaných textových dát otvorte databázový súbor *data.db* cez predtým nainštalovaný nástroj.
## Plánovanie spúšťania spiderov
* Pre Windows: Otvorte nástroj Task Scheduler a v sekcii *Actions* kliknite na *Create Basic Task*. Následne zvoľte interval a čas spustenia úlohy a pridajte súbor *schedule_spiders.bat* (predtým nahraďte v súbore cestu k projektu správnou cestou podľa umiestnenia na vašom systéme). Po dosiahnutí nastaveného času sa otvorí terminál a spustia sa spideri.

