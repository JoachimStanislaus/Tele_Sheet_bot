# Tele_Sheet_bot

This Bot is written in Python with pyTelegramBotAPI.

An Example of the Google Sheet. You should follow this format for the code to work. Ideally just make a copy of this Google Sheet.
https://docs.google.com/spreadsheets/d/1mE0O-fxkrgoQ2FTlSNbO1CPgEU0-VWbdz9QOQKA1OmU/edit#gid=0

## Installation

First of all, you need to install the pyTelegramBotAPI.

```bash
sudo pip install pyTelegramBotAPI
```
oauth2client – to authorize with the Google Drive API using OAuth 2.0
gspread – to interact with Google Spreadsheets
```bash
pip install gspread oauth2client
```

Finally clone the repo
```bash
git clone https://github.com/JoachimStanislaus/Tele_Sheet_bot
```

After you clone, you need to add a few tokens.

This should be your Token received from Botfather.
```python
bot = telebot.TeleBot('your telebot token from the botfather ')
```
https://www.wikihow.com/Know-Chat-ID-on-Telegram-on-Android
```python
TelegramUsers = ["your telegram userid in integers "]
```
This guide will teach you how to get your json key and setup the gspread portion. https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html
```python
credentials = ServiceAccountCredentials.from_json_keyfile_name("The name of the json key you downloaded earlier.json", scopes) #access the json key you downloaded earlier 
```
Pretty Self explanatory... just change it to the name of your spreadsheet.
```python
sheet = file.open('Name of your spreadsheet') # get the instance of the Spreadsheet
```



## Usage

Once you're done setting it up and the bot is running.

Do /add to add and it will prompt you with several questions.



## Running the Bot
You can one-time run the Bot with the command

```Bash
python Tele_Sheet_bot.py
```
This isn't recommend. Use something like screen to hold the Bot. screen -S SheetBot Then just retype the command and you are finished!

## Contributing
please email me @ joachimtan00@gmail.com first to discuss what you would like to change.