from django.shortcuts import render, redirect, get_object_or_404
from calorie_counter_app.models import *
from calorie_counter_app.forms import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.contrib import messages


def login_view(request):
    form_data= AuthenticationForm()
    if request.method=="POST":
        form_data= AuthenticationForm(request, data= request.POST)
        if form_data.is_valid():
            user= form_data.get_user()
            if user:
                login(request, user)
                return redirect('dashboard_view')

    context={
        'form_title': 'User Login Page',
        'form_btn': 'Login',
        'title': 'Login',
        'form_data': form_data
    }
    return render(request, 'master/base_form.html', context)

def register_view(request):
    form_data= RegistrationForm()
    if request.method=='POST':
        form_data= RegistrationForm(request.POST)
        if form_data.is_valid():
            form_data.save()
            return redirect('login_view')
    context= {
        'form_title': 'User Registration Page',
        'form_btn': 'Register',
        'title': 'Register',
        'form_data': form_data, 
    }
    return render(request, 'master/base_form.html', context)
# Create your views here.
@login_required
def dashboard_view(request):
   
    try:
       
        bmr= request.user.user_profile.bmr
        
    except:
      
        bmr= 0
        messages.warning(request, 'Please update your profile first.')
        return redirect('profile_update_view')
    data= ConsumeCalorieModel.objects.filter(user=request.user).aggregate(total_calorie= Sum('consumed_calorie'))
    print(data['total_calorie'])
    
    total_consumed_calorie= data['total_calorie'] or 0
    less_or_more_calorie= bmr - total_consumed_calorie
    if total_consumed_calorie > bmr:
        Feedback= 'You are having too much calorie than required.'
    else:
        Feedback= 'You are having less calorie than required.'
    context={
        'bmr': round(bmr, 2),
        'total_consumed_calorie': round(total_consumed_calorie, 2),
        'less_or_more_calorie': round(less_or_more_calorie, 2),
        'Feedback': Feedback,

    }
    
    return render(request, 'dashboard.html', context)


@login_required
def profile_page(request):
    return render(request, 'profile.html')
@login_required
def profile_update_view(request):
    current_user= request.user
    try:
        profile_data= current_user.user_profile
        print(profile_data)
    except:
        profile_data=None
    form_data= UpdateProfileForm(instance=profile_data)
    if request.method=='POST':
        form_data= UpdateProfileForm(request.POST, request.FILES, instance=profile_data)
        if form_data.is_valid():
            form_data= form_data.save(commit=False)
            form_data.user= current_user
            form_data.save()
            return redirect('profile_page')
    context= {
        'form_title': 'User Profile Update Page',
        'form_btn': 'Update',
        'title': 'Update Profile',
        'form_data': form_data, 
    }
    return render(request, 'master/base_form.html', context)

@login_required
def calorie_consumption_list(request):
    try:
           
        bmr= request.user.user_profile.bmr
            
    except:
          
        bmr= 0
        messages.warning(request, 'Please update your profile first.')
        return redirect('profile_update_view')
    consumed_calorie= ConsumeCalorieModel.objects.all()
    context={
        'consumed_calorie': consumed_calorie
    }
    return render(request, 'calorie_list.html', context)
@login_required
def add_consumed_calorie(request):
    form_data= ConsumeCalorieForm()

    if request.method=='POST':
        form_data= ConsumeCalorieForm(request.POST)
        if form_data.is_valid():
            form_data= form_data.save(commit=False)
            form_data.user= request.user
            form_data.save()
            return redirect('calorie_consumption_list')
    context= {
        'form_title': 'Add Calorie Consumption Data',
        'form_btn': 'Add Calorie',
        'title': 'Add calorie',
        'form_data': form_data, 
        }
    return render(request, 'master/base_form.html', context)
@login_required
def update_consumed_calorie(request, id):
    data= get_object_or_404(ConsumeCalorieModel, id=id)

    form_data= ConsumeCalorieForm(instance=data)

    if request.method=='POST':
        form_data= ConsumeCalorieForm(request.POST, instance=data)
        if form_data.is_valid():
            form_data= form_data.save(commit=False)
            form_data.user= request.user
            form_data.save()
            return redirect('calorie_consumption_list')
    context= {
        'form_title': 'Update Calorie Consumption Data',
        'form_btn': 'Update Calorie',
        'title': 'Update calorie',
        'form_data': form_data, 
        }
    return render(request, 'master/base_form.html', context)
@login_required
def delete_consumed_calorie(request, id):
    get_object_or_404(ConsumeCalorieModel, id=id).delete()
    return redirect('calorie_consumption_list')
@login_required
def logout_view(request):
    logout(request)
    return redirect('login_view')

