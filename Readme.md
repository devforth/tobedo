# ToBeDo: Telegram simple checklist bot

<a href="https://devforth.io"><img src="https://raw.githubusercontent.com/devforth/OnLogs/e97944fffc24fec0ce2347b205c9bda3be8de5c5/.assets/df_powered_by.svg" style="height:36px"/></a>


![Group 169](https://github.com/devforth/tobedo/assets/1838656/8828eb64-6a5a-43c9-bc4d-29e0b754ab34)

[How to use bot](https://devforth.io/blog/tobedo-simple-telegram-checklist-todo-bot/).

Want to use the deployed version?

1) Create a new group (or channel) in telegram for your checklists and invite https://t.me/tobedo_bot there.
2) Make tobedo_bot a group admin so he can read the messages
3) The bot will automatically turn any messages into a checklist, parsing line by line

# Deploy own instance of bot

If you want to extend functionality, you can fork this repo and redeploy the bot.

1) Go to https://telegram.me/BotFather and add a new bot. Remember bot username, and API token
2) Build tobedo Docker image, edit username/image name in publish_to_dockerhub.sh and run it.
3) Deploy tobedo docker file to some server and pass the environment variable TG_TOKEN returned by BotFather.


Simple Docker run example:

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
      - /volumes/tobedo/:/code/db/
```
