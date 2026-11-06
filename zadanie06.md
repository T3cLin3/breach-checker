# 1. Własne testy

PS C:\Users\Student\Bartosz-Hauff\breach-checker> docker compose exec backend pytest
================================================================================================== test session starts ===================================================================================================
platform linux -- Python 3.12.16, pytest-8.4.2, pluggy-1.7.0
rootdir: /app
collected 7 items                                                                                                                                                                                                        

tests/test_check.py .......                                                                                                                                                                                        [100%]

=================================================================================================== 7 passed in 0.08s ====================================================================================================
PS C:\Users\Student\Bartosz-Hauff\breach-checker> 

PS C:\Users\Student\Bartosz-Hauff\breach-checker> docker compose exec backend pytest
================================================================================================== test session starts ===================================================================================================
platform linux -- Python 3.12.16, pytest-8.4.2, pluggy-1.7.0
rootdir: /app
collected 7 items                                                                                                                                                                                                        

tests/test_check.py ....F..                                                                                                                                                                                        [100%]

======================================================================================================== FAILURES ========================================================================================================
______________________________________________________________________________________________ test_uppercase_hash_is_found ______________________________________________________________________________________________

client = <FlaskClient <Flask 'app'>>

    def test_uppercase_hash_is_found(client):
        response = client.post("/check", json={"hash": LEAKED.upper()})
>       assert response.status_code == 200
E       assert 400 == 200
E        +  where 400 = <WrapperTestResponse streamed [400 BAD REQUEST]>.status_code

tests/test_check.py:27: AssertionError
================================================================================================ short test summary info =================================================================================================
FAILED tests/test_check.py::test_uppercase_hash_is_found - assert 400 == 200
============================================================================================== 1 failed, 6 passed in 0.09s ===============================================================================================

What's next:
    Debug this Compose error with Gordon → docker ai "help me fix this compose error"
PS C:\Users\Student\Bartosz-Hauff\breach-checker> 

Po usunięciu .lower() z kodu app.py, serwer przestał konwertować zapytania użytkownika do małych liter. Oryginalne 4 testy z zajęć wysyłały już hashe zapisane małymi literami, dlatego tylko test zawierający hash z wielkimi literami nie przechodzi.

# 2. Awaria a blokada

PS C:\Users\Student\Bartosz-Hauff\breach-checker> '{"hash":"7c4a8d09ca3762af61e59520943dc26494f8941b"}' | curl.exe -s -o blad.html -w "HTTP %{http_code}\n" -X POST http://localhost:8080/api/check -H "Content-Type: application/json" -d '@-'
HTTP 500

PS C:\Users\Student\Bartosz-Hauff\breach-checker> docker compose ps -a          
NAME                        IMAGE                                                                     COMMAND                  SERVICE    CREATED          STATUS                     PORTS
breach-checker-backend-1    breach-checker-backend                                                    "flask --app app run…"   backend    38 minutes ago   Exited (1) 2 seconds ago   
breach-checker-db-1         postgres:16-alpine                                                        "docker-entrypoint.s…"   db         38 minutes ago   Exited (0) 4 minutes ago   
breach-checker-frontend-1   sha256:5f8ca3eb06c46be91bb746675af8d3ec6bf36b73555d6da611a04333e38550de   "/docker-entrypoint.…"   frontend   7 days ago       Up 37 minutes              0.0.0.0:8080->80/tcp, [::]:8080->80/tcp
PS C:\Users\Student\Bartosz-Hauff\breach-checker> 

PS C:\Users\Student\Bartosz-Hauff\breach-checker> docker inspect --format '{{.State.Status}} {{.State.ExitCode}}' breach-checker-backend-1
exited 1
PS C:\Users\Student\Bartosz-Hauff\breach-checker> 

| Wymiar porównania | Krok 4: Blokada (kontener, który „wisi”) | Krok 5: Awaria (zatrzymana baza db) |
| :--- | :--- | :--- |
| **Status w `docker compose ps`** | `Up (healthy)` – proces backendu żyje i odpowiada na healthcheck, Docker uważa, że wszystko jest w porządku. | `Up (unhealthy)` (lub status błędu/restartu) – kontener po restarcie nie przechodzi testu zdrowia, bo baza nie odpowiada. |
| **CPU w `docker stats`** | **Bliskie 0%** – aplikacja nie wykonuje żadnych operacji procesora, wątek bezczynnie czeka na zwolnienie blokady tabeli. | **Bliskie 0%** – proces nie wykonuje obliczeń, oczekuje w pętli lub na timeout nawiązania połączenia sieciowego. |
| **Ostatnie linie logów** | Widoczna linia wejścia żądania (np. `check: hash=...`), ale **brak linii podsumowującej** z kodem HTTP `200`. | Logi zalane błędami połączenia z bazą danych (np. `ConnectionRefusedError` lub `OperationalError: could not connect to server`). |
| **Co dostał klient** | Błąd **504 Gateway Time-out** zwracany przez serwer Nginx. | Błąd **500 Internal Server Error** (bądź 502 Bad Gateway) zawierający wygenerowany przez aplikację plik `blad.html`. |
| **Po jakim czasie** | Dopiero **po 60 sekundach** (po upływie limitu czasu oczekiwania serwera proxy). | **Natychmiast** (lub po bardzo krótkim czasie próby nawiązania połączenia, rzędu pojedynczych sekund). |

Plik blad.html zawiera Traceback błędów, szczegółowo opisujący błąd połączenia z bazą danych, ścieżki do plików źródłowych projektu oraz zmienne środowiskowe. Pokazywanie pełnego tracebacku na serwerze produkcyjnym to problem bezpieczeństwa, ponieważ ujawniamy potencjalnemu atakującemu wewnętrzną strukturę katalogów serwera, wersje używanych bibliotek, nazwy funkcji a czasem nawet poufne dane.

# Frontend w trybie deweloperskim

PS C:\Users\Student\Bartosz-Hauff\breach-checker> curl.exe http://localhost:8080/nginx.conf
server {
    listen 80;

    # Pliki strony (index.html, style.css, script.js)
    location / {
        root /usr/share/nginx/html;
        index index.html;
    }

    # Wszystko pod /api/ nginx przekazuje do usługi backend w sieci Compose
    location /api/ {
        proxy_pass http://backend:5000/;
    }
}
PS C:\Users\Student\Bartosz-Hauff\breach-checker> 

PS C:\Users\Student\Bartosz-Hauff\breach-checker> curl.exe -I http://localhost:8080/nginx.conf
HTTP/1.1 404 Not Found
Server: nginx/1.31.6
Date: Fri, 06 Nov 2026 13:50:11 GMT
Content-Type: text/html
Content-Length: 153
Connection: keep-alive

PS C:\Users\Student\Bartosz-Hauff\breach-checker> 

Zgodnie z plikiem Dockerfile, proces budowania obrazu produkcyjnego jawnie kopiuje do katalogu serwowanego przez Nginx (/usr/share/nginx/html) wyłącznie pliki statyczne stanowiące właściwą stronę webową (takie jak index.html, style.css, script.js). Pliki konfiguracyjne serwera czy sam Dockerfile pozostają poza tym folderem, dzięki czemu nie są publicznie serwowane przez serwer WWW klientom zewnętrznym.
Montując cały katalog roboczy projektu za pomocą jednego bind mounta wystawiamy do sieci wszystkie znajdujące się w nim pliki, w tym pliki konfiguracyjne aplikacji, pliki kontenerów (np. Dockerfile), ukryte katalogi systemowe lub pliki ze statycznie wpisanymi hasłami i kluczami API. Daje to potencjalnemu atakującemu pełen wgląd w architekturę techniczną naszej infrastruktury oraz ułatwia odnalezienie wektorów ataku.