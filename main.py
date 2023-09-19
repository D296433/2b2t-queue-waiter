from javascript import require, On
import time
import os
from plyer import notification
mfly = require('mineflayer')
with open("data/oldPosition.txt", "w", encoding="UTF-8") as f:
    f.write("0")
with open("data/pass10.txt", "w", encoding="UTF-8") as f:
    f.write("99999")

def notif(msg):
    notification.notify(
        title = '2b2t queuer',
        message = msg,
        app_icon = "2b2t.ico",
        timeout = 10,
    )

print("Fetching user information...")
with open("data/cfg.txt", "r", encoding="UTF-8") as f:
    cfg = f.read().split("\n")
if len(cfg) != 5:
    print("Invalid user information.")
    time.sleep(5)
    exit()
print("Attempting to connect to 2b2t.org...")
bot = mfly.createBot({
    'host': cfg[0],
    'port': cfg[1],
    'username': cfg[2],
    'auth': cfg[3],
    'version': cfg[4]
})

@On(bot, "spawn")
def spawn(*args):
    print("Connected to 2b2t.org!")
    notif("Connected to 2b2t.org!")

@On(bot, "messagestr")
def chat(msg, positionReg, *args):
    position = None
    for line in positionReg.split("\n"):
        if line.startswith("Position "):
            words = line.split(" ")
            position = words[3]
            break
    if position:
        with open("data/oldPosition.txt", "r", encoding="UTF-8") as f:
            oldPosition = f.read()
        if oldPosition != position:
            print(f"Position: {position}")
            with open("data/oldPosition.txt", "w", encoding="UTF-8") as f:
                f.write(position)
            with open("data/pass10.txt", "r", encoding="UTF-8") as f:
                pass10 = int(f.read())
            if int(position) <= 10:
                msg = f"Position: {position}"
                notif(msg)
            elif pass10 - int(position) >= 10:
                with open("data/pass10.txt", "w", encoding="UTF-8") as f:
                    f.write(position)
                msg = f"Position: {position}"
                notif(msg)

@On(bot, "kicked")
def kicked(reason, loggedIn, *args):
    print(f"Kicked: {reason}")
    notif(f"Kicked: {reason}")
    if loggedIn:
        print("Attempting to reconnect...")
        notif("Attempting to reconnect...")
        bot.connect()

@On(bot, "end")
def end(*args):
    print("Disconnected from 2b2t.org!")
    notif("Disconnected from 2b2t.org!")
    print("Attempting to reconnect...")
    notif("Attempting to reconnect...")
    bot.connect()

@On(bot, "error")
def error(err, *args):
    print(f"Error: {err}")
    notif(f"Error: {err}")