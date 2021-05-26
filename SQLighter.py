import sqlite3

class SQLighter:

    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def close(self):
        """ Закрываем текущее соединение с БД """
        self.connection.close()
      

#   Нахождение вопроса для бота по номеру вопроса
    def select_question_by_token_number(self, token, questnum):
        entities = (questnum, token)
        with self.connection:
            return self.cursor.execute('SELECT * FROM questions WHERE number_of_quest = ? AND token = ?', entities).fetchall()[0]

#   Подсчет количества вопросов в боте
    def select_question_by_token(self, token):
        """ Считаем количество строк """
        with self.connection:
            return  self.cursor.execute('SELECT quest FROM questions WHERE token = ?', (token,)).fetchall()

#   Подсчет количества вопросов в боте
    def count_question_by_token(self, token):
        """ Считаем количество строк """
        with self.connection:
            result =  self.cursor.execute('SELECT * FROM questions WHERE token = ?', (token,)).fetchall()
            return len(result)

    def insert_question(self, token, question, questionNumber):
        entities = (token, question, questionNumber)
        with self.connection:
            self.cursor.execute('INSERT INTO questions (token, quest, number_of_quest) VALUES (?, ?, ?)', entities)
            self.connection.commit()


#   Получение ответа по токену бота id пользователя и номеру вопроса
    def select_answer_by_token_userNumber_questionNumber(self, token, usernum, questnum):
        entities = (usernum, questnum, token)
        with self.connection:
            return self.cursor.execute('SELECT * FROM answers WHERE user_id = ? AND quest_id = ? AND token = ?', entities).fetchall()

#   Подсчет количества ответов пользователя
    def count_answer_by_token_userNumber(self, token,  usernum):
        """ Считаем количество строк """
        entities = (usernum, token)
        with self.connection:
            result =  self.cursor.execute('SELECT * FROM answers WHERE user_id = ? AND token = ?', entities).fetchall()
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


#   Возвращает комбинации Вопрос - Ответ
    def select_bot_answers(self, token):
        with self.connection:
            return self.cursor.execute('SELECT questions.quest, answers.answer FROM answers INNER JOIN questions ON answers.quest_id = questions.number_of_quest AND answers.token = questions.token AND questions.token = ?', (token,)).fetchall()



    def add_bot(self, token):
        with self.connection:
            self.cursor.execute('INSERT INTO bots (token) VALUES (?)', (token,))    
            self.connection.commit()

    def delete_bot(self, token):
        with self.connection:
            self.cursor.execute('DELETE FROM bots WHERE token = ?', (token,))
            self.cursor.execute('DELETE FROM questions WHERE token = ?', (token,))
            self.cursor.execute('DELETE FROM answers WHERE token = ?', (token,))
            self.connection.commit()

    def bot_on(self, token):
        with self.connection:
            self.cursor.execute('UPDATE bots SET status = 1 WHERE token = ?', (token,))
            self.connection.commit()

    def bot_off(self, token):
        with self.connection:
            self.cursor.execute('UPDATE bots SET status = 0 WHERE token = ?', (token,))
            self.connection.commit()

    def bot_status(self, token):
        with self.connection:
            return self.cursor.execute('SELECT status FROM bots WHERE token = ?', (token,)).fetchall()[0][0]

    def bot_list(self):
        with self.connection:
            return self.cursor.execute('SELECT * FROM bots').fetchall()