from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.apps import apps
from django.urls import reverse
from datetime import date, datetime
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from .models import Employee
import customers

# Create your views here.


def get_day():
    day_of_week = datetime.now()
    return date.weekday(day_of_week)
    
@login_required
def index(request):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    logged_in_user = request.user
    try:
        logged_in_employee = Employee.objects.get(user = logged_in_user)
        Customer = apps.get_model('customers.Customer')
        today_date = date.today() #gets today's date
        day_index = get_day() #gets today's day
        weekday_name = days[day_index]

        local_customers = Customer.objects.filter(zip_code = logged_in_employee.zip_code)
        good_standing = local_customers.exclude(suspend_end__gt = today_date, suspend_start__lt = today_date) 
        pick_up = good_standing.exclude(date_of_last_pickup = today_date)
        needy_customers = pick_up.filter(weekly_pickup = weekday_name) | pick_up.filter(one_time_pickup = today_date)
        
        context = {
            'logged_in_employee' : logged_in_employee,
            'today_date' : today_date,
            'local_customers': local_customers,
            'good_standing' : good_standing,
            'pick_up' : pick_up,
            'needy_customers' : needy_customers
        }
        
        
        return render(request, 'employees/index.html', context)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('employees:create'))
    

@login_required
def create(request):
    logged_in_user = request.user
    if request.method == "POST":
        name_from_form = request.POST.get('name')
        zip_code = request.POST.get('zip_code')
        new_employee = Employee(name=name_from_form, user=logged_in_user, zip_code = zip_code)
        new_employee.save()
        return HttpResponseRedirect(reverse('employees:index'))
    else:
        return render(request, 'employees/create.html')

@login_required
def edit_profile(request):
    logged_in_user = request.user
    logged_in_employee = Employee.objects.get(user=logged_in_user)
    if request.method == "POST":
        name_from_form = request.POST.get('name')
        logged_in_employee.name = name_from_form
        logged_in_employee.zip_code = request.POST.get('zip_code')
        logged_in_employee.save()
        return HttpResponseRedirect(reverse('employees:index'))
    else:
        context = {
            'logged_in_employee': logged_in_employee
        }
        return render(request, 'employees/edit_profile.html', context)

@login_required
def daily_search(request):
    logged_in_user = request.user
    logged_in_employee = Employee.objects.get(user=logged_in_user)
    daily_list = customers.objects.filter(zip_code = logged_in_employee.zip_code)
    return daily_list


@login_required
def confirm_pickup(request, id):
    Customer = apps.get_model('customers.Customer')
    employee = request.user
    today_date = date.today()
    customer_today = Customer.objects.get(pk = id)
    
    try:
        customer_today.balance += 20
        customer_today.date_of_last_pickup = today_date
        customer_today.save()

        context = {
            'employee' : employee,
            'today_date' : today_date,
            'customer_balance' : customer_today.balance,
            'customer_pickup' : customer_today.date_of_last_pickup
        }
        return render(request, 'employees/index.html', context)
    except:
        return HttpResponseRedirect(reverse('employees:create'))


def daily_filter(request):
    
    try:
        logged_in_user = request.user
        logged_in_employee = Employee.objects.get(user = logged_in_user)
        Customer = apps.get_model('customers.Customer')
        local_customers = Customer.objects.filter(zip_code = logged_in_employee.zip_code)
        pick_up_day = local_customers.filter(weekly_pickup = selected_day ) 

        context = {
            'pick_up_day' : pick_up_day,
            'logged_in_user' : logged_in_user,
            'logged_in_employee' : logged_in_employee,
            'local_customers' : local_customers
        }

        return render (request, 'employees/daily_filter.html', context)
    except:
        return HttpResponseRedirect(reverse('employees:daily_filter'))
    
    
    

    
