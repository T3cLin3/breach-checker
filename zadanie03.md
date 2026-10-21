# 1. Własne etykiety i pochodzenie warstw

PS C:\Users\Student\Bartosz-Hauff\breach-checker> docker inspect --format '{{json .Config.Labels}}' bartosz-hauff-frontend:v1
{"autor":"Bartosz Hauff","data":"16.10.2026","maintainer":"bartosz hauff"}
PS C:\Users\Student\Bartosz-Hauff\breach-checker> docker inspect --format '{{json .Config.Labels}}' bartosz-hauff-frontend:latest
{"autor":"Bartosz Hauff","data":"16.10.2026","maintainer":"bartosz hauff"}

PS C:\Users\Student\Bartosz-Hauff\breach-checker> docker history bartosz-hauff-frontend:v1
IMAGE          CREATED          CREATED BY                                      SIZE      COMMENT
c23b82ce71b8   3 minutes ago    EXPOSE [80/tcp]                                 0B        buildkit.dockerfile.v0
<missing>      3 minutes ago    RUN /bin/sh -c htmlhint /usr/share/nginx/htm…   4.1kB     buildkit.dockerfile.v0
<missing>      3 minutes ago    COPY . /usr/share/nginx/html # buildkit         32.8kB    buildkit.dockerfile.v0
<missing>      25 minutes ago   RUN /bin/sh -c apk add --no-cache nodejs npm…   102MB     buildkit.dockerfile.v0
<missing>      25 minutes ago   LABEL autor=Bartosz Hauff data=16.10.2026       0B        buildkit.dockerfile.v0
<missing>      25 minutes ago   LABEL maintainer=bartosz hauff                  0B        buildkit.dockerfile.v0
<missing>      3 weeks ago      RUN /bin/sh -c set -x     && apkArch="$(cat …   52.4MB    buildkit.dockerfile.v0
<missing>      3 weeks ago      ENV ACME_VERSION=0.4.1                          0B        buildkit.dockerfile.v0
<missing>      3 weeks ago      ENV NJS_RELEASE=1                               0B        buildkit.dockerfile.v0
<missing>      3 weeks ago      ENV NJS_VERSION=1.0.1                           0B        buildkit.dockerfile.v0
<missing>      3 weeks ago      CMD ["nginx" "-g" "daemon off;"]                0B        buildkit.dockerfile.v0
<missing>      3 weeks ago      STOPSIGNAL SIGQUIT                              0B        buildkit.dockerfile.v0
<missing>      3 weeks ago      EXPOSE map[80/tcp:{}]                           0B        buildkit.dockerfile.v0
<missing>      3 weeks ago      ENTRYPOINT ["/docker-entrypoint.sh"]            0B        buildkit.dockerfile.v0
<missing>      3 weeks ago      COPY 30-tune-worker-processes.sh /docker-ent…   16.4kB    buildkit.dockerfile.v0
<missing>      3 weeks ago      COPY 20-envsubst-on-templates.sh /docker-ent…   12.3kB    buildkit.dockerfile.v0
<missing>      3 weeks ago      COPY 15-local-resolvers.envsh /docker-entryp…   12.3kB    buildkit.dockerfile.v0
<missing>      3 weeks ago      COPY 10-listen-on-ipv6-by-default.sh /docker…   12.3kB    buildkit.dockerfile.v0
<missing>      3 weeks ago      COPY docker-entrypoint.sh / # buildkit          8.19kB    buildkit.dockerfile.v0
<missing>      3 weeks ago      RUN /bin/sh -c set -x     && addgroup -g 101…   5.72MB    buildkit.dockerfile.v0
<missing>      3 weeks ago      ENV DYNPKG_RELEASE=1                            0B        buildkit.dockerfile.v0
<missing>      3 weeks ago      ENV PKG_RELEASE=1                               0B        buildkit.dockerfile.v0
<missing>      3 weeks ago      ENV NGINX_VERSION=1.31.6                        0B        buildkit.dockerfile.v0
<missing>      3 weeks ago      LABEL maintainer=NGINX Docker Maintainers <d…   0B        buildkit.dockerfile.v0
<missing>      4 weeks ago      CMD ["/bin/sh"]                                 0B        buildkit.dockerfile.v0
<missing>      4 weeks ago      ADD alpine-minirootfs-3.24.2-x86_64.tar.gz /…   9.08MB    buildkit.dockerfile.v0


Z obrazu bazowego pochodzą warstwy od dołu, które stworzone zostały 3-4 tygodnie temu. Z mojego Dockerfile pochodzą warstwy stworzone później (dzisiaj tj. 16.10.2026). Niektóre warstwy mają rozmiar 0B ponieważ są to jedynie instrukcje, które dopisały metadane (CMD, ENTRYPOINT, ENV, LABEL, STOPSIGNAL), a nie instrukcje ADD, RUN lub COPY. Wyświetlana jest tylko moja wartość maintainer, ponieważ patrzymy na historię tego konkretnego kontenera, a nie tego, na czyim obrazie bazowym został stworzony.



# 2. Run działa raz

Zawartość pliku build.txt:
    - Dla kontener1: Wed Oct 21 18:57:40 UTC 2026
    - Dla kontener2: Wed Oct 21 18:57:40 UTC 2026

Wynik polecenia docker ps:
CONTAINER ID   IMAGE                   COMMAND                  CREATED              STATUS                   PORTS                                         NAMES
a5af7c91a7a7   moj_frontend            "/docker-entrypoint.…"   23 seconds ago       Up 22 seconds            0.0.0.0:8082->80/tcp, [::]:8082->80/tcp       kontener2
8fa39e376299   moj_frontend            "/docker-entrypoint.…"   About a minute ago   Up About a minute        0.0.0.0:8081->80/tcp, [::]:8081->80/tcp       kontener1
ca757559731a   574a4700333b            "uvicorn system_test…"   31 hours ago         Up 8 minutes (healthy)                                                 biblioteka_backend
d40a85be7db5   multigem-multigem-app   "uvicorn main:app --…"   4 days ago           Up 8 minutes             0.0.0.0:8080->8000/tcp, [::]:8080->8000/tcp   multigem-multigem-app-1

Instrukcja RUN wykonuje się tylko raz na etapie docker build, tworząc nową, niezmienną warstwę w obrazie. Plik build.txt został wygenerowany w momencie kompilacji obrazu, a kontenery tylko odczytują gotowy stan systemu plików tego obrazu, zamiast generować plik na nowo przy docker run.



# 3. Nadpisanie CMD

root   /usr/share/nginx/html;

Kopiujemy pliki do tego folderu, bo Nginx ma wpisane w parametrze root, że właśnie stamtąd pobiera i wyświetla stronę w przeglądarce.



# 4. Diagnoza błędnego COPY

docker exec bledny_kontener ls /usr/share/nginx
html
index.html
script.js
style.css

docker exec bledny_kontener ls /usr/share/nginx/html
50x.html
build.txt
index.html

Htmlhint sprawdził plik index.html z /usr/share/nginx. Build przeszedł bo z punktu widzenia Dockera polecenie COPY do /usr/share/nginx/ jest technicznie poprawne. Pliki skopiowane zostały o jeden folder wyżej (folder /html zawiera nadal fabryczny plik Nginx).



# 5. Usunięcie tagu a usunięcie obrazu

docker rmi breach-checker-frontend:latest
Untagged: breach-checker-frontend:latest

docker rmi breach-checker-frontend:v2
Untagged: breach-checker-frontend:v2
Deleted: sha256:283f92b9312fcee5f18c22e5df29ac1e2d5752096bf81088d46e99429a61bc35

Oto krótsza, zwięzła wersja do wpisania w pliku:

Polecenie docker rmi faktycznie usuwa obraz z dysku (Deleted) dopiero wtedy, gdy usuwamy ostatni istniejący tag wskazujący na ten obraz. Jeśli na to samo ID wskazuje jeszcze inna nazwa, Docker tylko ją odpina (Untagged), a pliki zostają na dysku.