import math
from sqlalchemy import text, func
from flask import render_template, request, redirect, jsonify, send_file, g, session
from pyexpat.errors import messages
from app.models import Patient, User, TimeFrame, ExaminationList, TimeFrame, ExaminationSchedule, Account,MedicineBill, Medicine
import json
import dao

from app import app, login,db
from flask_login import login_user, logout_user
from datetime import datetime
import pandas as pd
from io import BytesIO
@app.route("/", methods=['get', 'post'])
def index():

    if request.method.__eq__('POST'):
        appointment_date = request.form.get('appointment_date')

        if (appointment_date):
            pass
        else:
            appointment_date = '2024-12-12'
        date_obj = datetime.strptime(appointment_date, '%Y-%m-%d')
        formatted_date = date_obj.strftime('%d-%m-%Y')
        count_schedule = dao.get_list_patient2(appointment_date)
        if(len(count_schedule) >=40):
            print(len(count_schedule))
            return jsonify({
                "status": 400,
                "messages": "Ngày này đã kín lịch"
                })
        print(len(count_schedule))
        name = request.form.get('name')
        sex = request.form.get('sex')
        birth = request.form.get('birth')
        address = request.form.get('address')
        time = request.form.get('time')
        note = request.form.get('note')
        date = request.form.get('date')
        a = dao.create_appointment(name = name, sex=sex, birth=birth, address=address, time = time, note = note,date_examination=date)
        return redirect(request.referrer or '/')
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
            print(u)
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
    appointment_date = request.form.get('appointment_date')

    if(appointment_date):
        pass
    else:
        appointment_date = '2024-12-12'
    date_obj = datetime.strptime(appointment_date, '%Y-%m-%d')
    formatted_date = date_obj.strftime('%d-%m-%Y')
    if request.method.__eq__('POST'):


        record = dao.get_list_patient2(appointment_date)
        print(record)
        return render_template('list.html', records = record,date=formatted_date)

    return render_template('list.html',date=formatted_date)

@app.route("/abc", methods=['get', 'post'])
def medi():
    if request.method.__eq__('POST'):
        a = request.form.get('ids')
        print(a)
        return render_template('medicineb.html')
    return render_template('medicineb.html')



@app.route('/api/patient/<patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    if patient_id:
        print(patient_id)
        dao.delete_patient(patient_id)
        return jsonify({"status": 200})
    print("Loi xoa")
    return jsonify({"statussss": 404})


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

@app.route("/api/timeframe", methods=['GET'])
def timeframe_procee():

    time_frames = dao.get_list_time_frame()
    data = []
    for time_frame in time_frames:
        data.append({'time': time_frame.time})

    print(time_frames)
    # Trả về dữ liệu dưới dạng JSON
    return jsonify(data)  # Đảm bảo trả về đối tượng jsonify để Flask trả về response JSON

@app.route("/export_excel")
def export_excel_procee():
    # [(2, 'aa', 'nam', datetime.datetime(2000, 2, 2, 0, 0), 'HCM'),
    #  (3, 'aa', 'nam', datetime.datetime(2000, 2, 2, 0, 0), 'HCM'),
    #  (4, 'aa', 'nam', datetime.datetime(2000, 2, 2, 0, 0), 'HCM'), (7, 'Nguyen Le Ngoc Anh', '0798536554', None, None)]
    data = [
        {'examination_id': 5, 'patient_name': 'aa', 'patient_id': 5, 'time': '3:00', 'examination_date': '2024-12-20'},
        {'examination_id': 5, 'patient_name': 'aa', 'patient_id': 5, 'time': '3:00', 'examination_date': '2024-12-20'}
    ]
    data2 = session.get('dataJson', None)
    print(data2)
    df = pd.DataFrame(data2)

    # Sử dụng BytesIO để lưu tạm file Excel trong bộ nhớ (không ghi vào disk)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Examination Data')

    # Đưa con trỏ về đầu file
    output.seek(0)

    # Gửi file Excel về phía người dùng
    return send_file(output, as_attachment=True, download_name="examination_data.xlsx",
                     mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")



@app.route("/taoDon/<patient_id>/<date>", methods=['GET','POST'])
def taoDon(patient_id,date):
    name = dao.get_patient_name_by_id(patient_id)
    print(name)
    if request.method.__eq__('POST'):

        ho_ten = request.form.get('name')

        trieu_chung = request.form.get('trieuChung')
        du_doan_benh = request.form.get('duDoanBenh')


        drug_data = request.form.get('drugCollector')
        ans = json.loads(drug_data)
        a = MedicineBill(diagnotic=trieu_chung, symptoms=du_doan_benh, examinationDate= datetime.now())
        pass
    return render_template('taoDon.html',name=name,date=date)








@app.route('/api/search-drugs', methods=['GET'])
def search_drugs():
    query = request.args.get('q',' ').strip()  # Lấy tham số `q` từ URL

    if not query:
        return jsonify([])  # Trả về danh sách rỗng nếu không có từ khóa tìm kiếm

    print(query)
    # results = db.session.query(Medicine.name).filter(Medicine.name.__eq__(query)).limit(4).all()
    results = db.session.query(Medicine.name).filter(func.lower(Medicine.name).like(f"%{query.lower()}%")).limit(4).all()
    results_list = [{'name': result[0]} for result in results]

    return jsonify(results_list)


@app.route("/listPatient",methods=['GET','POST'])
def get_list_patient_procees():
    appointment_date = request.form.get('appointment_date')
    # appointment_date = datetime.today().strftime('%Y-%m-%d')
    if(appointment_date):
        pass
    else:
        appointment_date = '2024-12-12'
    date_obj = datetime.strptime(appointment_date, '%Y-%m-%d')
    formatted_date = date_obj.strftime('%d-%m-%Y')
    if request.method.__eq__('POST'):


        record = dao.get_list_patient2(appointment_date)
        print(record)
        return render_template('patientList.html', records = record,date=formatted_date)

    return render_template('patientList.html',date=formatted_date)
if __name__ == '__main__':
    from app import admin
    app.run(debug=True)
