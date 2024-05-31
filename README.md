# activity_meetup_schedule_bot (НЕ МОЙ ПРОЕКТ, БЫЛ ИСПОЛЬЗОВАН В КАЧЕСТВЕ ПРИМЕРА РАБОТЫ)

## Настройка конфигурации

В файле config.yml необходимо указать:
1) bot_token - токен бота, который будет хостить данный сервис
2) tg_channel - канал, куда будет публиковаться опрос. 

## Изменение времени запуска

В файле app.py есть функция для запуска опроса в определенное время. 
P.S. опрос должен быть удален в течение 48 часов после публикации, необходимо учитывать это в расписании. 

```python
async def scheduler():
    # время по UTC 0 (Москва +3h)
    # Wednesday Poll (start, clearing)
    aioschedule.every().tuesday.at("07:00").do(start_poll_scheduled)
    aioschedule.every().thursday.at("06:30").do(delete_last_posts)
    # Sunday Poll (start, clearing)
    aioschedule.every().friday.at("08:00").do(start_poll_scheduled)
    aioschedule.every().sunday.at("07:30").do(delete_last_posts)

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(10)
```

[Инструкция](https://github.com/ibrb/python-aioschedule) как работать с расписанием. 

## Развертывание бота (нужен Docker)

1) Перенести все файлы из этой директории на сервер
2) Собрать докер образ
```bash
docker build -t bot .
```
3) Запустить докер образ
```bash
docker run -d --rm bot
```

### Полезные [команды](https://tproger.ru/translations/docker-instuction/) для докера
