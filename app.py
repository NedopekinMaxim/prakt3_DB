import requests
from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)   # создаем приложение

conn = psycopg2.connect(database="service_db",  # подключение к бд
                        user="postgres",
                        password="",
                        host="localhost",
                        port="5432")

cursor = conn.cursor()  # добавляем курсор

@app.route('/login/', methods=['POST', 'GET'])  # декоратор
def login():

    if request.method == 'POST':    # исключение на проверку пост
        if request.form.get("login"):
            username = request.form.get('username')
            password = request.form.get('password')
            cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(username), str(password)))
            records = list(cursor.fetchall())

            if username and password and records:   # исключение на пустой ввод
                #рендер страницы аккаунта
                return render_template('account.html', full_name=records[0][1], log=username, pas=password)
        elif request.form.get("registration"):
            return redirect("/registration/")     # перенаправление на регистрацию
    return render_template('login.html')    # рендер страницы регистрация


@app.route('/registration/', methods=['POST', 'GET'])   # декоратор
def registration():

    if request.method == 'POST':    # проверка на пост
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')

        if str(name) and str(login) and str(password):  # проверка на исключения

            cursor.execute("SELECT * FROM service.users WHERE login=%s", (str(login),)) #обращение к бд
            records = cursor.fetchall()
            if records:
                return redirect("/registration/")
            else:
                cursor.execute('INSERT INTO service.users (full_name, login, password) VALUES (%s, %s, %s);', (str(name), str(login), str(password)))
                return redirect('/login/')

        conn.commit()   # внесение данных в бд

    return render_template('registration.html') # рендер регистрации