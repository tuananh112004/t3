from sqlalchemy import Column, String, Integer, Float, ForeignKey, Boolean, Enum
from sqlalchemy.dialects.mysql import DATETIME, DOUBLE
from sqlalchemy.orm import relationship
from enum import Enum as RoleEnum
from app import app, db
from flask_login  import UserMixin

# class Category(db.Model):
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String(50), nullable=False, unique=True)
#     products = relationship('Product', backref='category', lazy=True)
#
#
# class Product(db.Model):
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String(50), nullable=False)
#     price = Column(Float, default=0)
#     description = Column(String(255), nullable=True)
#     image = Column(String(100), nullable=True)
#     active = Column(Boolean, default=True)
#     category_id = Column(Integer, ForeignKey(Category.id), nullable=False)

class UserRole(RoleEnum):
    Admin = 1
    Cashier = 2
    Doctor = 3
    Nurse = 4
    Patient = 5

class User(db.Model, UserMixin):
    __tablename__ = "user"  # Bảng chung của lớp cha
    id = Column(Integer, primary_key = True, autoincrement = True)
    name = Column(String(50), nullable = True)
    sex = Column(String(50), nullable=True)
    birthday = Column(DATETIME, nullable=True)
    address = Column(String(150), nullable=True)
    username = Column(String(50), nullable = False, unique = True)
    password = Column(String(100), nullable = False)
    avatar = Column(String(150), default = "https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729533/zuur9gzztcekmyfenkfr.jpg")
    user_role = Column(Enum(UserRole), default = UserRole.Patient)
    type = Column(String(50))  # Trường này dùng để phân biệt lớp con
    __mapper_args__ = {
        "polymorphic_identity": "user",  # Định danh cho lớp cha
        "polymorphic_on": type , # Trường để phân biệt các lớp con
        "with_polymorphic": "*"  # Đảm bảo ánh xạ tất cả các lớp con
    }

    def __init__(self,name,sex,birthday,address,username,password,avatar):
        self.username = username
        self.password = password
        self.avatar = avatar
        self.address = address
        self.name = name
        self.sex = sex
        self.birthday = birthday





class Employee (User):
    __tablename__ = "employee"
    id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    salary = Column(String(50))
    # type = Column(String(50))  # Trường này dùng để phân biệt lớp con
    __mapper_args__ = {
        "polymorphic_identity": "employee",  # Định danh cho lớp Employee
        # "polymorphic_on": type  # Trường để phân biệt các lớp con
    }
    def __init__(self,name,sex,birthday,address,username,password,avatar,salary):
        super().__init__(name,sex,birthday,address,username,password,avatar)
        self.salary = salary

class Doctor(Employee):
    __tablename__ = "doctor"
    id = Column(Integer, ForeignKey("employee.id"), primary_key=True)
    specialist = Column(String(50))
    yearOfExperience = Column(Integer)
    __mapper_args__ = {
        "polymorphic_identity": "doctor",  # Định danh cho lớp Patient
    }
    def __init__(self, name, sex, birthday, address, username, password, avatar, specialist, yearOfExperience, salary):
        super().__init__(name, sex, birthday, address, username, password, avatar,salary)
        self.specialist = specialist
        self.yearOfExperience = yearOfExperience

class Nurse(Employee):
    __tablename__ = "nurse"  # Bảng chung của lớp cha
    id = Column(Integer, ForeignKey("employee.id"), primary_key=True)
    degree = Column(String(50))
    __mapper_args__ = {
        "polymorphic_identity": "nurse",  # Định danh cho lớp Patient
    }
    def __init__(self, name, sex, birthday, address, username, password, avatar,degree, salary):
        super().__init__(name, sex, birthday, address, username, password, avatar,salary)
        self.degree = degree


class Cashier(Employee):
    __tablename__ = "cashier"  # Bảng chung của lớp cha
    id = Column(Integer, ForeignKey("employee.id"), primary_key=True)
    skill = Column(String(50))
    __mapper_args__ = {
        "polymorphic_identity": "cashier",  # Định danh cho lớp Patient
    }

    def __init__(self, name, sex, birthday, address, username, password, avatar, skill, salary):
        super().__init__(name, sex, birthday, address, username, password, avatar,salary)
        self.skill = skill

class Administrator(Employee):
    __tablename__ = "administrator"  # Bảng chung của lớp cha
    id = Column(Integer, ForeignKey("employee.id"), primary_key=True)
    inauguration = Column(DATETIME)
    __mapper_args__ = {
        "polymorphic_identity": "administrator",  # Định danh cho lớp Patient
    }
    def __init__(self, name, sex, birthday, address, username, password, avatar, inauguration, salary):
        super().__init__(name, sex, birthday, address, username, password, avatar,salary)
        self.inauguration = inauguration

class Patient (User):
    __tablename__ = "patient"  # Bảng chung của lớp cha
    id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    insuranced = Column(String(50))
    __mapper_args__ = {
        "polymorphic_identity": "patient",  # Định danh cho lớp Patient
    }
    def __init__(self, name, sex, birthday, address, username, password, avatar, insuranced):
        super().__init__(name, sex, birthday, address, username, password, avatar)
        self.insuranced = insuranced


class Bill(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    medicineMoney = Column(Float, default=0)
    serviceFee = Column(Float, default=0)
    totalFee = Column(Float, default=0)
    examinationDate = Column(DATETIME)
    cashier_id = Column(Integer, ForeignKey(Cashier.id), nullable=False)
    patient_id = Column(Integer, ForeignKey(Patient.id), nullable=False)



class MedicineBill(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    diagnotic = Column(String(50))
    symptoms = Column(String(50))
    examinationDate = Column(DATETIME)
    doctor_id = Column(Integer, ForeignKey(Doctor.id), nullable=False)
    patient_id = Column(Integer, ForeignKey(Patient.id), nullable=False)
    bill_id = Column(Integer, ForeignKey(Bill.id), nullable=False)

class MedicineUnit(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    unit = Column(String(50))
    medicines = relationship('Medicine', backref='medicine_unit', lazy=True)

    def __str__(self):
        return self.unit
class Medicine(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    description = Column(String(50))
    price = Column(Float, default=0)
    amount = Column(Integer, default=0)
    unit_id = Column(Integer, ForeignKey(MedicineUnit.id), nullable=False)

    def __str__(self):
        return self.name
class Precription(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    amount = Column(Integer, default=0)
    note = Column(String(50))
    medicine_id = Column(Integer, ForeignKey(Medicine.id), nullable=False)
    medicineBill_id = Column(Integer, ForeignKey(MedicineBill.id), nullable=False)

class ExaminationList(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    examinationDate = Column(DATETIME)
    nurse_id = Column(Integer, ForeignKey(Nurse.id), nullable=False)
class ExaminationSchedule(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey(Patient.id), nullable=False)
    examination_list_id = Column(Integer, ForeignKey(ExaminationList.id), nullable=False)
    patient_id = Column(Integer, ForeignKey(Patient.id), nullable=False)



if __name__ == '__main__':
    with app.app_context():
        # db.create_all()
        import hashlib
        # d = Doctor(name='Doc',sex="female",birthday="2000-01-02",address="ABC",username='docA', password = str(hashlib.md5('123'.encode('utf-8')).hexdigest()),avatar="123",specialist = 'ABC',yearOfExperience = 3,salary='aksj')
        # db.session.add(d)
        # u = Patient(name='A',sex="female",birthday="2000-01-02",address="ABC",username='patientA', password = str(hashlib.md5('123'.encode('utf-8')).hexdigest()),avatar="123",insuranced="123")
        # db.session.add(u)
        a = Administrator(name='A', sex="female", birthday="2000-01-02", address="ABC", username='adminA',
                    password=str(hashlib.md5('123'.encode('utf-8')).hexdigest()), avatar="123", inauguration="2000-01-01",salary='Aks')
        db.session.add(a)
        # donViA = MedicineUnit('vien')
        # thuocA = Medicine('thuoc','abc',12,22,)

        db.session.commit()

        # c1 = Category(name='Mobile')
        # c2 = Category(name='Tablet')
        # c3 = Category(name='Laptop')
        # db.session.add_all([c1, c2, c3])
        # db.session.commit()
        # products = [
        #     {
        #         "name": "iPhone 7 Plus",
        #         "description": "Apple, 32GB, RAM: 3GB, iOS13",
        #         "price": 17000000,
        #         "image": "https://res.cloudinary.com/dxxwcby8l/image/upload/v1647056401/ipmsmnxjydrhpo21xrd8.jpg",
        #         "category_id": 1
        #     },
        #     {
        #         "name": "iPad Pro 2020",
        #         "description": "Apple, 128GB, RAM: 6GB",
        #         "price": 37000000,
        #         "image": "https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729533/zuur9gzztcekmyfenkfr.jpg",
        #         "category_id": 2
        #     },
        #     {
        #         "name": "Galaxy Note 10 Plus",
        #         "description": "Samsung, 64GB, RAML: 6GB",
        #         "price": 24000000,
        #         "image": "https://res.cloudinary.com/dxxwcby8l/image/upload/v1647248722/r8sjly3st7estapvj19u.jpg",
        #         "category_id": 1
        #     }, {
        #         "name": "iPhone 7 Plus",
        #         "description": "Apple, 32GB, RAM: 3GB, iOS13",
        #         "price": 17000000,
        #         "image": "https://res.cloudinary.com/dxxwcby8l/image/upload/v1647056401/ipmsmnxjydrhpo21xrd8.jpg",
        #         "category_id": 1
        #     },
        #     {
        #         "name": "iPad Pro 2020",
        #         "description": "Apple, 128GB, RAM: 6GB",
        #         "price": 37000000,
        #         "image": "https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729533/zuur9gzztcekmyfenkfr.jpg",
        #         "category_id": 2
        #     },
        #     {
        #         "name": "Galaxy Note 10 Plus",
        #         "description": "Samsung, 64GB, RAML: 6GB",
        #         "price": 24000000,
        #         "image": "https://res.cloudinary.com/dxxwcby8l/image/upload/v1647248722/r8sjly3st7estapvj19u.jpg",
        #         "category_id": 1
        #     }, {
        #         "name": "iPhone 7 Plus",
        #         "description": "Apple, 32GB, RAM: 3GB, iOS13",
        #         "price": 17000000,
        #         "image": "https://res.cloudinary.com/dxxwcby8l/image/upload/v1647056401/ipmsmnxjydrhpo21xrd8.jpg",
        #         "category_id": 1
        #     },
        #     {
        #         "name": "iPad Pro 2020",
        #         "description": "Apple, 128GB, RAM: 6GB",
        #         "price": 37000000,
        #         "image": "https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729533/zuur9gzztcekmyfenkfr.jpg",
        #         "category_id": 2
        #     },
        #     {
        #         "name": "Galaxy Note 10 Plus",
        #         "description": "Samsung, 64GB, RAML: 6GB",
        #         "price": 24000000,
        #         "image": "https://res.cloudinary.com/dxxwcby8l/image/upload/v1647248722/r8sjly3st7estapvj19u.jpg",
        #         "category_id": 1
        #     }, {
        #         "name": "iPhone 7 Plus",
        #         "description": "Apple, 32GB, RAM: 3GB, iOS13",
        #         "price": 17000000,
        #         "image": "https://res.cloudinary.com/dxxwcby8l/image/upload/v1647056401/ipmsmnxjydrhpo21xrd8.jpg",
        #         "category_id": 1
        #     },
        #     {
        #         "name": "iPad Pro 2020",
        #         "description": "Apple, 128GB, RAM: 6GB",
        #         "price": 37000000,
        #         "image": "https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729533/zuur9gzztcekmyfenkfr.jpg",
        #         "category_id": 2
        #     },
        #     {
        #         "name": "Galaxy Note 10 Plus",
        #         "description": "Samsung, 64GB, RAML: 6GB",
        #         "price": 24000000,
        #         "image": "https://res.cloudinary.com/dxxwcby8l/image/upload/v1647248722/r8sjly3st7estapvj19u.jpg",
        #         "category_id": 1
        #     }
        # ]
        # for p in products:
        #     prod = Product(**p)
        #     db.session.add(prod)
        # db.session.commit()