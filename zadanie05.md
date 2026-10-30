# 1. Healthcheck backendu

PS C:\Users\Student\Bartosz-Hauff\breach-checker> docker compose up -d --build
[+] Building 1.2s (23/23) FINISHED                                                                                                                                                                                        
 => [internal] load local bake definitions                                                                                                                                                                           0.0s
 => => reading from stdin 1.09kB                                                                                                                                                                                     0.0s
 => [backend internal] load build definition from Dockerfile                                                                                                                                                         0.0s
 => => transferring dockerfile: 364B                                                                                                                                                                                 0.0s
 => [frontend internal] load build definition from Dockerfile                                                                                                                                                        0.0s
 => => transferring dockerfile: 318B                                                                                                                                                                                 0.0s
 => [backend internal] load metadata for docker.io/library/python:3.12-slim                                                                                                                                          0.7s
 => [frontend internal] load metadata for docker.io/library/nginx:alpine                                                                                                                                             0.0s
 => [frontend internal] load .dockerignore                                                                                                                                                                           0.0s
 => => transferring context: 66B                                                                                                                                                                                     0.0s
 => [frontend 1/5] FROM docker.io/library/nginx:alpine@sha256:df221db836e1754089190208cee7eeda94f233197056426eda74a43ab1abeac2                                                                                       0.0s
 => => resolve docker.io/library/nginx:alpine@sha256:df221db836e1754089190208cee7eeda94f233197056426eda74a43ab1abeac2                                                                                                0.0s
 => [frontend internal] load build context                                                                                                                                                                           0.0s
 => => transferring context: 120B                                                                                                                                                                                    0.0s
 => CACHED [frontend 2/5] RUN apk add --no-cache nodejs npm && npm install -g htmlhint                                                                                                                               0.0s
 => CACHED [frontend 3/5] COPY index.html style.css script.js /usr/share/nginx/html/                                                                                                                                 0.0s
 => CACHED [frontend 4/5] COPY nginx.conf /etc/nginx/conf.d/default.conf                                                                                                                                             0.0s
 => CACHED [frontend 5/5] RUN htmlhint /usr/share/nginx/html/index.html                                                                                                                                              0.0s
 => [frontend] exporting to image                                                                                                                                                                                    0.1s
 => => exporting layers                                                                                                                                                                                              0.0s
 => => exporting manifest sha256:cdc29008ea7587ee9587e0abbe9cd883ff10356d78e40150ae234ecb484a0b54                                                                                                                    0.0s
 => => exporting config sha256:2fc36dbee5be149b9155b45388d56104d28fe205636f0f7758dafa5d7f8dfe77                                                                                                                      0.0s
 => => exporting attestation manifest sha256:05bb4a43bb29bc6f89cd46a83e3df732c8c99222e21b3d8926dd389b50621c0f                                                                                                        0.0s
 => => exporting manifest list sha256:5f8ca3eb06c46be91bb746675af8d3ec6bf36b73555d6da611a04333e38550de                                                                                                               0.0s
 => => naming to docker.io/library/breach-checker-frontend:latest                                                                                                                                                    0.0s
 => => unpacking to docker.io/library/breach-checker-frontend:latest                                                                                                                                                 0.0s
 => [frontend] resolving provenance for metadata file                                                                                                                                                                0.0s
 => [backend internal] load .dockerignore                                                                                                                                                                            0.0s
 => => transferring context: 79B                                                                                                                                                                                     0.0s
 => [backend 1/5] FROM docker.io/library/python:3.12-slim@sha256:aa943ce411423c7582288f18707ff66eddcbaeb510502d747a72aeb34f30d159                                                                                    0.0s
 => => resolve docker.io/library/python:3.12-slim@sha256:aa943ce411423c7582288f18707ff66eddcbaeb510502d747a72aeb34f30d159                                                                                            0.0s
 => [backend internal] load build context                                                                                                                                                                            0.0s
 => => transferring context: 63B                                                                                                                                                                                     0.0s
 => CACHED [backend 2/5] WORKDIR /app                                                                                                                                                                                0.0s
 => CACHED [backend 3/5] COPY requirements.txt .                                                                                                                                                                     0.0s
 => CACHED [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt                                                                                                                                          0.0s
 => CACHED [backend 5/5] COPY . /app/                                                                                                                                                                                0.0s
 => [backend] exporting to image                                                                                                                                                                                     0.1s
 => => exporting layers                                                                                                                                                                                              0.0s
 => => exporting manifest sha256:db8d42e0131429363db7a4afc3d9f9b1da4928bb702dc4fa7af208308da0b2e9                                                                                                                    0.0s
 => => exporting config sha256:b145aceebbc6d1428d735aea6b5feb133cb92993bd89eebaf7cba63ee6b8fbe1                                                                                                                      0.0s
 => => exporting attestation manifest sha256:00e3c3a6a20380dd076f495e47db3afe3fb194cc395813879f4ad695614ce9c0                                                                                                        0.0s
 => => exporting manifest list sha256:3da225dac590efb56e6df5f56cc6fbf551e7eaa0891821ef588119b93a011020                                                                                                               0.0s
 => => naming to docker.io/library/breach-checker-backend:latest                                                                                                                                                     0.0s
 => => unpacking to docker.io/library/breach-checker-backend:latest                                                                                                                                                  0.0s
 => [backend] resolving provenance for metadata file                                                                                                                                                                 0.0s
[+] up 6/6
 ✔ Image breach-checker-frontend       Built                                                                                                                                                                          1.3s
 ✔ Image breach-checker-backend        Built                                                                                                                                                                          1.3s
 ✔ Network breach-checker_default      Created                                                                                                                                                                        0.0s
 ✔ Container breach-checker-db-1       Healthy                                                                                                                                                                        5.8s
 ✔ Container breach-checker-backend-1  Healthy                                                                                                                                                                       11.4s
 ✔ Container breach-checker-frontend-1 Started 

 PS C:\Users\Student\Bartosz-Hauff\breach-checker> docker compose ps
NAME                        IMAGE                     COMMAND                  SERVICE    CREATED          STATUS                    PORTS
breach-checker-backend-1    breach-checker-backend    "python app.py"          backend    16 seconds ago   Up 10 seconds (healthy)   5000/tcp
breach-checker-db-1         postgres:16-alpine        "docker-entrypoint.s…"   db         16 seconds ago   Up 15 seconds (healthy)   5432/tcp
breach-checker-frontend-1   breach-checker-frontend   "/docker-entrypoint.…"   frontend   16 seconds ago   Up 4 seconds              0.0.0.0:8080->80/tcp, [::]:8080->80/tcp

# 2. Trwałość bazy

Po INSERT:

PS C:\Users\Student\Bartosz-Hauff\breach-checker> # Windows PowerShell
>> '{"hash":"bc45408273d7e1914b741c3407b0b559764f7876"}' | curl.exe -X POST http://localhost:8080/api/check -H "Content-Type: application/json" -d '@-'
>> 
{"found":true}


Po docker compose down

PS C:\Users\Student\Bartosz-Hauff\breach-checker> # Windows PowerShell
>> '{"hash":"bc45408273d7e1914b741c3407b0b559764f7876"}' | curl.exe -X POST http://localhost:8080/api/check -H "Content-Type: application/json" -d '@-'
>> 
{"found":true}


Po docker compose down -v
                                                                                                                                                               0.2s
PS C:\Users\Student\Bartosz-Hauff\breach-checker> # Windows PowerShell
>> '{"hash":"bc45408273d7e1914b741c3407b0b559764f7876"}' | curl.exe -X POST http://localhost:8080/api/check -H "Content-Type: application/json" -d '@-'
>> 
{"found":false}

Po dodaniu nowych danych do bazy polecenie zwraca true, ponieważ znajduje te dane.
Wpisanie docker compose down zatrzymuje jedynie kontener - dane w wolumenach pozostają niezmienione.
Wpisanie docker compose down -v usuwa wolumeny czyli przy kolejnym uruchomieniu zostaję one przywrócone do stanu sprzed INSERT'a - dlatego jest false.

# 3. Skalowanie

PS C:\Users\Student\Bartosz-Hauff\breach-checker> docker compose ps
NAME                        IMAGE                     COMMAND                  SERVICE    CREATED          STATUS                    PORTS
breach-checker-backend-1    breach-checker-backend    "python app.py"          backend    6 minutes ago    Up 6 minutes (healthy)    5000/tcp
breach-checker-backend-2    breach-checker-backend    "python app.py"          backend    45 seconds ago   Up 44 seconds (healthy)   5000/tcp
breach-checker-backend-3    breach-checker-backend    "python app.py"          backend    45 seconds ago   Up 44 seconds (healthy)   5000/tcp
breach-checker-db-1         postgres:16-alpine        "docker-entrypoint.s…"   db         6 minutes ago    Up 6 minutes (healthy)    5432/tcp
breach-checker-frontend-1   breach-checker-frontend   "/docker-entrypoint.…"   frontend   6 minutes ago    Up 5 minutes              0.0.0.0:8080->80/tcp, [::]:8080->80/tcp

PS C:\Users\Student\Bartosz-Hauff\breach-checker> docker compose exec frontend nslookup backend
Server:         127.0.0.11
Address:        127.0.0.11:53

Non-authoritative answer:

Non-authoritative answer:
Name:   backend
Address: 172.19.0.5
Name:   backend
Address: 172.19.0.3
Name:   backend
Address: 172.19.0.6

backend-1  | check: hash=bc454...
backend-1  | 172.19.0.6 - - [30/Oct/2026 13:51:56] "POST /check HTTP/1.1" 200 -
backend-1  | check: hash=bc454...
backend-1  | 172.19.0.6 - - [30/Oct/2026 13:51:56] "POST /check HTTP/1.1" 200 -
backend-1  | check: hash=bc454...
backend-1  | 172.19.0.6 - - [30/Oct/2026 13:51:56] "POST /check HTTP/1.1" 200 -

backend-1  | check: hash=bc454...
backend-1  | 172.19.0.6 - - [30/Oct/2026 13:51:56] "POST /check HTTP/1.1" 200 -
backend-1  | check: hash=bc454...
backend-1  | 172.19.0.6 - - [30/Oct/2026 13:51:56] "POST /check HTTP/1.1" 200 -
backend-1  | check: hash=bc454...
backend-1  | 172.19.0.6 - - [30/Oct/2026 13:51:56] "POST /check HTTP/1.1" 200 -


Przed restartem frontend nie wiedział o nowych replikach i kierował ruch do starego adresu, ponieważ przetłumaczyć nazwę backend tylko raz przy uruchomieniu.
Restart zmusił go do ponownego odpytania DNS i wykrycia 3 kopii backendu. Skalowanie byłoby niemożliwe przy porcie 5000:5000, ponieważ doszłoby do konfliktu portów.