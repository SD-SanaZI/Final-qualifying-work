import sqlite3

class SQLighter:

    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def select_all(self):
        """ Получаем все строки """
        with self.connection:
            return self.cursor.execute('SELECT * FROM answers').fetchall()

#   Получение ответа по токену бота id пользователя и номеру вопроса
    def select_triple(self, token, usernum, questnum):
        entities = (usernum, questnum, token)
        with self.connection:
            return self.cursor.execute('SELECT * FROM answers WHERE user_id = ? AND quest_id = ? AND token = ?', entities).fetchall()

#   Нахождение вопроса для бота по номеру вопроса
    def select_question(self, token, questnum):
        entities = (questnum, token)
        with self.connection:
            return self.cursor.execute('SELECT * FROM questions WHERE number_of_quest = ? AND token = ?', entities).fetchall()[0]

#   Подсчет количества ответов пользователя
    def count_quest_rows_user(self, token,  usernum):
        """ Считаем количество строк """
        entities = (usernum, token)
        with self.connection:
            result =  self.cursor.execute('SELECT * FROM answers WHERE user_id = ? AND token = ?', entities).fetchall()
            return len(result)

#   Подсчет количества вопросов в боте
    def count_quest_rows_bot(self, token):
        """ Считаем количество строк """
        entities = (token)
        with self.connection:
            result =  self.cursor.execute('SELECT * FROM questions WHERE token = ?', (token,)).fetchall()
            return len(result)

#   Запись ответа
    def insert_answer(self, token, usernum, questnum,  textanswer):
        entities = (usernum, questnum, textanswer, token)
        with self.connection:
            self.cursor.execute('INSERT INTO answers (user_id, quest_id, answer, token) VALUES (?, ?, ?, ?)', entities)
            self.connection.commit()

#   Удаление ответа - по токену, id пользователя и номеру вопроса
    def delete_answer(self, token, usernum, questnum):
        entities = (usernum, questnum, token)
        with self.connection:
            self.cursor.execute('DELETE FROM answers WHERE user_id = ? AND quest_id = ? AND token = ?', entities)
            self.connection.commit()

#   Удаление всех ответов пользователя в конкретном боте
    def delete_user(self, token, usernum):
        entities = (usernum, token)
        with self.connection:
            self.cursor.execute('DELETE FROM answers WHERE user_id = ? AND token = ?', entities)
            self.connection.commit()
            
    def close(self):
        """ Закрываем текущее соединение с БД """
        self.connection.close()