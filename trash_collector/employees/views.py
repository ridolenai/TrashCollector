from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.apps import apps
from django.urls import reverse
from datetime import date
from django.core.exceptions import ObjectDoesNotExist
from trash_collector.employees.models import Employee


# Create your views here.
@login_required
def index(request):
    # This line will get the Customer model from the other app, it can now be used to query the db for Customers
    # logged= apps.get_model('customers.Customer')
    # return render(request, 'employees/index.html')
    logged_in_user = request.user
    try:
        logged_in_employee = Employee.objects.get(user = logged_in_user)
        today = date.today()

        context = {
            'logged_in_employee':logged_in_employee,
            'today':today
        }
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('employee:create'))

@login_required
def create(request):
    logged_in_user = request.user
    if request.method == "POST":
        name_from_form = request.POST.get('name')
        address_from_form = request.POST.get('address')
        zip_from_form = request.POST.get('zip_code')
        weekly_from_form = request.POST.get('weekly_pickup')
        new_employee = Employee(name=name_from_form, user=logged_in_user, address=address_from_form, zip_code=zip_from_form, weekly_pickup=weekly_from_form)
        new_employee.save()
        return HttpResponseRedirect(reverse('customers:index'))
    else:
        return render(request, 'customers/create.html')

@login_required
def edit_profile(request):
    logged_in_user = request.user
    logged_in_employee = Employee.objects.get(user=logged_in_user)
    if request.method == "Post":
        name_from_form = request.POST.get('name')
        address_from_form = request.POST.get('address')
        zip_from_form = request.POST.get('zip_code')
        weekly_pickup_from_form = request.POST.get('weekly')
        logged_in_employee.name = name_from_form
        logged_in_employee.address = address_from_form
        logged_in_employee.zip_code = zip_from_form
        logged_in_employee.weekly_pickup = weekly_pickup_from_form
        logged_in_employee.save()
        return HttpResponseRedirect(reverse('employees:index'))
    else:
        context = {
            'logged_in_employee': logged_in_employee
        }
        return render(request, 'employees/edit_profile.html', context)

