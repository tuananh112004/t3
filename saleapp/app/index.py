import math

from flask import render_template, request, redirect
import dao
from app import app, login
from flask_login import login_user, logout_user


@app.route("/", methods=['get', 'post'])
def index():
    if request.method.__eq__('POST'):

        return redirect('/')
    else:
        time_frames = dao.get_list_time_frame()
        return render_template('index.html',time_frames=time_frames)

   # return render_template('index.html', categories = cates, products = prods, page = math.ceil(total/page_size))

@app.route("/login", methods=['get', 'post'])
def login_procee():
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        u = dao.auth_user(username, password)
        if u:
            login_user(u)
            return redirect('/')



    return render_template('login.html')



@login.user_loader
def get_user(user_id):
    return dao.get_user_by_id(user_id)

@app.route("/logout")
def logout_procees():
    logout_user()
    return redirect('/login')



@app.route("/createList", methods =['get','post'])
def create_list_procee():
    if request.method.__eq__('POST'):
        appointment_date = request.form.get('appointment_date')

        record = dao.get_list_patient2(appointment_date)
        print(record)
        return render_template('list.html', records = record)

    return render_template('list.html')

@app.route("/abc", methods=['get', 'post'])
def medi():
    if request.method.__eq__('POST'):
        a = request.form.get('ids')
        print(a)
        return render_template('medicineb.html')
    return render_template('medicineb.html')



@app.route("/login-admin",methods=['post'])
def login_admin_procees():
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        u = dao.auth_user(username, password)
        if u:
            login_user(u)
            return redirect('/admin')
        return redirect('/admin')

if __name__ == '__main__':
    from app import admin
    app.run(debug=True)
