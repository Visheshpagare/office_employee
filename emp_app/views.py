from django.shortcuts import render , HttpResponse, redirect
from .models import Employee , Role , Department 
from datetime import datetime
from django.db.models import Q
 

# Create your views here.

def index(request):
    return render(request, 'index.html')


def all_emp(request):
    emps = Employee.objects.all()
    context = {
        'emps': emps
    }
    print(context)
    return render(request, 'all_emp.html', context)

def add_emp(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        salary = int(request.POST.get('salary', 0))
        bonus = int(request.POST.get('bonus', 0))
        phone = int(request.POST.get('phone', 0))
        dept_id = int(request.POST.get('dept', 0))
        role_id = int(request.POST.get('role', 0))
        new_emp = Employee(
            first_name=first_name, 
            last_name=last_name, 
            salary=salary, 
            bonus=bonus, 
            phone=phone, 
            dept_id=dept_id, 
            role_id=role_id, 
            hire_date=datetime.now()
        )
        new_emp.save()
        return HttpResponse('Employee added succesfully !')
       
    elif request.method=='GET':
       return render(request, 'add_emp.html')
    else:
     return HttpResponse('An axception occured ! Employee has not been added')

def remove_emp(request, emp_id = None):
    if emp_id:
        try:
            emp_to_be_removed = Employee.objects.get(id=emp_id)
            emp_to_be_removed.delete()
            return redirect('all_emp') # Redirect to all_emp page after deletion
        except Employee.DoesNotExist:
            return HttpResponse("Employee does not exist", status=404)

    emps = Employee.objects.all()
    context = {
        'emps': emps
    }
    return render(request, 'remove_emp.html', context)

def filter_emp(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        dept_name = request.POST.get('dept') # Renamed to avoid conflict with potential Department object
        role_name = request.POST.get('role') # Renamed to avoid conflict with potential Role object
        emps = Employee.objects.all() # Start with all employees

        # Apply filters based on provided criteria
        if name:
            emps = emps.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))
        if dept_name:
            emps = emps.filter(dept__name__icontains=dept_name) 
        if role_name:
            emps = emps.filter(role__name__icontains=role_name)
        
        context = {
            'emps': emps
        }
        return render(request, 'all_emp.html', context)

    elif request.method == 'GET':
        return render(request, 'filter_emp.html')
    else:
        # Should not be reached, but good for completeness
        return HttpResponse('An unexpected error occurred!', status=400)