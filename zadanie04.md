# 1. Endopoint GET /health

{"status":"ok"}

172.18.0.1 - - [23/Oct/2026 12:44:36] "GET /health HTTP/1.1" 200 -

# 2. Kontener diagnostyczny healthcheck-probe

PS D:\Users\asass\Desktop\Programowanie - sem3\Laby - mw\breach-checker> docker run --rm --network breach-net healthcheck-probe
backend: OK

PS D:\Users\asass\Desktop\Programowanie - sem3\Laby - mw\breach-checker> docker run --rm healthcheck-probe
backend: UNREACHABLE

PS D:\Users\asass\Desktop\Programowanie - sem3\Laby - mw\breach-checker> docker stop backend
backend
PS D:\Users\asass\Desktop\Programowanie - sem3\Laby - mw\breach-checker> docker run --rm --network breach-net healthcheck-probe
backend: UNREACHABLE
PS D:\Users\asass\Desktop\Programowanie - sem3\Laby - mw\breach-checker> docker start backend
backend

Uruchomienie kontenera bez flagi --network umieszcza go w domyślnej sieci bridge, w której nie działa automatyczny DNS dla kontenerów. Ponadto sonda jest wtedy odizolowana od sieci breach-net, w której znajduje się działający backend.

# 3. Trwałość danych

PS D:\Users\asass\Desktop\Programowanie - sem3\Laby - mw\breach-checker> docker exec backend sh -c "echo notatka > /tmp/notatka.txt"
PS D:\Users\asass\Desktop\Programowanie - sem3\Laby - mw\breach-checker> docker restart backend
backend
PS D:\Users\asass\Desktop\Programowanie - sem3\Laby - mw\breach-checker> docker exec backend cat /tmp/notatka.txt
notatka
PS D:\Users\asass\Desktop\Programowanie - sem3\Laby - mw\breach-checker> docker rm -f backend
backend
PS D:\Users\asass\Desktop\Programowanie - sem3\Laby - mw\breach-checker> docker run -d --name backend --network breach-net -p 5000:5000 -v ./data/leaked-sha1.txt:/app/data/leaked-sha1.txt:ro breach-checker-backend:v1
c1d80b35baaa24d169948387a62a05b0159eb7c544867b4b19a9fa08e0a0a71b
PS D:\Users\asass\Desktop\Programowanie - sem3\Laby - mw\breach-checker> docker exec backend cat /tmp/notatka.txt
cat: /tmp/notatka.txt: No such file or directory

PS D:\Users\asass\Desktop\Programowanie - sem3\Laby - mw\breach-checker> docker run --rm -v breach-dane:/dane alpine sh -c "date >> /dane/historia.txt"
PS D:\Users\asass\Desktop\Programowanie - sem3\Laby - mw\breach-checker> docker run --rm -v breach-dane:/dane alpine sh -c "date >> /dane/historia.txt; cat /dane/historia.txt"
Thu Oct 29 20:08:22 UTC 2026
Thu Oct 29 20:08:27 UTC 2026
PS D:\Users\asass\Desktop\Programowanie - sem3\Laby - mw\breach-checker> docker volume ls
DRIVER    VOLUME NAME
local     095e16c3557cf5b5089e0c2c74924760e795aa18cb20ea88dabbfddf1074d3b4
local     72024943174c2e5d56a0051b017ecf17bb4e63089a8c1e9ac54977c9c0b6134a
local     breach-dane
local     put_mw_lab3_system_biblioteczny_pgdata
PS D:\Users\asass\Desktop\Programowanie - sem3\Laby - mw\breach-checker> docker volume rm breach-dane
breach-dane

Plik w /tmp przetrwał restart, ponieważ warstwa zapisywalna jest przypisana do konkretnego kontenera i istnieje tak długo, jak sam kontener. Po użyciu rm kontener został usunięty wraz ze swoją warstwą zapisywalną, więc plik zniknął.
Plik historia.txt przetrwał, ponieważ został zapisany na wolumenie, który jest zarządzany przez Dockera niezależnie od cyklu życia kontenerów.
Lista wycieków również przetrwałaby polecenie docker rm, ponieważ jest podłączona z systemu plików hosta za pomocą tzw. bind mounta, a usuwanie kontenera nie kasuje plików na naszym komputerze.