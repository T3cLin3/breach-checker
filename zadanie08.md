# 1. Frontend w pipeline

https://github.com/T3cLin3/breach-checker/actions/runs/44748786700

```text
 > [lint 5/5] RUN htmlhint index.html:
0.150 
0.159    /site/index.html
0.160       L14 |        <h1>Breach Checker
0.160                    ^ Tag must be paired, missing: [ </h1> ], start tag match failed [ <h1> ] on line 14. (tag-pair)
0.160 
0.161 Scanned 1 files, found 1 errors in 1 files (12 ms)
------
Dockerfile:7
--------------------
   5 |     WORKDIR /site
   6 |     COPY index.html style.css script.js ./
   7 | >>> RUN htmlhint index.html
   8 |     
   9 |     # --- Etap 2: obraz końcowy - sam nginx i pliki strony ---
--------------------
ERROR: failed to build: failed to solve: process "/bin/sh -c htmlhint index.html" did not complete successfully: exit code: 1
Error: Process completed with exit code 1.
```

https://github.com/T3cLin3/breach-checker/actions/runs/44748974843

W tym zielonym uruchomieniu `verify` pobiera i sprawdza oba obrazy produkcyjne z rejestru (backend oraz frontend), ponieważ dodałny został job budujący i publikujący do GHCR oraz podpięty został do `docker-compose.ci.yml` i `verify`. Wcześniej publikowany i pobierany rejestru był wyłącznie obraz backendu, a frontend powstawał w trakcie uruchamiania z lokalnego kontekstu.

# 2. `latest` tylko po weryfikacji

https://github.com/T3cLin3/breach-checker/actions/runs/45851748901

https://github.com/T3cLin3/breach-checker/actions/runs/45852934770

Po nieudanym uruchomieniu tag `latest` backendu nadal wskazywał na poprzednią, zweryfikowaną wersję (z wcześniejszego udanego commita), ponieważ job `promote` został pominięty i nie przeniósł tagu na zepsuty obraz. Jest to kluczowe dla osoby pobierającej obraz bez podawania tagu, bo nie dostanie ona przez przypadek niedziałającej kompilacji z `127.0.0.1:5000`. Dzięki temu `latest` pozostaje bezpiecznym wskaźnikiem na ostatni obraz, który przeszedł testy i weryfikację.

# 3. Publiczny pakiet  - odczyt bez tokenu, zapis z tokenem

```text
PS D:\Users\asass\Desktop\Programowanie - sem3\Laby - mw\breach-checker> docker logout ghcr.io
Removing login credentials for ghcr.io
```

```text
PS D:\Users\asass\Desktop\Programowanie - sem3\Laby - mw\breach-checker> docker pull ghcr.io/t3clin3/breach-checker-backend:latest
latest: Pulling from t3clin3/breach-checker-backend
37aac3b4c58b: Pull complete 
30cf67d7101c: Pull complete 
3257a4f28f7b: Pull complete 
20a29117e585: Pull complete 
e3e428093f5e: Pull complete 
45407919f870: Pull complete 
b3a894f93095: Pull complete 
286d8c291daa: Pull complete 
83a14706aa6d: Pull complete 
Digest: sha256:65229f609afbdd7eebdfc534763cd2c5618c5f3082a5b01e4ca87625c013ac6b
Status: Downloaded newer image for ghcr.io/t3clin3/breach-checker-backend:latest
ghcr.io/t3clin3/breach-checker-backend:latest
```

```text
PS D:\Users\asass\Desktop\Programowanie - sem3\Laby - mw\breach-checker> docker pull ghcr.io/t3clin3/breach-checker-backend:517d67a8d928db17578cdbdd7b2ad189e8988a93
517d67a8d928db17578cdbdd7b2ad189e8988a93: Pulling from t3clin3/breach-checker-backend
Digest: sha256:65229f609afbdd7eebdfc534763cd2c5618c5f3082a5b01e4ca87625c013ac6b
Status: Downloaded newer image for ghcr.io/t3clin3/breach-checker-backend:517d67a8d928db17578cdbdd7b2ad189e8988a93
ghcr.io/t3clin3/breach-checker-backend:517d67a8d928db17578cdbdd7b2ad189e8988a93
```

```text
PS D:\Users\asass\Desktop\Programowanie - sem3\Laby - mw\breach-checker> docker images --digests ghcr.io/t3clin3/breach-checker-backend
REPOSITORY                               TAG                                        DIGEST                                                                    IMAGE ID       CREATED          SIZE
ghcr.io/t3clin3/breach-checker-backend   517d67a8d928db17578cdbdd7b2ad189e8988a93   sha256:65229f609afbdd7eebdfc534763cd2c5618c5f3082a5b01e4ca87625c013ac6b   65229f609afb   16 minutes ago   212MB
ghcr.io/t3clin3/breach-checker-backend   latest                                     sha256:65229f609afbdd7eebdfc534763cd2c5618c5f3082a5b01e4ca87625c013ac6b   65229f609afb   16 minutes ago   212MB
```

```text
PS D:\Users\asass\Desktop\Programowanie - sem3\Laby - mw\breach-checker> docker push ghcr.io/t3clin3/breach-checker-backend:latest
The push refers to repository [ghcr.io/t3clin3/breach-checker-backend]
286d8c291daa: Layer already exists 
83a14706aa6d: Layer already exists 
30cf67d7101c: Layer already exists 
e3e428093f5e: Layer already exists 
3257a4f28f7b: Layer already exists 
20a29117e585: Layer already exists 
b3a894f93095: Layer already exists 
37aac3b4c58b: Layer already exists 
45407919f870: Layer already exists 
latest: digest: sha256:65229f609afbdd7eebdfc534763cd2c5618c5f3082a5b01e4ca87625c013ac6b size: 2199
```

Digest `sha256:...` dla tagów `latest` oraz skrótu ostatniego commita jest taki sam (gdy oba wskazują na zweryfikowany obraz), co potwierdza, że odnoszą się do identycznej zawartości warstw. Pobieranie (`docker pull`) zadziałało bez logowania, ponieważ pakiet jest publiczny i odczyt nie wymaga uwierzytelnienia , natomiast wysyłanie (`docker push`) zakończyło się odmową dostępu, bo publikowanie do rejestru wymaga uwierzytelnienia z odpowiednimi uprawnieniami. Token z kroku 1 (z zakresem `write:packages`) służył do ręcznego uwierzytelniania w GHCR i nadania uprawnień do publikowania pakietów w rejestrze (w przeciwieństwei do anonimowego pobierania).
Pomimo prób naprawienia, AI nie pomogło osiągnąć oczekiwanego efektu a jedynie ciągle ten zamieszczony powyżej :/
