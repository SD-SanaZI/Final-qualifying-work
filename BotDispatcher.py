from SQLighter import SQLighter
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import handlers

#Класс бота
class Bot:
    #Конструктор
    def __init__(self, token, handlers, status):
        super().__init__()
        self.token = token
        self.status = None
        self.updater = Updater(token)
        self.dispatcher = self.updater.dispatcher
        for handler in handlers:
            self.dispatcher.add_handler(handler)
        self.status = status

    #Запуск бота        
    def polling(self):
        if self.status == 1:
            print("bot: ", self.token, " started")
            self.poll = self.updater.start_polling(poll_interval=0.1, timeout=10)

    #Возвращает состояние бота(Включен/выключен)        
    def getStatus(self):
        return self.status

    #Изменяет статус бота на противоположный    
    def changeStatus(self):
        if self.status == 0:
            self.status = 1
            self.polling()
        elif self.status == 1:
            self.stop()

    #Деструктор            
    def __del__(self):
        self.stop()

    #Останавливает бота
    def stop(self):
        if self.status != None:
            print("bot: ", self.token, " stoped")
            self.status = 0
            self.updater.stop()

    #Возвращает токен бота            
    def getToken(self):
        return self.token
        
#Диспетчер ботов
class BotDispatcher:
    #Конструктор
    def __init__(self, databaseName):
        super().__init__()
        self.databaseName = databaseName
        self.bots = []
        self.build()
        self.activation()

    #Создание ботов и заполнение ими деспетчера
    def build(self):
        print("build start")
        startHandler = CommandHandler('reg',handlers.start)
        delHandler = CommandHandler('del',handlers.delete)
        textHandler = MessageHandler(Filters.text ,handlers.next_mess)
        #Объеденяем в список
        handlerList = [startHandler, delHandler, textHandler]
        
        db_worker = SQLighter(self.databaseName)
        botList = db_worker.bot_list()
        db_worker.close()
        print(botList)
        for row in botList:
            try:
                self.bots.append(Bot(row[0], handlerList, row[1]))
            except:
                print("Token:", row[0], "unuseable")
                continue

    #Включение ботов    
    def activation(self):
        for bot in self.bots:
            bot.polling()

    #Возвращает информации бота по номеру
    def botInfo(self,botNumber):
        return (self.bots[botNumber].getToken(), self.bots[botNumber].getStatus())

    #Остановка всех ботов диспетчера        
    def stop(self):
        for bot in self.bots:
            bot.stop()
    
    def countBots(self):
        return len(self.bots)
    
    def getIndexByToken(self, token):
        for i in range(len(self.bots)):
            if self.bots[i].getToken() == token:
                return i
        return None

    def changeBotStatus(self, token):
        index = self.getIndexByToken(token)
        if index != None:
            self.bots[index].changeStatus()
            db_worker = SQLighter(self.databaseName)
            print(db_worker.bot_status(token))
            if db_worker.bot_status(token) == 1:
                print("bot off")
                db_worker.bot_off(token)
            else:
                print("bot on")
                db_worker.bot_on(token)
            db_worker.close()   
        
    def reload(self):
        print("Reload...")
        self.stop()
        print("List spase")
        self.bots = []
        print()
        self.build()
        self.activation()
                      