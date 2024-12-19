from app.models import Doctor, Medicine, MedicineUnit, MedicineBill, Administrator
from flask_admin import Admin, BaseView, expose
from app import app, db
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user
from flask import redirect



class AdminView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and isinstance(current_user, Administrator)

# if isinstance(doctor1, Doctor):
#     print("doctor1 is an instance of Doctor")
# else:
#     print("doctor1 is not an instance of Doctor")
class DoctorView(AdminView):
    column_list = ['id','name','specialist']
    column_searchable_list = ['name']
    column_filters = ['name']
    column_editable_list = ['name']
    can_export = True

class MedicineView(AdminView):
    column_list = ['name','description']
class MedicineUnitView(AdminView):
    column_list = ['id','unit','medicines']
class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated


# class Statsview(BaseView):
#     @expose('/')
#     def index(self):
#
#         return self.render('admin/stats.html')
#     def is_accessible(self):
#         return current_user.is_authenticated

admin = Admin(app=app, name='eCommerce Admin', template_mode='bootstrap4')
admin.add_view(MedicineUnitView(MedicineUnit,db.session))
admin.add_view(MedicineView(Medicine,db.session))
admin.add_view(DoctorView(Doctor,db.session))

# admin.add_view(AdminView(User,db.session))
# admin.add_view(Statsview(name="Thong ke"))
admin.add_view(LogoutView(name="Logout"))