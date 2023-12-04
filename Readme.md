# ToBeDo: Telegram simple checklist bot

Want to use deployed version?

1) Create a new group (or channel) in telegram for your checklists and invite https://t.me/tobedo_bot there.
2) Make tobedo_bot a group admin so he can read the messages
3) The bot will automatically turn any messages into a checklist parsing line by line

# Deployment of own bot

1) Go to https://telegram.me/BotFather and add a new bot. Remember bot username, and API token
2) Deploy tobedo docker file to some server and pass environment variable TG_TOKEN returned by BotFather. Also mount /code/db.sqlite3 to some persistent storage

```sh
docker run -e TG_TOKEN=<your token> -v /volumes/tobedo/:/code/db/ devforth/tobedo
```

Compose example:

```yaml
version: '3.3' 

services:
  tobedo:
    image: devforth/tobedo
    environemnt:
      - TG_TOKEN=<your token>
    volumes:
      - /volumes/tobedo.sqlite3:/code/tobedo.sqlite3
```
