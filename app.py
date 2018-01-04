from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage )
from linebot.models import TextSendMessage

from schema import db, Game, Country
import peewee, random

app = Flask(__name__)
linebotapi = LineBotApi(
    "0JYIPWREoo8d1jAEVUqfNV0pUiUJDDfyl++wPd1wtmcPsESCzIfyjNoCN/r+7TsaiqAXBtfbmKvvu+OpEY2yY8uIhcSV30qeipi++RW/XCaSeiN3mq1ZC4MNxnULnqJzYQmKtFtv7wu3B7mUQOd3SwdB04t89/1O/w1cDnyilFU")

handler = WebhookHandler('434b0c353d1b5632bc70b7ba5fa7c9a5')
    
@app.before_request
def before_request():
    db.connect()
        
@app.after_request
def after_request(response):
    db.close()
    return response
    
@app.route('/callback', methods=['POST'])
def callback():
    signature = request.headers['X-LINE-SIGNATURE']
    
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
        
    return 'OK'
    
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == "/new":
        newQuestion(event)
    
    elif event.message.text == "/giveup":
        try:
            player = Game.get(Game.source_id == event.source.user_id)
        except peewee.DoesNotExist:
            pass
        else:
            giveUp(event, player)
            
    elif event.message.text == "/help":
        script = "Type /new to get a new question. \nType /giveup if you don't know the answer and want to know it."
        
        linebotapi.reply_message(
            event.reply_token,
            TextSendMessage(text=script)
        )
       
    else:   
        try:
            player = Game.get(Game.source_id==event.source.user_id)
        except peewee.DoesNotExist:
            linebotapi.reply_message(
                event.reply_token,
                TextSendMessage(text="Type /new to get a new question! Type /help for more info!")
            )
        else:
            if event.message.text == "city":
                linebotapi.reply_message(
                    event.reply_token,
                    TextSendMessage(text="Nope!")
                )
            else:
                guessAnswer(event, player)
                #linebotapi.reply_message(
                #    event.reply_token,
                #    TextSendMessage(text=str(player.currentcountry.name))
                #)
        
def newQuestion(event):
    
    countries = Country.select()
    country = random.choice(list(countries))
    
    try:
        user = Game.get(Game.source_id==event.source.user_id)
    except peewee.DoesNotExist:
        user = Game(source_id=event.source.user_id, isgroup=False)
    
    user.currentcountry = country
    user.save()
        
    linebotapi.reply_message(
        event.reply_token, 
        TextSendMessage(text="What is the capital of {}?".format(user.currentcountry.name))
    )
    
    
def guessAnswer(event, player):
    country = player.currentcountry
    answer = country.capital
    guess = event.message.text
    
    if guess.lower() in answer.lower():
        linebotapi.reply_message(
            event.reply_token,
            TextSendMessage(text="You're right! The capital of {} is {}! \nType /new for a new question!".format(country.name, answer))
        )
    else:
        linebotapi.reply_message(
            event.reply_token,
            TextSendMessage(text="Nope!")
        )
    
    
def giveUp(event, player):
    
    country = player.currentcountry
    answer = country.capital
    
    linebotapi.reply_message(
        event.reply_token,
        TextSendMessage(text="The capital of {} is {}!".format(country.name, answer))
    )
    
    player.delete_instance()
    
"""The following was used back before I keep everything in database
def openCountry():
    cl = codecs.open('countriescapital.json', 'r')
    clist = json.loads(cl.read())
    cl.close()
    return clist
    
def randomCountry(countries):
    return random.choice(list(countries.keys()))
    
def openPlayers():
    print("Opening players")
    playersf = codecs.open('players.json', 'r')
    players = json.loads(playersf.read())
    playersf.close()
    return players
    
def savePlayers(players):
    print("Closing players")
    playersf = codecs.open('players.json', 'w')
    playersjson = json.dumps(players)
    playersf.write(playersjson)
    playersf.close()
"""
        
if __name__ == "__main__":
    app.run(debug=True)