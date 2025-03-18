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
- **IDS** (Sistem za nadzor vsiljivega dostopa do aplikacije. Uporabil sem aplikacijo Snort, AIDE, HPING3, HYDRA, Nmap)
- **Wireshark** (Orodje za simulacijo in dokumentacijo ranljivosti nešifrirane komunikacije)

## Zahteve
- Raspberry Pi 3 ali novejši.
- Priklopljena LED lučka z ustreznimi povezavami.
- Nameščen Python 3.7+.
- Dostop do interneta.
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
- Prvi del namestitve je potekal po navodilih iz kibernetika.xyz Raspberry Pi 3.docx dokumenta z to razliko da sem namesto node.js uporabil Python in knjižnico Flask. Postavil sem svojo domeno na duckdns.org spletni strani in jo zaščitil z Let's Encrypt certifikatom na NGINX-u.
- V tem delu sem najprej namestil Python 3 in orodja za virtualna okolja, pripravil mapo za projekt, ustvaril in aktiviral virtualno okolje in namestil potrebne knjižnice (Flask, Flask-Limiter, RPi-GPIO). Ustvaril sem datoteko led_control.py, in mapo templates z datoteko index.html in podmapo css z .css datoteko. Po uspešnem testiranju aplikacije sem ustvaril led_control.service storitveno datoteko, ki je poskrbela za samodejno zaganjanje aplikacije ob zagonu (izpad elektrike ipd.) Na koncu, ko je vse delovalo tako kot mora sem z Flask-Limiter omejil število zahtev na web aplikacijo, kar bo preprečilo DDOS napade. V požarnem zidu sem pustil odprte samo tiste porte ki, so nujni za nemoteno delovanje aplikacije.
- Nato sem začel izvajati različne teste, ki so testirali kako je aplikacija varna in uporabna za delo, lahko tudi za komercialno uporabo.

## Testiranje

**Analiza vpliva šifriranja na zakasnitev**  

![image](https://github.com/user-attachments/assets/7bc5c77b-861b-4d01-b226-c835a8131f44)


S pomočjo Wireshark-a sem prestrezal podatke na http prometu:

![image](https://github.com/user-attachments/assets/ce6da9bb-7eb5-432a-8da9-a802bc36078f)



Aplikacija je dostopna preko SSL povezave na https://www.vajeiot.duckdns.org:7443 (port je obvezen)
        
git clone https://github.com/mijerrj/led_control.git
cd /led_control
