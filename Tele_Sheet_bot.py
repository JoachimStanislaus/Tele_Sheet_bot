from oauth2client.service_account import ServiceAccountCredentials
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
import gspread
import json
import telebot
from datetime import datetime
bot = telebot.TeleBot('your telebot token from the botfather ')
TelegramUsers = ["your telegram userid in integers "]

record_dict = {}
months_dict = {"01": "Jan", "02": "Feb", "03": "Mar", "04": "Apr", "05": "May", "06": "Jun", "07": "Jul", "08": "Aug", "09": "Sept", "10": "Oct", "11": "Nov", "12": "Dec"}

#Google Sheet Authentication
scopes = [
'https://www.googleapis.com/auth/spreadsheets',
'https://www.googleapis.com/auth/drive'
]
credentials = ServiceAccountCredentials.from_json_keyfile_name("The name of the json key you downloaded earlier.json", scopes) #access the json key you downloaded earlier 
file = gspread.authorize(credentials) # authenticate the JSON key with gspread
sheet = file.open('Name of your spreadsheet') # get the instance of the Spreadsheet


#Get today's date in integer format
def today_date():
    # Creating a datetime object so we can test.
    a = datetime.now()
    # Converting a to string in the desired format (YYYYMMDD) using strftime
    # and then to int.
    a = str(a.strftime('%d/%m/%y'))
    return a

#Checks if User is Authorized or not
def UserCheck(message):
    if message.from_user.id in TelegramUsers:    
        return True
    else:
        bot.reply_to(message, "Unauthorized User")
        print(message.from_user.id)
        return False

#determine if money in or out
def get_inout(message):
    inout = message.text
    print("In or Out: ",inout)
    record_dict["in or out"] = inout

    if inout.lower() == 'out':
        start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        start_markup.row('Food', 'Living Essentials', 'Health/Medical')
        start_markup.row('Groceries', 'Transportation', 'Personal' , 'Toiletries')
        start_markup.row('Entertainment/Social', 'Utilities', 'Travel', 'Gifts')
        sent = bot.send_message(message.chat.id, "Choose a category", reply_markup=start_markup)
        print(message.text)
        bot.register_next_step_handler(sent,get_category)
    elif inout.lower() == 'in':
        start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        start_markup.row('Salary', 'Reimbursement', 'Refund')
        start_markup.row('Parents', 'Gifts', 'Topup')
        sent = bot.send_message(message.chat.id, "Choose a category", reply_markup=start_markup)
        print(message.text)
        bot.register_next_step_handler(sent,get_category)


#get category data    
def get_category(message):
    category = message.text
    print("Category: ",category)
    record_dict["Category"] = category

    start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    start_markup.row('Today')
    sent = bot.send_message(message.chat.id, "Date? (in dd/mm/yy)", reply_markup=start_markup)
    bot.register_next_step_handler(sent,get_date)

#get date data
def get_date(message):
    if message.text == 'Today':
        datee = today_date()
        record_dict["Date"] = datee
    else:
        datee = message.text
        record_dict["Date"] = datee
    print("Date: ",datee)
    sent = bot.send_message(message.chat.id,"Amount?")
    bot.register_next_step_handler(sent,get_amt)

def get_amt(message):
    amt = message.text
    record_dict["Amount"]=amt
    print(amt)
    sent = bot.send_message(message.chat.id,"Description?")
    bot.register_next_step_handler(sent,get_description)

def get_description(message):
    desc = message.text
    record_dict["Description"]=desc
    print(desc)
    print(record_dict)
    bot.send_message(message.chat.id,"Updating...")
    update_sheet(message)

#Convert Date from dictionary to month as a string
def month_check():
    x = list(record_dict["Date"])
    x = x[-5:-3]
    y = ''.join(x)
    return y

#Function to upload data to google sheets
def upload_data(worksheet,cell):
        cell_row = cell.row + 1
        cell_col = cell.col
        cell_val = worksheet.cell(cell_row, cell_col).value
        print(cell_val)
        while cell_val is not None:
            cell_row = cell_row + 1
            print(cell_row)
            cell_val = worksheet.cell(cell_row, cell_col).value
        print("Row {} is None".format(cell_row))
        worksheet.update_cell(cell_row, cell_col, record_dict['Category'])
        worksheet.update_cell(cell_row,cell_col-1,record_dict['Description'])
        worksheet.update_cell(cell_row,cell_col-2,record_dict['Amount'])
        worksheet.update_cell(cell_row,cell_col-3,record_dict['Date'])

@bot.message_handler(commands=['test'])
def testtest():
    x = list(record_dict["Date"])
    x = x[-5:-3]
    y = ''.join(x)
    return y
    

def update_sheet(message):
    if (record_dict["in or out"]) == "Out":
        worksheet = sheet.worksheet("Transactions") # get Transactions worksheet of the Spreadsheet
        cell = worksheet.find("Category out")
        upload_data(worksheet,cell)
        mthcheck = month_check()
        for x in months_dict:
            if x == mthcheck:
                print(months_dict[x])
                worksheet = sheet.worksheet(months_dict[x])
                cell = worksheet.find("Category out")
                upload_data(worksheet,cell)
                print("Data Uploaded to {}".format(months_dict[x]))
                break
            else:
                continue
        bot.send_message(message.chat.id,"Updated")       
        
    elif (record_dict["in or out"]) == "In":
        worksheet = sheet.worksheet("Transactions") # get Transactions worksheet of the Spreadsheet
        cell = worksheet.find("Category in")
        upload_data(worksheet,cell)
        mthcheck = month_check()
        for x in months_dict:
            if x == mthcheck:
                print(months_dict[x])
                worksheet = sheet.worksheet(months_dict[x])
                cell = worksheet.find("Category in")
                upload_data(worksheet,cell)
                print("Data Uploaded to {}".format(months_dict[x]))
                break
            else:
                continue
        bot.send_message(message.chat.id,"Updated")
    

    print(record_dict)




# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    if UserCheck(message) == True:
            bot.send_message(message.chat.id, "Welcome {}\nUser: {}  ".format(message.from_user.first_name,message.from_user.id))
            bot.reply_to(message, "/start & /help to start and get commands\n/add to add record")
    else:
        pass

#Handle /add
@bot.message_handler(commands=['add'])
def add_record(message):
    if UserCheck(message) == True:
        start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        start_markup.row('In','Out')
        sent = bot.send_message(message.chat.id, "Money In or Out? ", reply_markup=start_markup)
        bot.register_next_step_handler(sent,get_inout)
    else:
        pass
    


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, "out of first loop")



print("I'm listening...")
bot.infinity_polling()