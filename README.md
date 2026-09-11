# BLOKKY MonoMarket feed

Тестовая версия формирует 20 позиций из текущего Rozetka XML Хорошоп.

## GitHub

1. Создать репозиторий и загрузить содержимое этой папки.
2. Settings → Secrets and variables → Actions → New repository secret.
3. Имя секрета: `SOURCE_FEED_URL`.
4. Значение: URL текущего Rozetka feed Хорошоп.
5. Actions → Update MonoMarket feed → Run workflow.
6. Settings → Pages → Deploy from a branch → `main` → `/docs`.
7. После публикации прайс будет доступен по адресу `https://USERNAME.github.io/REPOSITORY/mono.json`.

## Перед тестом MonoMarket

В прайсе используется локация `BLOKKY-MAIN`. Такая локация должна существовать в кабинете MonoMarket. Если у магазина уже есть другой ID локации, заменить `WAREHOUSE_ID` в workflow.

## После подтверждения MonoMarket

В `.github/workflows/update-feed.yml` заменить:

`LIMIT: "20"`

на:

`LIMIT: "0"`

После следующего запуска будет опубликован полный прайс.
