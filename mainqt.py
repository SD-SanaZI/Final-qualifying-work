import sys

from PyQt5.QtWidgets import (QWidget, QLabel, QPushButton, QLineEdit, QGridLayout, 
                             QMessageBox, QApplication)

from telegram.ext import Updater

from PyQt5 import QtCore

from SQLighter import SQLighter

from BotDispatcher import BotDispatcher

class NewBotCreatorWindow(QWidget):
    #Конструктор    
    def __init__(self, root):
        super().__init__() 
        self.main = root
        self.positions = [0] * 2
        for i in range(len(self.positions)):
            self.positions[i] = [None] * 3           
        self.initUI()
        
    #Создание UI        
    def initUI(self):
        self.setGeometry(300, 300, 900, 600)
        self.setWindowTitle('New bot')   
        label1 = QLabel('Введите токен бота.')
        label1.setAlignment(QtCore.Qt.AlignCenter)
        self.positions[0][0] = label1
        label2 = QLabel('Введите вопрос №1')
        label2.setAlignment(QtCore.Qt.AlignCenter)
        self.positions[1][0] = label2
        button = QPushButton('Добавить вопрос')
        button.clicked.connect(self.addQuestionRow)
        self.positions[0][2] = button
        tokenEdit = QLineEdit()
        self.positions[0][1] = tokenEdit
        questionEdit = QLineEdit()
        self.positions[1][1] = questionEdit
        
        closeButton = QPushButton('Закрыть')
        closeButton.clicked.connect(self.close)
        
        saveButton = QPushButton('Сохранить')
        saveButton.clicked.connect(self.save)  

        self.positions.append([None, saveButton, closeButton])
        
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        
        
        self.markup()
                
        self.grid.setColumnStretch(self.grid.columnCount(),1)
        self.grid.setRowStretch(self.grid.rowCount (),1)

    #Сохраняет данные из полей и инициализирует создание нового бота
    def save(self):
        questions = []
        for i in range(1, len(self.positions)-1):
            if len(self.positions[i][1].text()) == 0:
                text = "Вопрос №" + str(i) + " пуст"
                QMessageBox.information(self, 'Ошибка', text)
                return 0
            questions.append(self.positions[i][1].text())
        try:
            up = Updater(self.positions[0][1].text())
        except Exception:
            QMessageBox.information(self, 'Ошибка', "Нерабочий токен")
            return 0
        self.main.addRow(self.positions[0][1].text(), questions)
        self.close()

    #Заново перестраевает Layout по разметке positions
    def markup(self):
        for i in range(len(self.positions)):
            for j in range(len(self.positions[0])):
                self.grid.addWidget(self.positions[i][j], i, j)        
    
    #Добавляет строку для ввода вопроса    
    def addQuestionRow(self):
        row = []
        questionNumber = 'Введите вопрос №' + str(len(self.positions)-1)
        row.append(QLabel(questionNumber))
        row.append(QLineEdit())
        row.append(None)
        lastRow = self.positions[len(self.positions)-1]
        self.positions[len(self.positions)-1] = row
                    
        self.positions.append(lastRow)
        self.grid.setRowStretch(self.grid.rowCount(),0)
    
        self.grid.addWidget(row[0], len(self.positions)-1, 0)
        self.grid.addWidget(row[1], len(self.positions)-1, 1)
        self.grid.addWidget(row[2], len(self.positions)-1, 2)
                    
        self.grid.setRowStretch(self.grid.rowCount(),1)
          
        self.markup()
        
class AnswerWindow(QWidget):
    #Конструктор
    def __init__(self, token, databaseName):
        super().__init__()
        self.token = token
        self.database = databaseName  #Название базы данных
        self.positions = []           #Разметка UI
        self.initUI()

    def markup(self):
        for i in range(len(self.positions)):
            for j in range(len(self.positions[0])):
                self.grid.addWidget(self.positions[i][j], i, j)
        
    def initUI(self):
        db_worker = SQLighter(self.database)        
        answerList = db_worker.select_bot_answers(self.token)
        questionList = db_worker.select_question_by_token(self.token)
        db_worker.close()        
        
        self.setGeometry(300, 300, 900, 600)
        self.setWindowTitle('Answers')
        
        answerList = sorted(answerList)
        
        for question in questionList:
            label1 = QLabel('Вопрос:')
            label2 = QLabel(question[0])
            self.positions.append([label1,label2])
            label1 = QLabel('Ответы:')
            self.positions.append([label1,None])
            for answer in answerList:
                if answer[0] == question[0]:
                    label2 = QLabel(answer[1])
                    self.positions.append([None,label2])
           
        #Создание Layout-разметки
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        
        self.markup()
         
        #Поправка отступов
        self.grid.setColumnStretch(self.grid.columnCount(),1)
        self.grid.setRowStretch(self.grid.rowCount (),1)       
                


class MainBotManagerWindow(QWidget):
    #Конструктор
    def __init__(self, databaseName):
        super().__init__()
        self.botDispetcher = 0        #Диспетчер ботов
        self.database = databaseName  #Название базы данных
        self.positions = []           #Разметка UI
        self.initUI()                 #

    #Создание UI
    def initUI(self):
        #Запуск диспетчера ботов
        self.botDispetcher = BotDispatcher(self.database)
        
        self.setGeometry(300, 300, 900, 600)
        self.setWindowTitle('Bot manager')

        #Создание Layout-разметки
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        
        self.positioning()
        #Заполнение Layout
        self.markup()

    def positioning(self):
        #Создание верхушки окна
        self.positions = []
        label1 = QLabel('Токены')
        label1.setAlignment(QtCore.Qt.AlignCenter)
        label2 = QLabel('Статус')
        label2.setAlignment(QtCore.Qt.AlignCenter)
        button = QPushButton('Добавить бота')      
        button.clicked.connect(self.addTokenRow)
        self.positions.append([label1,label2,button])
        
        #Добавление строк с ботами в разметку
        for i in range(self.botDispetcher.countBots()):
            row = []
            row.append(QPushButton(self.botDispetcher.botInfo(i)[0]))
            row[0].clicked.connect(self.answersToQuestions)
            row.append(QPushButton(str(self.botDispetcher.botInfo(i)[1])))
            row[1].clicked.connect(self.changeBotStatus)
            row.append(QPushButton('Удалить бота'))
            row[2].clicked.connect(self.deleteBot)
            self.positions.append(row)
        

    #Заново перестраевает Layout по разметке positions
    def markup(self):
        for i in range(len(self.positions)):
            for j in range(len(self.positions[0])):
                self.grid.addWidget(self.positions[i][j], i, j)
        #Поправка отступов
        self.grid.setColumnStretch(self.grid.columnCount(),1)
        self.grid.setRowStretch(self.grid.rowCount (),1)
                
    #Выводит окно с вопросами и ответами на них пользователей
    def answersToQuestions(self):
        token = self.sender().text()
        self.answerWindow = AnswerWindow(token, self.database)
        self.answerWindow.show()
    
        
    def changeBotStatus(self):
        sender = self.sender()
        for i in range(len(self.positions)):
            if self.positions[i][1] == sender:
                token = self.positions[i][0].text()
        self.botDispetcher.changeBotStatus(token)
        for row in self.positions:
            for widget in row:
                if widget != None:
                    widget.deleteLater()
        self.positions = []
        self.positioning()
        self.markup()        
        
    #Открывает окно создания нового бота
    def addTokenRow(self):
        self.newBot = NewBotCreatorWindow(self)
        self.newBot.show()

    #Добавляет нового бота        
    def addRow(self, token, questions): 
        db_worker = SQLighter(self.database)
        print("Added token: ", token)
        db_worker.add_bot(token)
        for i in range(len(questions)):
            print("Added question: ", questions[i], " in token: ", token)
            db_worker.insert_question(token,questions[i],i + 1)
        db_worker.close()
        self.botDispetcher.reload()
        for row in self.positions:
            for widget in row:
                if widget != None:
                    widget.deleteLater()
        
        self.positions = []
        self.positioning()
        self.markup()

        
    def deleteBot(self):
        sender = self.sender()
        for i in range(len(self.positions)):
            if self.positions[i][2] == sender:
                token = self.positions[i][0].text()
        db_worker = SQLighter(self.database)
        db_worker.delete_bot(token)
        db_worker.close()
        self.botDispetcher.reload()
        for row in self.positions:
            for widget in row:
                if widget != None:
                    widget.deleteLater()
        self.positions = []
        self.positioning()
        self.markup()

    def closeEvent(self, event):
        self.botDispetcher.stop()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainBotManagerWindow('database.db')
    ex.show()
    sys.exit(app.exec_())
