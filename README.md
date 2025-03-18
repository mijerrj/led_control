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
- **Beleženje, nadzor in odzivi na incidente (Snort logi, sistemski logi, ELK-stek)

## Zahteve
- Raspberry Pi 3 ali novejši.
- Priklopljena LED lučka z ustreznimi povezavami.
- Nameščen Python 3.7+.
- Dostop do interneta.

## Priklop LED in stikala
1. **LED lučka**:
   - **GPIO PIN 17 (Pin 11)** → Upor (330Ω) → Anoda (daljša žička) LED.
   - **GND** → Katoda (krajša žička) LED.

2. **Stikalo**:
   - **GPIO PIN 27 (Pin 13)** → Ena stran stikala.
   - **GND** → Druga stran stikala.

## Namestitev
- Prvi del namestitve je potekal po navodilih iz kibernetika.xyz Raspberry Pi 3.docx dokumenta.
- V drugem delu sem najprej namestil Python 3 in orodja za virtualna okolja, pripravil mapo za projekt, ustvaril in aktiviral virtualno okolje in namestil potrebne knjižnice (Flask, Flask-Limiter, RPi-GPIO). Ustvaril sem datoteko led_control.py, in mapo templates z datoteko index. html in podmapo css z .css datoteko. Po testiranju aplikacije sem ustvaril led_control.service storitveno datoteko ki je poskrbela za samodejno zaganjanje aplikacije ob zagonu (izpad elektrike ipd.) Na koncu, ko je vse delovalo tako kot mora sem z Flask-Limiter omejil število zahtev na web aplikacijo, kar bo preprečilo DDOS napade. V požarnem zidu sem pustil odprte porte samo tiste ki, so nujni za nemoteno delovanje aplikacije.

Aplikacija je dostopna preko SSL povezave na https://www.vajeiot.duckdns.org:7443 (port je obvezen)
        
git clone https://github.com/mijerrj/led_control.git
cd /led_control
