Data: 11.13.2026
Wersja Trivy: 0.76.0

| Nazwa obrazu | Rozmiar | Liczba podatności wszystikich (HIGH / CRITICAL) | Liczba podatności z dostępną poprawką (HIGH / CRITICAL) |
| --- | --- | --- | --- |
| breach-checker-backend:dev | 55.6 MB | 49 / 0 | 2 / 0 |
| breach-checker-backend:prod | 52.1 MB | 49 / 0 | 2 / 0 |
| breach-checker-frontend:przed | 59.5 MB | 27 / 1 | 27 / 1 |
| breach-checker-frontend:prod | 26.4 MB | 3 / 0 | 3 / 0 |

W celu zmniejszenia powierzchni ataku wprowadzono multi-stage builds, co pozwoliło usunąć zbędne narzędzenia deweloperskie i biblioteki ze środowisk produkcyjnych. Dodatkowo wykorzystano flagę `-pull`, aby wymusić pobranie najnowszych wersji obrazów bazowych, posiadających aktualne łatki bezpieczeństwa. Podatności o status `unfixed` nie mogą zostać dziś naprawione, ponieważ zależą one od zewnętrznych pakietów systemowych lub bibiotek. Kolejny skan bezpieczeństwa zostanie przeprowadzony przy następnej aktualizacji zależności projektu lub po wydaniu nowych wersji obrazów bazowych.