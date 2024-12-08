import math

from flask import render_template, request, redirect
import dao
from app import app, login
from flask_login import login_user, logout_user


@app.route("/")
def index():
    # cates = dao.load_categories()
    # cate_id = request.args.get('category_id')
    # page = request.args.get('page', 1)
    # prods = dao.load_products(cate_id = cate_id, page = (int)(page))
    # page_size = app.config.get('PAGE_SIZE',8)
    # total = dao.count_products()

    return render_template('index.html')
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



@app.route("/createList")
def create_list_procee():
    list_patient = dao.get_list_patient()
    return render_template('list.html', list_patient = list_patient)



    return render_template('login.html')

@app.route("/abc", methods=['get', 'post'])
def medi():
    if request.method.__eq__('POST'):
        a = request.form.get('ids')
        print(a)
        return render_template('medicineb.html')
    return render_template('medicineb.html')




if __name__ == '__main__':
    app.run(debug=True)
