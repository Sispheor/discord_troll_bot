# Discord troll bot

## Features

### Troll a member on connect

This bot will randomly troll users that connect to a channel by speaking out loud some sentences.

- A user connect to a channel
- The troll bot join the channel too
- The troll bot say something randomly to troll the user (from a list of sounds you provide)
- The bot disconnect from the channel

### Display the master fapper

The master fapper is the player who spent the more time playing games. The bot tracks users activities and register them into the database. 
Every week the top players is displayed in a channel.
```
Master fapper of the week:  player-4 

Player      Hours
--------  -------
player-4    16
player-2    10
player-1    8
player-3    2
```

## Configuration

Script variable (to pass via environment)

| Name              | Required | Default | Comment                                                             |
|-------------------|----------|---------|---------------------------------------------------------------------|
| DISCORD_SERVER_ID | True     |         | The ID of the discord server to connect                             |
| DISCORD_BOT_ID    | True     |         | Id of the bot (client ID)                                           |
| DISCORD_TOKEN     | True     |         | Auth token of the bot                                               |

Check file `troll-bot_config.yml` for other settings

## Dev env installation

Clone the repo
```bash
git clone https://github.com/Sispheor/discord_troll_bot
```

Install python libs
```bash
pip install --no-cache-dir -r requirements.txt
```

System packages
```bash
apt install -y ffmpeg
```

Place secrets in `environments/bot.env`
```bash
DISCORD_SERVER_ID=123456
DISCORD_BOT_ID=45678
DISCORD_TOKEN=7777777888888899999999
```

Run the dev docker env
```bash
docker-compose up db phpmyadmin
```

Run the script
```bash
python discord_bot.py
```

## Prod installation with Docker

Place secrets in `environments/bot.env`
```bash
DISCORD_SERVER_ID=123456
DISCORD_BOT_ID=45678
DISCORD_TOKEN=7777777888888899999999
```

Run prod Docker compose file
```bash
docker-compose up db bot
```

## Generate sound file from Text To Speech engine

Sound files can be generated via a Text To Speech(TTS) engine. 
You can use for example [http://www.fromtexttospeech.com/](http://www.fromtexttospeech.com/).

You can also use a local self hosted TTS engine like Svoxpico.

Install the library
```bash
sudo apt install libttspico-utils
```

Generate a sentence
```bash
pico2wave -l en-EN -w test.wav "hello princess!"
```

Test it
```bash
play test.wav
```

Place the generated file in your "sounds" folder.
