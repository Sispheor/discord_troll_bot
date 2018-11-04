# BUILD
# docker build -t discord-bot .
# RUN
#docker run -it --rm --name discord-bot \
#-e "DISCORD_SERVER_ID=1234" \
#-e "DISCORD_BOT_ID=4567" \
#-e "DISCORD_TOKEN=secret_token" \
#-e "CHANCE_TO_TROLL=30" \
#-v /root/sounds:/app/sounds \
#discord-bot


FROM python:3.6

RUN apt-get update && apt install -y ffmpeg
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r /app/requirements.txt

CMD [ "python", "./discord_bot.py" ]
