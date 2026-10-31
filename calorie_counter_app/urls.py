from django.urls import path
from calorie_counter_app.views import *

urlpatterns = [
    path('', login_view, name='login_view'),
    path('register/', register_view, name='register_view'),
    path('dashboard/', dashboard_view, name='dashboard_view'),
    path('profile/', profile_page, name='profile_page'),
    path('update_profile/', profile_update_view, name='profile_update_view'),
    path('calorie_list/', calorie_consumption_list, name='calorie_consumption_list'),
    path('add_calorie/', add_consumed_calorie, name='add_consumed_calorie'),
    path('upadate_calorie/<int:id>/', update_consumed_calorie, name='update_consumed_calorie'),
    path('delete_calorie/<int:id>/', delete_consumed_calorie, name='delete_consumed_calorie'),
    path('logout/', logout_view, name='logout_view'),

]