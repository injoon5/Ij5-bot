from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def main():
    resres = "Your bot is alive!<br><a href=https://discord.com/api/oauth2/authorize?client_id=797712776012627988&permissions=268954704&scope=bot>Invite me to your server!</a>"
    # readline_all.py
   
    resres = resres + "<script src='https://cdn.jsdelivr.net/npm/@widgetbot/crate@3' async defer> new Crate({server: '809081372684714065', channel: '809085478582222949'})</script>"
    return resres
    
def run():
    app.run(host="0.0.0.0", port=8080)
    
def keep_alive():
    server = Thread(target=run)
    server.start()