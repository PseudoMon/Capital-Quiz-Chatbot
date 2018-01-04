# Capital-Quiz-Chatbot
A "chatbot" for Line that asks you what's the capital of random countries. It makes use of Flask, Flask-SocketIO, Peewee, and, of course, LINE Messaging API for Python. You'd need to have those installed along with Python and access to Line's Developer console if you want to run it yourself.

This bot reads the countries'data from an SQlite database that you'll have to create first by running `schema.py`. The program is written to read from a specific data file (`countriescapitalnew.txt`). Though I'm sure that file is freely availbale, I don't remember where I got it. Sorry about that; I'd be grateful is someone can remind me where it came from. The database also contains other information not used by the bot (population, area, continent) which can be used to make the questions more complicated. 

There are two tables in the database: one for the countries data, and the other keeps a record of which games are going on. Each time a user "talks" to the bot, it'll check the user's id to reply correctly. 

To facilitate cities with alias or multiple names, the bot will only check if your guess is contained in the answer. I realise that's not a perfect solution (just "Fe" would be considered the capital of Colombia, even though the full answer in the databse is "Santa Fe de Bogota". On the other hand, "Bogota" will be considered correct, which is a good thing).

