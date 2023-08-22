from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record
from post_office import mail
import calendar as cal_module
from calendar import HTMLCalendar
from datetime import datetime

# Create your views here.
def home(request):
    records = Record.objects.all()
    # check to see if user is logged in
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        # authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have successfully logged in!")
            return redirect("home")
        else:
            messages.success(
                request, "There was an error logging in. Please try again."
            )
            return redirect("home")
    else:
        return render(request, "home.html", {'records': records})

def logout_user(request):
    logout(request)
    messages.success(request, "You have successfully logged out!")
    return redirect("home")

def register_user(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			# authenticate and login
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, "You have registered successfully! Welcome!")
			return redirect('home')
	else:
		form = SignUpForm()
		return render(request, 'register.html', {'form': form})

	return render(request, 'register.html', {'form': form})

def user_record(request, pk):
    if request.user.is_authenticated:
        # look up records
        user_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'user_record':user_record})
    else:
        messages.success(request, "You must be logged in to view that page.")
        return redirect('home')

def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Record deleted successfully!")
        return redirect('home')
    else:
        messages.success(request, "You must be logged in to do that.")
        return redirect('home')

def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request,'Record added successfully!')
                return redirect('home')
        return render(request, 'add_record.html', {'form': form})
    else: 
        messages.success(request, "You must be logged in to do that.")
        return redirect('home')

def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record updated successfully!")
            return redirect('home')
        return render(request, 'update_record.html', {'form': form})  
    else:
        messages.success(request, "You must be logged in to do that.")
        return redirect('home')

def calendar(request, year, month):
    # convert month from name to number
    month = month.capitalize()
    month_number = list(cal_module.month_name).index(month)
    month_number = int(month_number)
    
    # create calendar
    cal = HTMLCalendar().formatmonth(
        year,
        month_number
        )
    
    # get current date
    now = datetime.now()
    current_date = now.date()
    # format date
    formatted_date = current_date.strftime('%d %B %Y')
    
    # get current time
    current_time = now.strftime('%I:%M %p')
    
    return render(request, 'calendar.html', {
        "year": year,
        "month": month,
        "month_number": month_number,
        "cal": cal,
        "formatted_date": formatted_date,
        "current_time": current_time,
        })

# def send_email_view(request):
#     mail.send(
#         ['recipient@example.com'],
#         subject='My email',
#         message='Hi there!',
#         html_message='Hi <strong>there</strong>!',
#     )
#     return render(request, 'template.html', context)