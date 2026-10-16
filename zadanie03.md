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

