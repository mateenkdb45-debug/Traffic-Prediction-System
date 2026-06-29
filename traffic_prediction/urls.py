from django.contrib import admin
from django.urls import path
from admins import views as AdminViews
from users import views as UserViews
from Utility.train_model import training,train_vehicles_model
from Utility.predict import predict_vehicles

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', AdminViews.BasePage, name='base'),

    path('register', AdminViews.RegisterUserPage, name='register'),
    path('login', AdminViews.UserLoginPage, name='login'),
    path('adminlogin', AdminViews.AdminLoginPage, name='adminlogin'),

    path('userlist', AdminViews.ViewUserPage, name='userlist'),
    path('useravtivate/<int:pk>', AdminViews.UserActivateFunction, name='useractivate' ),
    path('userdeavtivate/<int:pk>', AdminViews.UserDeactivateFunction, name='userdeavtivate' ),
    path('user_edit/<int:pk>', AdminViews.user_edit, name='user_edit'),

    path('userhome', UserViews.UserHomePage, name='userhome'),
    path('task1', UserViews.Task1, name='task1'),
    path('task2', UserViews.Task2, name='task2'),
    path('task3', UserViews.Task3, name='task3'),

    path('training',training,name='training'),
    path('model',train_vehicles_model,name='model'),

    path('predict_vehicles',predict_vehicles,name='predict_vehicles'),
]
