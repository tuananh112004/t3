from sqlalchemy import text
from app.models import Patient, User, TimeFrame, ExaminationList, TimeFrame,ExaminationSchedule
import hashlib
from app import app,db
from datetime import datetime
from flask_login  import logout_user

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
    password2 =  str(hashlib.md5('123'.encode('utf-8')).hexdigest())
    return User.query.filter(User.username.__eq__(username),
                             User.password.__eq__(password2)).first()
def get_user_by_id(id):
    return User.query.get(id)


def get_list_patient():
    return Patient.query.all()

def get_list_time_frame():
    return TimeFrame.query.all()

def get_list_patient2(appointment_date):
    target_date = datetime(2024, 12, 19).date()  # Ngày bạn muốn tìm kiếm

    # Truy vấn dữ liệu từ các bảng ExaminationSchedule, Patient, TimeFrame và ExaminationList
    examination_schedules = db.session.query(ExaminationSchedule, Patient, TimeFrame, ExaminationList). \
        join(Patient, Patient.id == ExaminationSchedule.patient_id). \
        join(TimeFrame, TimeFrame.id == ExaminationSchedule.time_frame_id). \
        join(ExaminationList, ExaminationList.id == ExaminationSchedule.examination_list_id). \
        filter(db.func.date(ExaminationSchedule.date_examination) == target_date).all()

    # Kiểm tra kết quả trả về
    if not examination_schedules:
        print("Không có dữ liệu cho ngày này")

    result_data = []
    for schedule, patient, time_frame, exam_list in examination_schedules:
        result_data.append({
            'examination_id': schedule.id,
            'patient_name': patient.name,  # Lấy tên bệnh nhân
            'patient_id': patient.id,
            'time': time_frame.time,  # Lấy khung giờ khám
            'examination_date': schedule.date_examination.strftime('%Y-%m-%d'),  # Ngày khám
            'nurse_id': exam_list.nurse_id,  # ID của y tá (nếu cần)
        })
    print(result_data)
    return result_data
