import logging
from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from .models import Event,CustomUser,Category,Registration
from .forms import CustomUserCreationForm,EventForm,RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .decorators import role_required
from django.core.mail import send_mail



# Create your views here.

# -------------------
# User Registration View
# -------------------

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            messages.success(
                request,"Registration sucessful! Welcome."
            )
            return redirect("event_list")
        else:
            messages.error(
                request,"Registration failed. Please correct the errors below."
            )
    else:
        form = CustomUserCreationForm()

    return render(request,"event_app/register.html",{'form':form})

# -------------------
# User Login View
# -------------------

def user_login(request):
    
    if request.method == "POST":
        form = AuthenticationForm(
            request,data=request.POST
        )
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(
                request,username=username,password=password
            )

            if user is not None:
                login(request,user)
                messages.success(
                    request,f"Welcome back, {user.username}!"
                )
                return redirect("event_list")

            else:
                messages.error(
                    request,"Invalid username or password."
                )
        else:
            messages.error(
                request,form.non_field_errors()
            )
    else:
        form = AuthenticationForm()
    
    return render(request,"event_app/login.html",{"form":form})


# -------------------
# User Logout View
# -------------------

def logout_view(request):
    logout(request)
    messages.success(request,"You have been logged out.")
    return redirect("login")

# -------------------
# Event List View
# -------------------

@login_required
def event_list(request):

    if request.user.role == "manager":
        events = Event.objects.for_manager(request.user).select_related('category')
        # categories = Category.objects.filter(events__in=events).prefetch_related("events")
        categories = Category.objects.filter(events__in=events).distinct()

    else:
        events = Event.objects.all().select_related('category')
        # categories = Category.objects.all().prefetch_related("events")
        categories = Category.objects.all()
    return render(request,"event_app/event_list.html",{"events":events,"categories":categories})

# -------------------
# Event Create View
# -------------------
@role_required('manager')
@login_required
def event_create(request):
    if request.method == "POST":
        form = EventForm(request.POST,request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            form.save_m2m()
            
            # SEND CONFIRMATION EMAIL

            subject = "Event Registration Successful"
            message = f"""
            Hi {request.user.username},

            You have successfully created an event: {event.title}.
            """

            from_email = "sorathiyahemil2023@gmail.com"
            recipient_list = [request.user.email]

            send_mail(subject,message,from_email,recipient_list,fail_silently=False)

            messages.success(request,"Event created successfully!")
            return redirect("event_list")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
            messages.error(
                request,"Failed to create event.Please fix the errors below."
            )
    else:
        form = EventForm()

    return render(request,"event_app/event_form.html",{"form":form})


# -------------------
# Event Update View
# -------------------
@role_required('manager')
@login_required
def event_update(request,pk):
    event = get_object_or_404(Event,pk=pk)

    if request.method == "POST":
        form = EventForm(
            request.POST,request.FILES,instance=event
        )
        if form.is_valid():
            form.save()
            messages.success(request,"Event updated successfully!")
            return redirect("event_list")
        else:
            messages.error(
                request,"Failed to update event. Please fix the errros below."
            )
    else:
        form = EventForm(instance=event)
    
    return render(request,"event_app/event_form.html",{"form":form})

# -------------------
# Event Delete View
# -------------------
@role_required('manager')
@login_required
def event_delete(request,pk):
    event = get_object_or_404(Event,pk=pk)
    if request.method == "POST":
        event.delete()
        messages.success(request,"Event deleted successfully!")
        return redirect("event_list")
    
    return render(request,"event_app/event_confirm_delete.html",{"event":event})

# -------------------
# Event Detail View
# -------------------

@login_required
def event_details(request,pk):
    event = get_object_or_404(Event,id=pk)
    return render(request,"event_app/event_details.html",{"event":event})


# --------------------------
# Registration Create View
# --------------------------

@role_required('participant')
@login_required
def registration_create(request,event_id):

    event = get_object_or_404(Event, id=event_id)

    user_has_booked = Registration.objects.filter(event=event,user=request.user).exists()

    if user_has_booked:
        messages.error(request,"You have already booked this event.")
        return redirect("event_list")

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        form.instance.event = event
        if form.is_valid():
            registration = form.save(commit=False)
            registration.event = event
            registration.user = request.user
            registration.save()
            form.save_m2m()

            # SEND CONFIRMATION EMAIL

            subject = "Event Registration Successful"
            message = f"""
            Hi {request.user.username},

            You have successfully registered for the event: {event.title}.

            Event Details:
            - Start Date: {event.start_date}
            - End Date: {event.end_date}
            - Description: {event.description}

            Thank you for registration!
            """

            from_email = "sorathiyahemil2023@gmail.com"
            recipient_list = [request.user.email]

            send_mail(subject,message,from_email,recipient_list,fail_silently=False)

            messages.success(request,"Your booking was successful! Email has been sent successfully!")
            return redirect("registration_list")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
            messages.error(
                request,"Failed to Registration.Please fix the errors below."
            )
    else:
        form = RegistrationForm()

    return render(request,"event_app/registration_form.html",{"form":form,'event':event})

# --------------------------
# Registration Update View
# --------------------------

@role_required('participant')
@login_required
def registration_update(request,pk):
    registration = get_object_or_404(Registration,pk=pk)

    if request.method == "POST":
        form = RegistrationForm(
            request.POST,instance=registration
        )
        if form.is_valid():
            form.save()
            messages.success(request,"Registration updated successfully!")
            return redirect("registration_list")
        else:
            messages.error(
                request,"Failed to update Registration. Please fix the errros below."
            )
    else:
        form = RegistrationForm(instance=registration)
    
    return render(request,"event_app/Registration_form.html",{"form":form})

# --------------------------
# Registration Delete View
# --------------------------

@role_required('participant')
@login_required
def registration_delete(request,pk):
    registration = get_object_or_404(Registration,pk=pk)
    if request.method == "POST":
        registration.delete()
        messages.success(request,"Registration deleted successfully!")
        return redirect("registration_list")
    
    return render(request,"event_app/registration_confirm_delete.html",{"registration":registration})

# --------------------------
# Registration List
# --------------------------

@role_required('participant')
@login_required
def registration_list(request):
    registrations = Registration.objects.filter(user=request.user)
    return render(request,"event_app/registration_list.html",{"registrations":registrations})

# ------------------------
# Registration Detail View
# ------------------------

@login_required
def registration_details(request,pk):
    registration = get_object_or_404(Registration,id=pk)
    return render(request,"event_app/registration_details.html",{"registration":registration})

@role_required('manager')
@login_required
# ------------------------
# Registration Detail View
# ------------------------

def manager_dashboard(request):
    events = Event.objects.for_manager(request.user)

    registrations = Registration.objects.filter(event__in=events).select_related('user','event')

    return render(request,"event_app/dashboard.html",{"events":events,"registrations":registrations})