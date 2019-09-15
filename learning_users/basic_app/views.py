from django.conf import settings
from django.shortcuts import render
from basic_app.forms import UserForm,UserProfileInfoForm
from django.contrib.auth.models import User
from basic_app.models import UserProfileInfo,Log
from django.core.mail import send_mail
from django.template.loader import render_to_string
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas



# Extra Imports for the Login and Logout Capabilities
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    user_form = UserForm(data=request.POST)
    profile_form = UserProfileInfoForm(data=request.POST)
    return render(request,'basic_app/index.html',{'user_form':user_form,
                           'profile_form':profile_form,})

def coordinator(request):
    footfall = len(UserProfileInfo.objects.filter(cs=False))-2
    pp_l = len(UserProfileInfo.objects.filter(pp=True))
    bat_l = len(UserProfileInfo.objects.filter(bat=True))
    tq_l = len(UserProfileInfo.objects.filter(tq=True))
    ar_l = len(UserProfileInfo.objects.filter(ar=True))
    aio_l = len(UserProfileInfo.objects.filter(aio=True))
    ty_l = len(UserProfileInfo.objects.filter(ty=True))
    syt_l = len(UserProfileInfo.objects.filter(syt=True))
    mod_l = len(UserProfileInfo.objects.filter(mod=True))
    th_l = len(UserProfileInfo.objects.filter(th=True))
    pubg_l = len(UserProfileInfo.objects.filter(pubg=True))
    logleft = len(User.objects.filter(last_login=None))
    left = len(UserProfileInfo.objects.filter(cs=False,pp=False,bat=False,tq=False,ar=False,aio=False,ty=False,syt=False,mod=False,th=False,pubg=False)) - 2
    return render(request, 'basic_app/coordinator.html',{'footfall':footfall ,'pp_l':pp_l,'bat_l':bat_l,'tq_l':tq_l,'ar_l':ar_l,'aio_l':aio_l,'ty_l':ty_l,'syt_l':syt_l,'mod_l':mod_l,'th_l':th_l,'pubg_l':pubg_l,'left':left,'logleft':logleft})

@login_required
def special(request):
    # Remember to also set login url in settings.py!
    # LOGIN_URL = '/basic_app/user_login/'
    return HttpResponse("You are logged in. Nice!")

@login_required
def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return HttpResponseRedirect(reverse('index'))

def register(request):

    registered = False

    if request.method == 'POST':

        # Get info from "both" forms
        # It appears as one form to the user on the .html page
        user_form = UserForm(data=request.POST )
        profile_form = UserProfileInfoForm(data=request.POST)

        # Check to see both forms are valid
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            profile = profile_form.save(commit=False)
            
            if User.objects.filter(email=user.email).exists() or UserProfileInfo.objects.filter(mob_no=profile.mob_no) or UserProfileInfo.objects.filter(college_reg_id=profile.college_reg_id):
                print("Exixt")
            else:    
                # Save User Form to Database
                user = user_form.save()

                # Hash the password
                user.set_password(user.password)
                codeg=1110+user.id
                user.username='P19'+str(codeg)

                # Update with Hashed password
                user.save()

                # Now we deal with the extra info!

                # Can't commit yet because we still need to manipulate
                

                # Set One to One relationship between
                # UserForm and UserProfileInfoForm
                profile.user = user

                log = Log()
                log.mob_no_log = profile.mob_no
                log.email_log = user.email
                log.refuser = user.username
                log.save()

                # Check if they provided a profile picture
                #if 'profile_pic' in request.FILES:
                #print('found it')
                # If yes, then grab it from the POST form reply
                #profile.profile_pic = request.FILES['profile_pic']

                # Now save model
                profile.save()

                # Registration Successful!
                registered = True
                subject = "Registration Sucessful Pravesha'19"
                message = render_to_string("basic_app/message_body.html",{'regid':user.username ,'fname':user.first_name,'lname':user.last_name})
                from_email = settings.EMAIL_HOST_USER
                to_list = [user.email]
                send_mail(subject,message,from_email,to_list,fail_silently=True)
                
                

        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors,profile_form.errors)

    else:
        # Was not an HTTP post so we just render the forms as blank.
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    # This is the render and context dictionary to feed
    # back to the registration.html file page.
    if registered== True:

        return render(request,'basic_app/registration.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered,
                           'username':user.username})
    else:
        return render(request,'basic_app/registration.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered,
                           })

def user_login(request):

    if request.method == 'POST':
        # First get the username and password supplied
        username = request.POST.get('username').upper()
        password = request.POST.get('password')

        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)

        # If we have a user
        if user:
            #Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request,user)
                # Send the user back to some page.
                # In this case their homepage.
                if user.profile.cs == False:
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return HttpResponseRedirect('coordinator')
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    else:
        #Nothing has been provided for username or password.
        return HttpResponseRedirect(reverse('index'))


def food_pref_updt(request):
        if request.method == 'POST':
            UserProfileInfo.objects.filter(mob_no=request.POST.get('no')).update(food_pref=request.POST.get('fp'))
            return HttpResponseRedirect(reverse('index'))

def participate(request):
    if request.method == 'POST':
        if request.POST.get('event') == 'pp':
            UserProfileInfo.objects.filter(mob_no=request.POST.get('no')).update(pp=True)
        elif request.POST.get('event') == 'bat':
            UserProfileInfo.objects.filter(mob_no=request.POST.get('no')).update(bat=True)
        elif request.POST.get('event') == 'tq':
            UserProfileInfo.objects.filter(mob_no=request.POST.get('no')).update(tq=True)
        elif request.POST.get('event') == 'ar':
            UserProfileInfo.objects.filter(mob_no=request.POST.get('no')).update(ar=True)
        elif request.POST.get('event') == 'aio':
            UserProfileInfo.objects.filter(mob_no=request.POST.get('no')).update(aio=True)
        elif request.POST.get('event') == 'ty':
            UserProfileInfo.objects.filter(mob_no=request.POST.get('no')).update(ty=True)
        elif request.POST.get('event') == 'syt':
            UserProfileInfo.objects.filter(mob_no=request.POST.get('no')).update(syt=True)
        elif request.POST.get('event') == 'mod':
            UserProfileInfo.objects.filter(mob_no=request.POST.get('no')).update(mod=True)
        elif request.POST.get('event') == 'th':
            UserProfileInfo.objects.filter(mob_no=request.POST.get('no')).update(th=True)
        elif request.POST.get('event') == 'pubg':
            UserProfileInfo.objects.filter(mob_no=request.POST.get('no')).update(pubg=True)
        # elif request.POST.get('event') == 'tiktok':
        #     UserProfileInfo.objects.filter(mob_no=request.POST.get('no')).update(tiktok=True)
        # elif request.POST.get('event') == 'opm':
        #     UserProfileInfo.objects.filter(mob_no=request.POST.get('no')).update(opm=True)
        # elif request.POST.get('event') == 'mc':
        #     UserProfileInfo.objects.filter(mob_no=request.POST.get('no')).update(mc=True)
        # elif request.POST.get('event') == 'meme':
        #     UserProfileInfo.objects.filter(mob_no=request.POST.get('no')).update(meme=True)
        return HttpResponseRedirect(reverse('index'))

def departicipate(request):
    if request.method == 'POST':
        if request.POST.get('event') == 'pp':
            UserProfileInfo.objects.filter(mob_no=request.POST.get('no')).update(pp=False)
        elif request.POST.get('event') == 'bat':
            UserProfileInfo.objects.filter(mob_no=request.POST.get('no')).update(bat=False)
        elif request.POST.get('event') == 'tq':
            UserProfileInfo.objects.filter(mob_no=request.POST.get('no')).update(tq=False)
        elif request.POST.get('event') == 'ar':
            UserProfileInfo.objects.filter(mob_no=request.POST.get('no')).update(ar=False)
        elif request.POST.get('event') == 'aio':
            UserProfileInfo.objects.filter(mob_no=request.POST.get('no')).update(aio=False)
        elif request.POST.get('event') == 'ty':
            UserProfileInfo.objects.filter(mob_no=request.POST.get('no')).update(ty=False)
        elif request.POST.get('event') == 'syt':
            UserProfileInfo.objects.filter(mob_no=request.POST.get('no')).update(syt=False)
        elif request.POST.get('event') == 'mod':
            UserProfileInfo.objects.filter(mob_no=request.POST.get('no')).update(mod=False)
        elif request.POST.get('event') == 'th':
            UserProfileInfo.objects.filter(mob_no=request.POST.get('no')).update(th=False)
        elif request.POST.get('event') == 'pubg':
            UserProfileInfo.objects.filter(mob_no=request.POST.get('no')).update(pubg=False)
        # elif request.POST.get('event') == 'tiktok':
        #     UserProfileInfo.objects.filter(mob_no=request.POST.get('no')).update(tiktok=False)
        # elif request.POST.get('event') == 'opm':
        #     UserProfileInfo.objects.filter(mob_no=request.POST.get('no')).update(opm=False)
        # elif request.POST.get('event') == 'mc':
        #     UserProfileInfo.objects.filter(mob_no=request.POST.get('no')).update(mc=False)
        # elif request.POST.get('event') == 'meme':
        #     UserProfileInfo.objects.filter(mob_no=request.POST.get('no')).update(meme=False)
        return HttpResponseRedirect(reverse('index'))

def user(request):
    return render(request, 'basic_app/user.html')


def report(request):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='hello.pdf')


