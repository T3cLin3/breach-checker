# 1. Raport podatności

breach-checker-frontend:prod    -   Total: 49 (HIGH: 49, CRITICAL: 0)    -   bez `--ignore-unfixed`

breach-checker-frontend:prod    -   Total: 3 (HIGH: 3, CRITICAL: 0)    -   z `--ignore-unfixed`

breach-checker-backend:prod    -   Total: 3 (HIGH: 3, CRITICAL: 0)    -   bez `--ignore-unfixed`

breach-checker-backend:prod    -   Total: 2 (HIGH: 2, CRITICAL: 0)    -   z `--ignore-unfixed`

Użycie flagii `--pull` zmniejszyło liczbę wykrytych podatności w przypadku frontendu, ponieważ pobrało najnowsze wersje obrazów z wgranymi poprawkami bezpieczeństwa.

# 2. Utwardzenie kontenera w działaniu

backend-1  | FileNotFoundError: [Errno 2] No usable temporary directory found in ['/tmp', '/var/tmp', '/usr/tmp', '/app']

PS C:\Users\Student\Bartosz-Hauff\breach-checker> docker compose exec backend touch /etc/test
touch: cannot touch '/etc/test': Read-only file system
PS C:\Users\Student\Bartosz-Hauff\breach-checker> docker compose exec backend touch /tmp/test
PS C:\Users\Student\Bartosz-Hauff\breach-checker> docker compose exec backend grep CapEff /proc/1/status
CapEff: 0000000000000000

PS C:\Users\Student\Bartosz-Hauff\breach-checker> docker compose exec backend pytest
================================================================================================== test session starts ===================================================================================================
platform linux -- Python 3.12.16, pytest-8.4.2, pluggy-1.7.0
rootdir: /app
collected 7 items                                                                                                                                                                                                        

tests/test_check.py .......                                                                                                                                                                                        [100%]

=================================================================================================== 7 passed in 0.08s ====================================================================================================

Ustawienie `read_only: true` uniemożliwia atakującemu modyfikację plików aplikacji i instalację złośliwego oprogramowania wewnątrz kontenera, natomiast `cap_drop: [ALL]` oraz `no-new-privileges:true` odbierają procesom zbędne uprawnienia jądra i blokują próby eskalacji uprawnień. W przeciwieństwie do `USER appuser`, która ogranicza zapis jedynie na poziomie uprawnień konkretnego użytkownika w systemie, flaga `read_only: true` blokuje zapis dla każdego procesu na poziomie całego systemu plików kontenera (nawet dla użytkownika root, z wyjątkiem jawnie zamontowanych wolumenów i tmpfs).

# 3. Sekret w usuniętym pliku

PS C:\Users\Student\Bartosz-Hauff\lab07-sekret> docker history sekret-demo:plik
IMAGE          CREATED          CREATED BY                                      SIZE      COMMENT
e44936bca5cc   18 seconds ago   RUN /bin/sh -c rm /tmp/klucz.txt # buildkit     8.19kB    buildkit.dockerfile.v0
<missing>      18 seconds ago   RUN /bin/sh -c test -s /tmp/klucz.txt && ech…   4.1kB     buildkit.dockerfile.v0
<missing>      19 seconds ago   COPY klucz.txt /tmp/klucz.txt # buildkit        12.3kB    buildkit.dockerfile.v0
<missing>      7 days ago       CMD ["/bin/sh"]                                 0B        buildkit.dockerfile.v0
<missing>      7 days ago       ADD alpine-minirootfs-3.22.8-x86_64.tar.gz /…   8.97MB    buildkit.dockerfile.v0

PS C:\Users\Student\Bartosz-Hauff\lab07-sekret> Get-ChildItem obraz/blobs/sha256 | Where-Object { tar -tf $_.FullName 2>$null | Select-String '^tmp/klucz.txt$' } | ForEach-Object { tar -xOf $_.FullName tmp/klucz.txt }
tajny-klucz-bartosz

Instrukcja `RUN rm` nie usunęła sekretu z obrazu, ponieważ każda instrukcja w Dockerfile tworzy osobną, niemutowalną warstwę, a usunięcie pliku w kolejnym kroku jedynie ukrywa go w finalnym widoku systemu plików, pozostawiając jego oryginalną zawartość we wcześniejszej warstwie (COPY). Zamiast kopiować plik na stałe do obrazu, klucz należało przekazać bezpiecznie podczas budowania za pomocą mechanizmu BuildKit secrets (RUN --mount=type=secret,id=klucz ...), który montuje plik tymczasowo wyłącznie na czas wykonywania konkretnej instrukcji bez zapisywania go w historii warstw.