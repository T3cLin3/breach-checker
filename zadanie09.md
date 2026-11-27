# 1. Metryki usługi `log`

```text
log_attempts_total{found="true"} 3.0
log_attempts_total{found="false"} 3.0
```

```text
Dla "true": 3
Dla "false": 9
```

Etykietą licznika jest tylko `found`, ponieważ przekazywanie `hash_prefix` naruszałoby prywatność użytkowników poprzez ujawnianie fragmentów hashy ich haseł w systemie monitoringu. W Prometheusie każda unikalna kombinacja etykiet tworzy osobny szereg czasowy, więc dodanie tysięcy różnych prefiksów obciążyłoby pamięć i spowolniło bazę danych. Po wykonaniu polecenia `docker compose up -d --build log` stary kontener zostaje usunięty i zastąpiony nowym, co zeruje licznik (ponieważ biblioteka `prometheus-client` przechowuje jego stan wyłącznie w ulotnej pamięci RAM procesu aplikacji).