from sqlalchemy import text
from app.models import Patient, User, TimeFrame, ExaminationList, TimeFrame, ExaminationSchedule, Account, Nurse
import hashlib
from flask import Flask, g, render_template, session
from app import app,db
from datetime import datetime
from flask_login  import logout_user,current_user

from flask import render_template, request, redirect
# def load_categories():
#
#     return Category.query.order_by('id').all()
#
#
# def load_products(cate_id=None, kw = None, page =1):
#     query = Product.query
#     if kw:
#         query = query.filter(Product.name.contains(kw))
#     if cate_id:
#         query = query.filter(Product.category_id == cate_id)
#
#     page_size = app.config.get('PAGE_SIZE')
#     start = (page - 1) * page_size
#     query = query.slice(start, start+page_size)
#
#
#     return query.all()
# def count_products():
#     return Product.query.count()


def auth_user(username, password):
    # password2 =  str(hashlib.md5('123'.encode('utf-8')).hexdigest())
    return Account.query.filter(Account.username.__eq__(username),
                             Account.password.__eq__(password)).first()
def get_user_by_id(id):
    return Account.query.get(id)


def get_list_patient():
    return Patient.query.all()

def get_list_time_frame():
    return TimeFrame.query.all()

def get_nurse_by_current_id(id):
    return Nurse.query.filter(Nurse.account_id == id).first()
def get_list_patient2(appointment_date):
    # target_date = datetime(2024, 12, 19).date()  # Ngày bạn muốn tìm kiếm

    target_date = datetime.strptime(appointment_date, '%Y-%m-%d').date()
    # nurse_id = get_nurse_by_current_id(current_user.id)
    # e = ExaminationList(examinationDate = target_date,nurse_id = nurse_id.id)



    print(target_date)
    # Truy vấn dữ liệu từ các bảng ExaminationSchedule, Patient, TimeFrame và ExaminationList
    examination_schedules = db.session.query(ExaminationSchedule, Patient, TimeFrame). \
        join(Patient, Patient.id == ExaminationSchedule.patient_id). \
        join(TimeFrame, TimeFrame.id == ExaminationSchedule.time_frame_id). \
        filter(db.func.date(ExaminationSchedule.date_examination) == target_date).all()

    result_data = []
    print(examination_schedules)
    # Kiểm tra kết quả trả về
    if not examination_schedules:
        print("Không có dữ liệu cho ngày này")



    for schedule, patient, time_frame in examination_schedules:
        result_data.append({
            'examination_id': schedule.id,
            'patient_name': patient.name,  # Lấy tên bệnh nhân
            'patient_id': patient.id,
            'time': time_frame.time,  # Lấy khung giờ khám
            'examination_date': schedule.date_examination.strftime('%Y-%m-%d'),  # Ngày khám

        })
    print(result_data)
    g.result_data = []
    g.result_data = result_data
    print(g.result_data)
    # if hasattr(g, 'result_data'):
    #     return f"Result: {g.result_data}"
    # else:
    #     return "No result data found!"
    session['result_data'] = result_data
    return result_data

def create_appointment(date_examination, note, name, email, phone, time,address):
    time_frame = TimeFrame.query.filter(TimeFrame.time == time).first()
    print(time_frame)
    time_frame_id = time_frame.id
    patient = Patient(name,phone,birthday=None, address=address, avatar=None)
    db.session.add(patient)
    db.session.commit()


    u = ExaminationSchedule(note=note,time_frame_id=time_frame_id,patient_id=patient.id, date_examination = date_examination,examination_list_id=None)
    db.session.add(u)
    db.session.commit()
    return True

