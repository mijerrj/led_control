# LED Control Application

Projekt za nadzor LED lučke preko spletne aplikacije, ki teče na Raspberry Pi 3 z uporabo Flask in Nginx.

## Funkcionalnosti
- Vklop in izklop LED lučke preko spletne aplikacije.
- Prikaz trenutnega stanja LED (prižgana/ugasnjena).
- Varovanje aplikacije pred DDoS napadi z Nginx in Flask-Limiter.
- Samodejni zagon aplikacije ob zagonu sistema.

## Uporabljene tehnologije
- **Raspberry Pi 3**
- **Ubuntu Server**
- **Flask** (Python framework za spletne aplikacije)
- **Nginx** (obratni proxy strežnik)
- **Certbot** (SSL certifikati)
- **venv** (virtualno okolje za namestitev aplikacije, knjižnic in za zagon)
- **Systemd** (upravljanje storitev)
- **ufw** (požarni zid)
- **DuckDNS** (spletna domena)
- **GPIO** (pini na RPI za nadzor LED na Raspberry Pi)
- **API** (končne točke za upravljanje in branje statusa)
- **IDS** (Sistem za nadzor vsiljivega dostopa do aplikacije. Uporabil sem aplikacijo Snort, AIDE, HPING3, HYDRA, Nmap, HTOP)
- **Wireshark** (Orodje za simulacijo in dokumentacijo ranljivosti nešifrirane komunikacije)

## Zahteve
- Raspberry Pi 3 ali novejši.
- Priklopljena LED lučka z ustreznimi povezavami.
- Nameščen Python 3.7+.
- Dostop do interneta.
- Analiza vpliva šifriranja na zakasnitev in porabo virov
- Implementacija mehanizma za nadzor dostopa do API-končnih točk za LED in tipko.
- Zavarovanje dostopa s token-based avtentikacijo (npr. JWT).
- Zaznavanje varnostnih groženj v IoT s sistemom za zaznavanje vdorov (IDS).
- Omogočanje požarnega zidu UFW in omejitev dovoljenih vrat.
- Spremljanje celovitosti datotek z AIDE (Advanced Intrusion Detection Environment).
- Izvajanje skeniranja odprtih vrat z Nmap in analiza morebitnih ranljivosti.
- Simulacija brute-force napada na SSH in dokumentiranje strategij omilitve.
- Beleženje, nadzor in odzivi na incidente** (Snort logi, sistemski logi, ELK-stek).

## Priklop LED in stikala
1. **LED lučka**:
   - **GPIO PIN 17 (Pin 11)** → Upor (330Ω) → Anoda (daljša žička) LED.
   - **GND** → Katoda (krajša žička) LED.

2. **Stikalo**:
   - **GPIO PIN 27 (Pin 13)** → Ena stran stikala.
   - **GND** → Druga stran stikala.

## Namestitev
- Prvi del namestitve je potekal po navodilih iz kibernetika.xyz Raspberry Pi 3.docx dokumenta z to razliko da sem namesto node.js uporabil Python in knjižnico Flask. Postavil sem svojo domeno na duckdns.org spletni strani in jo zaščitil z Let's Encrypt certifikatom na NGINX-u. Ker sem doma imel port 443 že zaseden sem za TLS povezavo uporabil port 7443.
- V tem delu sem najprej namestil Python 3 in orodja za virtualna okolja, pripravil mapo za projekt, ustvaril in aktiviral virtualno okolje in namestil potrebne knjižnice (Flask, Flask-Limiter, RPi-GPIO). Ustvaril sem datoteko led_control.py, in mapo templates z datoteko index.html in podmapo css z .css datoteko. Po uspešnem testiranju aplikacije sem ustvaril led_control.service storitveno datoteko, ki je poskrbela za samodejno zaganjanje aplikacije ob zagonu (izpad elektrike ipd.) Na koncu, ko je vse delovalo tako kot mora sem z Flask-Limiter omejil število zahtev na web aplikacijo, kar bo preprečilo DDOS napade. V požarnem zidu sem pustil odprte samo tiste porte ki, so nujni za nemoteno delovanje aplikacije.
- Nato sem začel izvajati različne teste, ki so testirali kako je aplikacija varna in uporabna za delo, lahko tudi za komercialno uporabo.

## Testiranje

**Analiza vpliva šifriranja na zakasnitev**  

![image](https://github.com/user-attachments/assets/7bc5c77b-861b-4d01-b226-c835a8131f44)


**Poraba virov pri zaščitenem in nezaščitenem prometu z HTOP**


*Nezaščiteno*
![image](https://github.com/user-attachments/assets/f87ac3e4-ef9c-45f3-bd65-2274e9c79d33)


*Zaščiteno*

![image](https://github.com/user-attachments/assets/76d96fb2-f9a5-4898-a049-8ac4c6595637)


**Prestrezanje podatkov na http prometu z tcpdump**

*Nezaščiteno*

![image](https://github.com/user-attachments/assets/0a645eea-22e3-47b1-8632-fba6a358c591)

*Zaščiteno*

![image](https://github.com/user-attachments/assets/2a65cc3a-437d-44cd-ab6f-593becc61ff9)


**Simulacija BRUTE-FORCE napada**

![image](https://github.com/user-attachments/assets/4de0cc7f-896a-4778-b40f-050e867a75bf)


**Simulacija BRUTE-FORCE napada na SSH**

![image](https://github.com/user-attachments/assets/3b35d16d-b8f3-4aa9-b826-20a25d5fc0af)

Malo ironično je, da zaradi zastarelih algoritmov ključev kot je diffie-hellman-group1-sha1, ki velja za nevarnega, brute-force napad ni uspel.


**Simulacija ne avtoriziranega dostopa do API-ja (curl)**

![image](https://github.com/user-attachments/assets/53aca40e-c664-4055-9bb5-c590dfe6945b)


**Simulacija omrežnega napada (HPING3)**

![image](https://github.com/user-attachments/assets/075c9d08-13d7-401e-b3ed-f87a7c267b36)


**Spremljanje celovitosti datotek (AIDE)**

Vsi podatki iz tega testa se nahajajo v datoteki Aide-report.txt


**Skeniranje odprtih vrat z NMAP**

![image](https://github.com/user-attachments/assets/b954f752-e76f-4b66-b938-0486966a6b2b)

![image](https://github.com/user-attachments/assets/80b911e9-e7c7-45c7-85a1-1cbccebb7950)


**Omogočanje požarnega zidu (ufw) in omejitev dovoljenih vrat**

![image](https://github.com/user-attachments/assets/0c5205d0-5bb9-4afa-b5ab-c00d5673fc8e)

Preden je bil projekt zaključen sem:
- ⚠️ Izklopil Telnet (port 23) in FTP (port 21).
- ⚠️ Posodobil Dropbear SSH (port 22) in v config dodal AllowUsers za samo en IP.
- ⚠️ Onemogočil SMB in gostujoči dostop.
- ⚠️ Konfiguracija za HTTPS (port 7443) je ostala nespremenjena ker je ustrezna.
- ⚠️ HTTP zahteve sem preusmeril na HTTPS (port 7443).



**Beleženje zahtevkov na API, vključno z neuspelimi poizkusi**

![image](https://github.com/user-attachments/assets/0103b5f0-b3be-45ef-88b2-678c6b96e4ca)


Aplikacija je dostopna preko SSL povezave na https://www.vajeiot.duckdns.org:7443 (port je obvezen)
        
git clone https://github.com/mijerrj/led_control.git
cd /led_control
