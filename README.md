# Discord troll bot

This bot will randomly troll users that connect to a channel by speaking out loud some sentences.

- A user connect to a channel
- The troll bot join the channel too
- The troll bot say something randomly to troll the user (from a list of sounds you provide)
- The bot disconnect from the channel


Script variable (to pass via environment)

| Name              | Required | Default | Comment                                                             |
|-------------------|----------|---------|---------------------------------------------------------------------|
| DISCORD_SERVER_ID | True     |         | The ID of the discord server to connect                             |
| DISCORD_BOT_ID    | True     |         | Id of the bot (client ID)                                           |
| DISCORD_TOKEN     | True     |         | Auth token of the bot                                               |
| CHANCE_TO_TROLL   | False    | 20      | Percentage of chance to troll a user that just connect to a channel |
| SOUND_PATH        | False    | sounds/ | Folder that contains sounds file to play to troll users             |

## Dev env installation

Clone the repo
```
git clone https://github.com/Sispheor/discord_troll_bot
```

```
pip install --no-cache-dir -r requirements.txt
```

System packages
```
apt install -y ffmpeg
```

Export all needed variables
```
export DISCORD_SERVER_ID=123456
export DISCORD_BOT_ID=45678
export DISCORD_TOKEN=7777777888888899999999
export CHANCE_TO_TROLL=20
export SOUND_PATH=/home/me/troll_sounds
```

Run the script
```
python discord_bot.py
```

## Prod installation with Docker

Compile Docker image
```
docker build -t discord-bot .
```

Run by passing configuration as environment. We also need to mount a volume that contains our sound files.
```
docker run -it --rm --name discord-bot \
-e "DISCORD_SERVER_ID=<id>" \
-e "DISCORD_BOT_ID=<id>" \
-e "DISCORD_TOKEN=<token>" \
-e "CHANCE_TO_TROLL=<integer>" \
-v <path_to_sounds>:/app/sounds \
discord-bot
```

E.g:
```
docker run -it --rm --name discord-bot \
-e "DISCORD_SERVER_ID=1234" \
-e "DISCORD_BOT_ID=4567" \
-e "DISCORD_TOKEN=secret_token" \
-e "CHANCE_TO_TROLL=30" \
-v /root/sounds:/app/sounds \
discord-bot
```

## Install systemd service

Copy following content into `/etc/systemd/system/docker-discord-bot.service`
```
[Unit]
Description=Docker discord troll bot
After=docker.service
Requires=docker.service

[Service]
TimeoutStartSec=0
Restart=always
ExecStartPre=-/usr/bin/docker stop discord-troll-bot
ExecStartPre=-/usr/bin/docker rm discord-troll-bot
ExecStart=/usr/bin/docker run --rm --name discord-troll-bot \
            -e "DISCORD_SERVER_ID=1234" \
            -e "DISCORD_BOT_ID=4567" \
            -e "DISCORD_TOKEN=secret_token" \
            -e "CHANCE_TO_TROLL=30" \
            -v /root/sounds:/app/sounds \
            discord-bot
ExecStop= /usr/bin/docker stop discord-troll-bot && /usr/bin/docker rm discord-troll-bot

[Install]
WantedBy=multi-user.target
```

Active the service
```
sudo systemctl daemon-reload
sudo systemctl enable docker-discord-bot
sudo systemctl start docker-discord-bot
```

## Generate sound file from Text To Speech engine

Sounds files can be generated via a Text To Speech(TTS) engine. 
You can use for example [http://www.fromtexttospeech.com/](http://www.fromtexttospeech.com/).

You can also use a local self hosted TTS engine like Svoxpico.

Install the library
```
sudo apt install libttspico-utils
```

Generate a sentence
```
pico2wave -l en-EN -w test.wav "hello princess!"
```

Test it
```
play test.wav
```

Place the generated file in your "sounds" folder.
