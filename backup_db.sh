#!/bin/bash

docker exec -it  d685b7b86e71 mysqldump -uroot -pp@ssw0rd troll_bot > troll_bot_db.sql
