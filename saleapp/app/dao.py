from sqlalchemy import text, func
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


def delete_patient(patient_id):
    patient = Patient.query.get(patient_id)
    return db.session.delete(patient)


def get_list_patient2(appointment_date):
    # target_date = datetime(2024, 12, 19).date()  # Ngày bạn muốn tìm kiếm

    target_date = datetime.strptime(appointment_date, '%Y-%m-%d').date()
    # return db.session.query(Product.id, Product.name, func.sum(ReceiptDetails.quantity * ReceiptDetails.unit_price)) \
    #     .join(ReceiptDetails, ReceiptDetails.product_id.__eq__(Product.id)).group_by(Product.id).all()
    print(target_date)
    dataTest = db.session.query(Patient.id,Patient.name, Patient.sex, Patient.birthday, Patient.address)\
                .join(ExaminationSchedule, ExaminationSchedule.patient_id==User.id) \
                .group_by(Patient.id) \
                .filter(func.date(ExaminationSchedule.date_examination).__eq__(appointment_date)).all()



    print(dataTest)
    return dataTest


def create_appointment(date_examination, note, name, birth, phone, time,address):
    time_frame = TimeFrame.query.filter(TimeFrame.time == time).first()
    print(time_frame)
    time_frame_id = time_frame.id
    patient = Patient(name,phone,birthday=birth, address=address, avatar=None)
    db.session.add(patient)
    db.session.commit()


    u = ExaminationSchedule(note=note,time_frame_id=time_frame_id,patient_id=patient.id, date_examination = date_examination,examination_list_id=None)
    db.session.add(u)
    db.session.commit()
    return True

if __name__ == '__main__':
    with app.app_context():
        print(get_list_patient2('2024-12-12'))

