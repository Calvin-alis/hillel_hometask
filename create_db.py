import sqlite3
from utilits import create_fake_email
from utilits import  create_fake_name
from utilits import  create_fake_phone
con = sqlite3.connect('homework_three.db')

cur = con.cursor()
# 3 - домашка
#  усовершенстувует наши таблицы,  исполняем правило db = <S, Q,Z>
# теперь у нас будут уникальные ключи,  создаваться в случае пустоты пользователей с уникальным индефикатором
sql_query = f'''
    CREATE TABLE IF NOT EXISTS emails
    (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    contactName text NOT NULL DEFAULT  '{create_fake_name()}', 
    emailValue text NOT NULL DEFAULT  '{create_fake_email()}'
    );
'''
cur.execute(sql_query)
con.commit()

sql_query_phons = f'''
CREATE TABLE IF NOT EXISTS phones
    (
    ID INTEGER PRIMARY KEY AUTOINCREMENT, 
    contactName text NOT NULL DEFAULT  '{create_fake_name()}', 
    phoneValue text NOT NULL DEFAULT '{create_fake_phone()}'
    );
'''

cur.execute(sql_query_phons)
con.commit()

con.close()

