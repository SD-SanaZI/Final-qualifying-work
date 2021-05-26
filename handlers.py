from SQLighter import SQLighter

def start(update, context):
    print("start", update.message.text)

    db_worker = SQLighter('database.db')    
    #Подсчитываем количество ответов пользователя    
    count = db_worker.count_answer_by_token_userNumber(context.bot.token, update.effective_chat.id)
    #Если пользователь не зарегестрирован
    if count == 0:
        print('new user ',context.bot.token)
        #Находим первый вопрос
        quest = db_worker.select_question_by_token_number(context.bot.token,count+1)
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
    db_worker = SQLighter('database.db')    
    db_worker.delete_user(context.bot.token, update.effective_chat.id)
    context.bot.send_message(chat_id = update.effective_chat.id, text = 'Ответы удалены.');
    db_worker.close()

#Обработка ответов        
def next_mess(update, context):
    print("next_mess ",context.bot.token)
    db_worker = SQLighter('database.db')
    
    #Подсчитываем количество ответов пользователя    
    count = db_worker.count_answer_by_token_userNumber(context.bot.token, update.effective_chat.id)
    #Если пользователь не зарегестирирован
    if count == 0:
        print("new user",context.bot.token)
        context.bot.send_message(chat_id = update.effective_chat.id, text = 'Для прохождения опроса напишите /reg.');
    else:
        print('old user ',context.bot.token)
        #Подсчитываем количество вопросов в опросе
        all_quest = db_worker.count_question_by_token(context.bot.token)
        #Запись ответа
        if count < all_quest+1:
            if db_worker.select_answer_by_token_userNumber_questionNumber(context.bot.token, update.effective_chat.id, count):
                db_worker.delete_answer(context.bot.token, update.effective_chat.id, count)
            db_worker.insert_answer(context.bot.token, update.effective_chat.id, count, update.message.text)
        
        print("Вопрос №", count, " из ", all_quest)

        #Если опрос не окончен
        if count < all_quest:
            quest = db_worker.select_question_by_token_number(context.bot.token,count+1)
            print(quest)
            if quest:
                context.bot.send_message(chat_id = update.effective_chat.id, text = quest[1]);
        else:
            context.bot.send_message(chat_id = update.effective_chat.id, text = 'Опрос окончен.');
    db_worker.close()