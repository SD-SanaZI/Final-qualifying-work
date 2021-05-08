import telebot;
import shelve
import config
from SQLighter import SQLighter
import sqlite3
import asyncio
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

print("start bot#")

#Регистрация пользователя/начало опроса
def start(update, context):
    print("start", update.message.text)

    db_worker = SQLighter(config.database_name)    
    #Подсчитываем количество ответов пользователя    
    count = db_worker.count_quest_rows_user(context.bot.token, update.effective_chat.id)
    #Если пользователь не зарегестрирован
    if count == 0:
        print('new user ',context.bot.token)
        #Находим первый вопрос
        quest = db_worker.select_question(context.bot.token,count+1)
        context.bot.send_message(chat_id = update.effective_chat.id, text = 'Начало опроса. Первый вопрос: ' + quest[1]);
        #Регистрация в бд
        db_worker.insert_answer(context.bot.token, update.effective_chat.id, count, 'Registred')
    else:
        print('old user ',context.bot.token)
        context.bot.send_message(chat_id = update.effective_chat.id, text = 'Вы уже проходите опрос. Для прохождения заново, удалите данные с помощью /del.');
    db_worker.close()

#Удаление ответов пользователя            
def delete(update, context):
    print('delete ',context.bot.token)
    db_worker = SQLighter(config.database_name)    
    db_worker.delete_user(context.bot.token, update.effective_chat.id)
    context.bot.send_message(chat_id = update.effective_chat.id, text = 'Ответы удалены.');
    db_worker.close()

#Обработка ответов        
def next_mess(update, context):
    print("next_mess ",context.bot.token)
    db_worker = SQLighter(config.database_name)
    
    #Подсчитываем количество ответов пользователя    
    count = db_worker.count_quest_rows_user(context.bot.token, update.effective_chat.id)
    #Если пользователь не зарегестирирован
    if count == 0:
        print("new user",context.bot.token)
        context.bot.send_message(chat_id = update.effective_chat.id, text = 'Для прохождения опроса напишите /reg.');
    else:
        print('old user ',context.bot.token)
        #Подсчитываем количество вопросов в опросе
        all_quest = db_worker.count_quest_rows_bot(context.bot.token)
        #Запись ответа
        if count < all_quest+1:
            if db_worker.select_triple(context.bot.token, update.effective_chat.id, count):
                db_worker.delete_answer(context.bot.token, update.effective_chat.id, count)
            db_worker.insert_answer(context.bot.token, update.effective_chat.id, count, update.message.text)
        
        print("Вопрос №", count, " из ", all_quest)

        #Если опрос не окончен
        if count < all_quest:
            quest = db_worker.select_question(context.bot.token,count+1)
            print(quest)
            if quest:
                context.bot.send_message(chat_id = update.effective_chat.id, text = quest[1]);
        else:
            context.bot.send_message(chat_id = update.effective_chat.id, text = 'Опрос окончен.');
    db_worker.close()

def main():
    updater = []
    dp = []
    startHandler = CommandHandler('reg',start)
    delHandler = CommandHandler('del',delete)
    textHandler = MessageHandler(Filters.text ,next_mess)
    
    for token in config.tokens:
        up = Updater(token)
        updater.append(up)
        disp = up.dispatcher
        disp.add_handler(startHandler)  
        disp.add_handler(delHandler)  
        disp.add_handler(textHandler)        
        dp.append(disp)
        
    update_queue = []
    
    for up in updater:
        update_queue.append(up.start_polling(poll_interval=0.1, timeout=10))
    
    while True:
        try:
            text = input()
        except NameError:
            text = input()

        # Gracefully stop the event handler
        if text == 'stop':
            for up in updater:
                up.stop()
            break

        # else, put the text into the update queue to be handled by our handlers
        elif len(text) > 0:
            for up in update_queue:
                up.put(text)

if __name__ == '__main__':
    main()