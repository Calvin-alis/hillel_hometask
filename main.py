
import  os
import sqlite3
from utilits import generate_password as gp
from utilits import  open_file
from utilits import create_fake_email as cfe
from utilits import normalize_and_calculate as nac
from utilits import  spacemarin_count as spacemarin

# импорты для 3 домашки
from utilits import create_fake_name
from  utilits import  create_fake_phone
from utilits import check_name
from  utilits import check_number
from flask import Flask, request
from datetime import datetime



app = Flask(__name__)


@app.route('/hello/')
def hello_world():
    return 'Hello, World!'

@app.route('/test/')
def test_func() -> str:
    name = 'Alex'
    return name



@app.route('/generate-password/')
def generate_password():
    # validate password-len from client
    password_len = request.args.get('password-len')
    if not password_len:
        password_len = 10
    else:
        if password_len.isdigit():
            password_len = int(password_len)
            # 10 .. 100
        else:
            password_len = 10
            # return 'Invalid parameter password-len. Should be int.'

    password = gp(password_len)
    return f'{password}'




#декоратор для вывода зависимостей
#отдельно реализовал функция open_file
@app.route('/requirements/')
def requirements() -> str:
    files  = open_file('/Users/alksandr/first_in_class/homework_hillel/homework_second/requirments.txt')
    return f'{files}\n' if  len(files) > 0 else 'Empty file'



#функция генерация рандомного usera
@app.route('/generate-users/')
def generate_users():
    # через curl все выводит, но когда пытаешься ввести все вручную пишет ошибку и возращает сообщение
    try:
        count_of_gen_users = int(request.args.get('user-generate'))
    except:
        return  'Error type'
    if int(count_of_gen_users) > 0 and int(count_of_gen_users) < 1000:
        result = cfe(count_of_gen_users)
    elif int(count_of_gen_users) > 1000:
        result = cfe(999)
    elif int(count_of_gen_users) <= 0:
        result = cfe()
    else:
        return 'example@gmail.com'
    return  f'{result }\n'



#функция для подсчета среднего веса, роста
@app.route('/mean/')
def calculate_mean():
    path = nac('hw (2) (1).csv')
    return f'{path}\n'


#функция для подсчета количества космонавтов в космасе
@app.route('/space/')
def calculate_spacemen():
    return 'Космодесантников к космасе на данный момент: ' + str(int(spacemarin()))


#@app.route('/generate-password2/')
#def generate_password2():
#     import random
#     import string
#     choices = string.ascii_letters + string.digits + '#$%^'
#     result = ''
#     for _ in range(10):
#         result += random.choice(choices)
#    return f'{result}\n'




@app.route('/emails/create/')
def create_email():
    import  sqlite3
    con = sqlite3.connect('homework_three.db')
    # http://127.0.0.1:5000/emails/create/?contactName=Alex&Email=awdaw@mail.com
    contact_name = request.args['contactName']
    email_value = request.args['Email']

    cur = con.cursor()
    sql_query = f'''
        INSERT INTO emails (contactName, emailValue)
        VALUES ('{contact_name}', '{email_value}');
        '''
    cur.execute(sql_query)
    con.commit()
    con.close()
    return 'create_email'


@app.route('/emails/read/')
def update_email():
    import sqlite3
    con = sqlite3.connect('homework_three.db')
    cur = con.cursor()
    sql_query = f'''
        SELECT * FROM emails;
        '''
    cur.execute(sql_query)
    result = cur.fetchall()
    con.close()
    return str(result)



@app.route('/emails/update/')
def delete_email():
    import sqlite3
    contact_name = request.args['contactName']
    email_value = request.args['Email']

    con = sqlite3.connect('homework_three.db')
    cur = con.cursor()
    sql_query = f'''
        UPDATE emails
        SET contactName = '{contact_name}'
        WHERE emailValue = '{email_value}';
        '''
    cur.execute(sql_query)
    con.commit()
    con.close()
    return 'update_email'



# 3 - домашняя работа
# реализован CRUD - что является dll  в нашей работе
# добавил и усвовершенстовал таблицы
# сделал дополнительные проверки
@app.route('/phones/create/')
def create_phones():
    import sqlite3
    connect = sqlite3.connect('homework_three.db')
    #что б избежать ошибок делаем дефолт значение и таким образом страхуем себя от плохого запроса
    contact_name = request.args.get('contactName', default= create_fake_name())
    phone_value =  request.args.get('phoneValue', default= create_fake_phone())
    cur = connect.cursor()
    sql_query_param = f'''
        INSERT INTO phones (contactName, phoneValue)
        VALUES ('{check_name(contact_name)}',  '{check_number(phone_value)}');
    '''
    cur.execute(sql_query_param)
    connect.commit()
    connect.close()
    return 'create phones'

@app.route('/phones/read/')
def read_phones_info():
    conect = sqlite3.connect('homework_three.db')
    cur = conect.cursor()
    sql_params = '''
        SELECT * FROM phones
    '''
    cur.execute(sql_params)
    res = cur.fetchall()
    conect.close()
    return str(res)

@app.route('/phones/update/')
def update_info():
    connect = sqlite3.connect('homework_three.db')
    cur = connect.cursor()
    name = request.args['ContactName']
    phone_number = request.args['phoneNumber']
    sql_param = f'''
    UPDATE phones
    SET contactName = '{name}'
    WHERE phoneValue = '{phone_number}';
    '''
    cur.execute(sql_param)
    connect.commit()
    connect.close()
    return 'update_info'


# есть идея но пока нахожусь на стадии разработки инструмента для обновление каскадно все ключи
@app.route('/phones/update-key/')
def update_key():
    connect = sqlite3.connect('homework_three.db')
    cur = connect.cursor()
    sql_param = '''
        UPDATE  phones CASCADE
        SET ID  = REPLACE AUTOINCREMENT ;
    '''
    cur.execute(sql_param)
    connect.commit()
    connect.close()
    return 'update_key'

@app.route('/phones/delete/')
def delete_info():
    connect = sqlite3.connect('homework_three.db')
    cur = connect.cursor()
    name = request.args['ContactName']
    sql_query = f'''
        DELETE FROM phones 
        WHERE contactName = '{name}';
        '''
    cur.execute(sql_query)
    connect.commit()
    connect.close()
    return 'delete_phones'

if __name__ == '__main__':
    app.run(host='0.0.0.0')


"""
http://google.com:443/search/?name=hillel&city=Dnepr

1. Protocol
http:// - protocol (https)
ftp:// - file transfer protocol
smtp:// - simple mail transfer protocol
ws:// (wss)

2. Domain (IPv4, IPv6)
google.com, facebook.com, lms.hillel.com
developer.mozilla.org -> 99.86.4.33 (DNS)

0-255.0-255.0-255.0-255
192.172.0.1

# WRONG
192.172.0
192.172.0.1.2
256.192.1.1

localhost -> 127.0.0.1

3. Port
http - 80
https - 443
smtp - 22

5000+

0 - 65535

4. Path
/generate-password/ -> generate_password()
/search/ -> make_search()

5. Query parameters
? - sep
name=hillel&city=Dnepr - 
{'name': 'hillel', 'city': 'Dnepr'}
"""
