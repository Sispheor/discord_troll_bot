# BUILD
# docker build -t discord-bot .
# RUN
#docker run -it --rm --name discord-bot \
#-e "DISCORD_SERVER_ID=1234" \
#-e "DISCORD_BOT_ID=4567" \
#-e "DISCORD_TOKEN=secret_token" \
#-v ${PWD}/troll-bot-config.yml:/app/troll-bot-config.yml \
#discord-bot


FROM python:3.8

RUN apt-get update && apt install -y ffmpeg
WORKDIR /app
ADD ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . /app

CMD [ "python", "-u", "./discord_bot.py" ]
