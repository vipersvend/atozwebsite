from django.shortcuts import render
from django.shortcuts import render,redirect,HttpResponse,HttpResponseRedirect
# Create your views here.
from django.contrib.auth import authenticate, login as auth_login
from UserApp.models import *
from json import dumps
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import random
import string
import json
from django.core.files.storage import FileSystemStorage
from PIL import Image
import os
from django.core.mail import send_mail
import datetime
from django.conf import settings
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = settings.URL
from django.contrib.auth import logout
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.core import serializers
cursor = connection.cursor()

#query = "delete from  UserApp_serviceproviders;;"
#print(cursor.executescript(query))

#20 - comment length
def check_comment_length(query, num_of_comments):

    return len(query.split('--')[1:]) == num_of_comments
    #return len(query.split(';')[-2].split('--')[-1]) == predefined_length


main_context = {
    'URL': URL,
    'providers': ServiceProviders.objects.all(),
    'services': Services.objects.all(),
    'locations': Locations.objects.all(),
    'categories': Category.objects.all()
}


def update_context():
    global main_context
    main_context = {}
    main_context['providers'] = ServiceProviders.objects.all()
    main_context['services'] = Services.objects.all()
    main_context['locations'] = Locations.objects.all()
    main_context['categories'] = Category.objects.all()
    main_context['URL'] = URL

replace_specials = {
    '-': '&dash',
    '<':'&lte;',
    '>':'&gte;',
    "'":'&inv_c;',
    "&":'&semi-C',
    "*":'&Star-C'
}

def is_clean(string):
    final = ''
    for x in string:
        try:
            final += replace_specials[x]
        except:
            final += x
    return final == string

#print(is_clean('select * from sql'))

def count_queries(string, count):
    return count == len([query for query in string.split('--')[0].split(';') if query.strip() != ''])

#print(count_queries('Select * from abc; delete from abc', 2)) # Returns True, since number of queris == 1

#print(check_comment_length("insert into USerApp_dummy( 'name', 'email', 'location', 'message') values('firstname', 'email', 'location', 'entry'); delete from user", 1))
#for row in cursor.execute('select * from UserApp_serviceproviders;'):
#    print(row)

def index(request):
    if request.method == 'POST':

        request.session['location'] = Locations.objects.get(location_id = request.POST.get('location')).location_name
        return redirect('home')
    try:
        print('CHECKING IF SESSION Throws any ERROR')
        print('*** META DATA : ***', request.session['location'] )
        #if the above line executes successfully, customer session is created
        print('CUSTOMER session is created already')
    except:
        print('CREATING NEW SESSION')
        request.session.create()
        request.session['location'] = ''

    context_dictionary = {'location':request.session['location']}
    context = dumps(context_dictionary)
    locations = Locations.objects.all()
    services = Services.objects.all()

    update_context()
    main_context['session_data'] = context
    return render(request, 'user/index.html',main_context )


def all_services(request):
    update_context()
    return render(request, 'user/allservices.html', main_context)

def login(request):
    logout(request)
    if request.method == 'POST':
        emailid = request.POST.get('emailid')
        password = request.POST.get('password')
        user = authenticate(username=emailid, password=password)
        
        if user is not None:
            print('USER AUTHENTICATED')
            auth_login(request, user)
            return redirect('home')
        else:
            return redirect('login')
        #authenticate(request, user)
    update_context()
    return render(request, 'user/login.html', main_context)

def new_service(request):
    if request.method == 'POST':
        service_name = request.POST.get('service_name')
        service_description  = request.POST.get('service_description')
        service_category = request.POST.get('service_category')
        uploaded_image = request.FILES['service_image']
        im = Image.open(uploaded_image)
        im = im.resize((506,601))

        #location_id = request.POST.get('service_location')

        service_id = ''.join(random.choices(string.ascii_uppercase + string.digits,k= 10))


        fs = FileSystemStorage()
        filename_gen = uploaded_image.name.split('.')
        print(filename_gen)
        filename = service_id+'.'+filename_gen[-1]
        #fs.save(filename,im)
    
        SAVE_IMAGE_LOCATION = os.path.join(BASE_DIR,'static','img',filename)

        im.save(SAVE_IMAGE_LOCATION)
        print("SAVE LOCATION IS: ",SAVE_IMAGE_LOCATION)


        Services.objects.create(
            service_id = service_id,
            service_image_name = filename,
            service_name = service_name,
            service_description = service_description,
            category = service_category
        )

    update_context()
    return render(request, 'user/newservice.html', main_context)


def dummy(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        location = request.POST.get('location')
        message = request.POST.get('message')

        query_string = f"insert into USerApp_dummy( 'name', 'email', 'location', 'message') values('{name}', '{email}', '{location}', '{message}' ); -- FixedLength Comment;"
        
        #if not check_comment_length(query_string, 1):
        #    return HttpResponse('INJECTION ATTACK! Incorrect Comment Length')
        #for entries in [name, email, location, message]:
        #    if not is_clean(entries):
        #        return HttpResponse('INJECTION ATTACK! Sepcial Characters Detected')


        #if not count_queries(query_string, 1):
        #    return HttpResponse('Multiple Queries Detected')
        
        cursor.executescript(query_string)

        # Insert Into Dummy
        Dummy.objects.create(
            name = name,
            email = email,
            location = location,
            message = message
        )


        # Select * from Dummy
        #Dummy.objects.all()

        # Select * from Dummy where name = 'Yash'
        #Dummy.objects.all().filter(name = 'Yash')

    update_context()
    return render(request, 'user/dummy.html',main_context)

def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        #location = request.POST.get('location')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        user_id = ''.join(random.choices(string.ascii_uppercase + string.digits,k= 10))
        newuser = UserProfile.objects.create(
            user_id = user_id, 
            contact_number = phone,
            name = name,
            username = email,
            email = email
        )
        newuser.set_password(password)

        newuser.save()
        return redirect('login')
        #query_string = f"insert into USerApp_dummy( 'name', 'email', 'location', 'message') values('{firstname}', '{email}', '{location}', '{message}' ); -- FixedLength Comment;"
        
        #if not check_comment_length(query_string, 1):
        #    return HttpResponse('INJECTION ATTACK! Incorrect Comment Length')
        #for entries in [firstname, email, location, message]:
        #    if not is_clean(entries):
        #        return HttpResponse('INJECTION ATTACK! Sepcial Characters Detected')


        #if not count_queries(query_string, 1):
        #    return HttpResponse('Multiple Queries Detected')
        

        # Insert Into Dummy
        #Dummy.objects.create(
        #    name = firstname,
        #    email = email,
        #    location = location,
        #    message = message
        #)

        #cursor.executescript(query_string)
        # Select * from Dummy
        #Dummy.objects.all()

        # Select * from Dummy where name = 'Yash'
        #Dummy.objects.all().filter(name = 'Yash')

    update_context()
    return render(request, 'user/register.html',main_context)

#def service(request):
#    update_context()
#    return render(request, 'user/service.html',main_context)

def serviceproviders(request):
    update_context()
    return render(request,'user/allproviders.html',main_context)
def new_provider(request):
    if request.method == 'POST':


        provider_id = ''.join(random.choices(string.ascii_uppercase + string.digits,k= 10))


        uploaded_image = request.FILES['provider_image']

        im = Image.open(uploaded_image)
        im = im.resize((150,150))
        fs = FileSystemStorage()
        filename_gen = uploaded_image.name.split('.')
        print(filename_gen)
        filename = provider_id+'.'+filename_gen[-1]
        SAVE_IMAGE_LOCATION = os.path.join(BASE_DIR,'static','img',filename)
        im.save(SAVE_IMAGE_LOCATION)
        print("SAVE LOCATION IS: ",SAVE_IMAGE_LOCATION)


        ServiceProviders.objects.create( 
        provider_name = request.POST.get('provider_name'),
        provider_id = provider_id,
        provider_image_name = filename,
        provider_location = Locations.objects.get(location_id = request.POST.get('provider_location')),
        provider_service = Services.objects.get(service_id = request.POST.get('provider_service')),
        provider_number = request.POST.get('provider_number')
        )
        pass

    update_context()
    return render(request, 'user/newprovider.html', main_context)


def populate_db(request):
    for x in [(1, 'UBDUJSANDU', 'Pune'),(2, 'SD123ASD32', 'Delhi'),(3, '6217431DSA', 'Mumbai')]:
        try:
            Locations.objects.create(
                location_id = x[1],
                location_name = x[2]
            )
        except:
            pass
    return HttpResponse("Done!")

def logout_view(request):
    logout(request)
    return redirect('home')

def service(request, service_id):
    service = Services.objects.get(service_id = service_id)

    update_context()
    main_context['service']=service
    return render(request, 'user/service_landing.html' ,main_context)

def new_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        uploaded_image = request.FILES['category_image']
        im = Image.open(uploaded_image)
        im = im.resize((500,500))

        category_id = ''.join(random.choices(string.ascii_uppercase + string.digits,k= 10))


        fs = FileSystemStorage()
        filename_gen = uploaded_image.name.split('.')
        print(filename_gen)
        filename = category_id+'.'+filename_gen[-1]
        #fs.save(filename,im)
    
        SAVE_IMAGE_LOCATION = os.path.join(BASE_DIR,'static','img',filename)

        im.save(SAVE_IMAGE_LOCATION)
        print("SAVE LOCATION IS: ",SAVE_IMAGE_LOCATION)


        Category.objects.create(
            category_id = category_id,
            category_image_name = filename,
            category_name = category_name,
        )

    update_context()
    return render(request, 'user/newcategory.html', main_context)

def categories(request):
    update_context()
    all_categories = Category.objects.all()
    main_context['categories']=all_categories
    return render(request, 'user/allcategories.html', main_context)


def category(request, category_id):
    category = Category.objects.get(category_id = category_id)
    filtered_services = Services.objects.all().filter(category = category_id)
    
    update_context()
    main_context['filtered_services'] = filtered_services
    main_context['category'] = category
    print(main_context)
    return render(request, 'user/category_services.html', main_context )


def reset_email_message(otp_id):
    return '''
Hi User,
Please use the below URL to reset your password with AtoZsabkuch.com
Note: Do not share the URL with anyone else.

URL: '''+URL+"/change_password/"+otp_id+'''.

Best Regards. 😄
'''    

def forgotpassword(request):
    message = None
    if request.method == 'POST':

        useremail = request.POST.get('emailid')
        user = User.objects.get(email = useremail)
        PasswordReset.objects.all().filter(email = useremail).delete()
        otp_id = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase+string.digits,k= 50))
        PasswordReset.objects.create(
            email = useremail,
            otp_id = otp_id
        )
        body = reset_email_message(otp_id)
        send_mail(
            "Password Reset Request",
            body,
            settings.EMAIL_HOST_USER,
            [useremail]
        )
        return redirect("emailsent")
            

        message = True
        return redirect('forgotpassword')
    
    update_context()
    main_context['message'] = message
    return render(request, 'user/forgotpassword.html', main_context)

def change_password(request, otp_id):
    if request.method == 'POST':
        try:
            print(request.POST.get('emailid'),request.POST.get('otp_id'))
            try:
                resetobj = PasswordReset.objects.get(email = request.POST.get('emailid'), otp_id = request.POST.get('otp_id'))
            except:
                return HttpResponse('Password Reset Link has been Expired')
            user = User.objects.get(email = request.POST.get('emailid'))

            user.set_password(request.POST.get('password'))
            user.save()
            resetobj.delete()
            logout(request)
            return redirect('login')

        except:
            return redirect('changepassword')
    update_context()
    try:
        email = PasswordReset.objects.get(otp_id = otp_id).email
    except:
        return HttpResponse('Password Reset Link has been Expired')
    main_context['emailid'] = email
    main_context['otp_id'] = otp_id
    return render(request, 'user/changepassword.html', main_context)


def emailsent(request):
    update_context()
    
    return render(request, 'user/emailsent.html', main_context)

@login_required(login_url = 'login')
def book_service(request, service_id):
    self_profile = UserProfile.objects.get(username = request.user)
    new_order = Orders.objects.create(
        order_id = ''.join(random.choices(string.ascii_uppercase + string.digits,k= 10)),
        order_customer = self_profile,
        order_services = [service_id],
        order_total_bill  = 99
    )
    return redirect('my_orders')

def my_orders(request):
    try:
        self_profile = UserProfile.objects.get(username = request.user)
    except:
        return redirect('login')
    request.session['my_orders'] = json.loads(serializers.serialize('json',[Services.objects.get(service_id = order.order_services[0]) for order in Orders.objects.all().filter(order_customer = self_profile)]))
    print(request.session['my_orders'])
    print(type(request.session['my_orders']))
    update_context()
    return render(request, 'user/myorders.html',main_context)