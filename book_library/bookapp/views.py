from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader, Template
from django.middleware.csrf import get_token
from bookapp.models import users, Listings
from bookapp.bookapis import get_book_info_from_isbn
import smtplib
import random
import string
import time
import calendar
from datetime import datetime

# import custom functions

# Create your views here.


def homepage(request):
    if 'user_login' in request.session:
        context = {
            "home_class": "active",
            "about_class": "inactive",
            "contact_class": "inactive",
            "ishidden": "hidden",
            "isnothidden": ""
        }
    else:
        context = {
            "home_class": "active",
            "about_class": "inactive",
            "contact_class": "inactive",
            "ishidden": "",
            "isnothidden": "hidden"
        }

    renderdata = {}
    renderdata['context'] = context
    template = loader.get_template('homepage.html')
    return HttpResponse(template.render(renderdata, request))


def signup(request):
    if 'user_login' in request.session:
        return redirect('homepage')
    else:
        # Create csrf token
        csrf_token = get_token(request)

        # If the form is submitted
        if request.method == "POST":
            # check if email id does not already exist
            if not users.objects.filter(email_id=request.POST["email"]):
                # check if passwords match or not
                if request.POST["password_1"] == request.POST["password_2"]:
                    error_message = ""
                    context = {
                        "csrf_token": csrf_token,
                        "error_message": error_message,
                        "ishidden": "",
                        "isnothidden": "hidden"
                    }
                    user_id = ''.join(random.choices(string.digits, k=18))
                    firstname = request.POST["firstname"]
                    lastname = request.POST["lastname"]
                    emailid = request.POST["email"]
                    pw = request.POST["password_1"]
                    data = users(id=user_id, firstname=firstname, lastname=lastname,
                                 email_id=emailid, password=pw)
                    data.save()
                    request.session['user_login'] = str(
                        users.objects.get(email_id=emailid).id)
                    request.session.modify = True
                    return redirect('homepage')
                else:
                    error_message = "Passwords do not match"
                    context = {
                        "csrf_token": csrf_token,
                        "error_message": error_message,
                        "ishidden": "",
                        "isnothidden": "hidden"
                    }
                    renderdata = {}
                    renderdata['context'] = context
                    template = loader.get_template('signup.html')
                    return HttpResponse(template.render(renderdata, request))
            else:
                error_message = "Email ID is already registered"
                context = {
                    "csrf_token": csrf_token,
                    "error_message": error_message,
                    "ishidden": "",
                    "isnothidden": "hidden"
                }
                template = loader.get_template('signup.html')
                renderdata = {}
                renderdata['context'] = context
                return HttpResponse(template.render(renderdata, request))
        else:
            context = {
                "csrf_token": csrf_token,
                "ishidden": "",
                "isnothidden": "hidden"
            }
            renderdata = {}
            renderdata['context'] = context
            template = loader.get_template('signup.html')
            return HttpResponse(template.render(renderdata, request))


def login(request):
    if 'user_login' in request.session:
        return redirect('homepage')
    else:
        # Create csrf token
        csrf_token = get_token(request)

        # Once form is submitted
        if request.method == "POST":
            email_address = request.POST["email"]
            pw = request.POST["password"]
            # Check if the particular email id and password exits in the database
            if users.objects.filter(email_id=email_address) and users.objects.filter(password=pw):
                user_id = users.objects.get(email_id=email_address).id
                if pw == users.objects.get(id=user_id).password:
                    error_message = ""
                    context = {
                        "csrf_token": csrf_token,
                        "error_message": error_message,
                        "ishidden": "",
                        "isnothidden": "hidden"
                    }
                    request.session['user_login'] = str(
                        users.objects.get(email_id=email_address).id)
                    request.session.modify = True
                    return redirect('homepage')
                else:
                    error_message = "record not found"
                    context = {
                        "csrf_token": csrf_token,
                        "error_message": error_message,
                        "ishidden": "",
                        "isnothidden": "hidden"
                    }

                    renderdata = {}
                    renderdata['context'] = context

                    template = loader.get_template('login.html')
                    return HttpResponse(template.render(renderdata, request))
            else:
                error_message = "record not found"
                context = {
                    "csrf_token": csrf_token,
                    "error_message": error_message,
                    "ishidden": "",
                    "isnothidden": "hidden"
                }
                renderdata = {}
                renderdata['context'] = context

                template = loader.get_template('login.html')
                return HttpResponse(template.render(renderdata, request))
        else:
            context = {
                "csrf_token": csrf_token,
                "ishidden": "",
                "isnothidden": "hidden"
            }

            renderdata = {}
            renderdata['context'] = context

            template = loader.get_template('login.html')
            return HttpResponse(template.render(renderdata, request))


def about(request):
    if 'user_login' in request.session:
        context = {
            "ishidden": "hidden",
            "isnothidden": "",
            "home_class": "inactive",
            "about_class": "active",
            "contact_class": "inactive",
        }
    else:
        context = {
            "ishidden": "",
            "isnothidden": "hidden",
            "home_class": "inactive",
            "about_class": "active",
            "contact_class": "inactive",
        }

    renderdata = {}
    renderdata['context'] = context
    template = loader.get_template('about.html')
    return HttpResponse(template.render(renderdata))


def contact(request):
    if 'user_login' in request.session:
        context = {
            "ishidden": "hidden",
            "isnothidden": "",
            "home_class": "inactive",
            "about_class": "inactive",
            "contact_class": "active",
        }
    else:
        context = {
            "ishidden": "",
            "isnothidden": "hidden",
            "home_class": "inactive",
            "about_class": "inactive",
            "contact_class": "active",
        }

    renderdata = {}
    renderdata['context'] = context
    template = loader.get_template('contact.html')
    return HttpResponse(template.render(renderdata))


def website_template(request):
    template = loader.get_template('website_template.html')
    return HttpResponse(template.render())


def test(request):
    template = loader.get_template('test.html')
    return HttpResponse(template.render())


def profile(request):
    if 'user_login' in request.session:
        context = {
            "ishidden": "hidden",
            "isnothidden": "",
            "home_class": "inactive",
            "about_class": "inactive",
            "contact_class": "inactive",
        }
        renderdata = {}
        renderdata['context'] = context
        template = loader.get_template('profile.html')
        return HttpResponse(template.render(renderdata, request))
    else:
        return redirect('login')


def browse_listings(request):
    csrf_token = get_token(request)
    listings = Listings.objects.all().values()
    if request.method == "POST":
        query = request.POST["query"]
        listings = Listings.objects.filter(book_title__icontains=query)
        numberOfResults = listings.count()
        if listings:
            noResults = "hidden"
        else:
            noResults = ""
        if numberOfResults == 1:
            s = ""
        else:
            s = "s"
        if 'user_login' in request.session:
            context = {
                "csrf_token": csrf_token,
                "ishidden": "hidden",
                "isnothidden": "",
                "home_class": "inactive",
                "about_class": "inactive",
                "contact_class": "inactive",
                "query": query,
                "madequery": "",
                "listings": listings,
                "noResults": noResults,
                "numberOfResults": numberOfResults,
                "s": s,
            }
        else:
            context = {
                "csrf_token": csrf_token,
                "ishidden": "",
                "isnothidden": "hidden",
                "home_class": "inactive",
                "about_class": "inactive",
                "contact_class": "inactive",
                "query": query,
                "madequery": "",
                "listings": listings,
                "noResults": noResults,
                "numberOfResults": numberOfResults,
                "s": s,
            }
    else:
        noResults = "hidden"
        numberOfResults = 0
        s = ""
        if 'user_login' in request.session:
            context = {
                "csrf_token": csrf_token,
                "ishidden": "hidden",
                "isnothidden": "",
                "home_class": "inactive",
                "about_class": "inactive",
                "contact_class": "inactive",
                "query": "",
                "madequery": "hidden",
                "listings": listings,
                "noResults": noResults,
                "numberOfResults": numberOfResults,
                "s": s,
            }
        else:
            context = {
                "csrf_token": csrf_token,
                "ishidden": "",
                "isnothidden": "hidden",
                "home_class": "inactive",
                "about_class": "inactive",
                "contact_class": "inactive",
                "query": "",
                "madequery": "hidden",
                "listings": listings,
                "noResults": noResults,
                "numberOfResults": numberOfResults,
                "s": s,
            }
    renderdata = {}

    renderdata['context'] = context
    template = loader.get_template('search.html')
    return HttpResponse(template.render(renderdata, request))


# add context and listings into a 2d dict called renderdata


def add_listing(request):
    csrf_token = get_token(request)
    if 'user_login' in request.session:
        context = {
            "ishidden": "hidden",
            "isnothidden": "",
            "home_class": "inactive",
            "about_class": "inactive",
            "contact_class": "inactive",
            "csrf_token": csrf_token,
        }
        if request.method == "POST":

            isbn = request.POST["isbn"]

            bookdata = get_book_info_from_isbn(isbn)
            book_title = bookdata[0]
            genre = bookdata[2][0]
            if bookdata[4] == 'NOT_MATURE':
                age = 18
            else:
                age = 13
            imgurl = bookdata[5]
            description = bookdata[1]
            if request.POST["saleOrBorrow"] == "sale":
                isForSale = True
                isForBorrowing = not isForSale
            else:
                isForBorrowing = True
                isForSale = not isForBorrowing
            price = request.POST["price"]
            data = Listings(userid=request.session['user_login'], book_title=book_title, isbn=isbn,
                            genre=genre, age_group=age, for_sale=isForSale, for_borrowing=not isForSale, price=price, imgurl=imgurl, description=description)
            data.save()
            return redirect('search')
        else:
            renderdata = {}
            renderdata['context'] = context
            template = loader.get_template('add_listing.html')
            return HttpResponse(template.render(renderdata, request))
    else:
        return redirect('login')


def signout(request):
    del request.session['user_login']
    return redirect('homepage')


def forgot(request):
    if 'user_login' in request.session:
        return redirect('homepage')
    else:
        if 'user_requested_password' in request.session:
            print(request.session['user_requested_password'])
            del request.session['user_requested_password']
        # Create csrf token
        csrf_token = get_token(request)

        # Once form is submitted
        if request.method == "POST":
            user_email_address = request.POST["email"]
            if users.objects.filter(email_id=user_email_address):
                context = {
                    "csrf_token": csrf_token,
                    "ishidden": "",
                    "isnothidden": "hidden",
                    "error_message": ""
                }
                # Needs to send email with new password
                print("email address: ", user_email_address)

                # send email to reset password
                with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                    smtp.ehlo()
                    smtp.starttls()
                    smtp.ehlo()

                    smtp.login('ispsinstock@gmail.com', 'acsfrsxmxbtcrmbj')

                    subject = 'Reprose Password Reset'
                    body = f'To reset your password, click on the following link: http://localhost:8000/resetPassword'

                    msg = f'Subject: {subject}\n\n{body}'

                    smtp.sendmail('ispsinstock@gmail.com',
                                  user_email_address, msg)
                request.session['user_requested_password'] = users.objects.get(
                    email_id=user_email_address).id
                return redirect('homepage')
            else:
                context = {
                    "csrf_token": csrf_token,
                    "ishidden": "",
                    "isnothidden": "hidden",
                    "error_message": "email id not found"
                }
                renderdata = {}
                renderdata['context'] = context
                template = loader.get_template('forgotPassword.html')
                return HttpResponse(template.render(renderdata, request))
        else:
            context = {
                "csrf_token": csrf_token,
                "ishidden": "",
                "isnothidden": "hidden",
                "error_message": ""
            }

            renderdata = {}
            renderdata['context'] = context

            template = loader.get_template('forgotPassword.html')
            return HttpResponse(template.render(renderdata, request))


def resetpw(request):
    if 'user_login' in request.session:
        return redirect('homepage')
    else:
        if 'user_requested_password' in request.session:
            print(request.session['user_requested_password'])
            csrf_token = get_token(request)
            if request.method == "POST":
                if request.POST['password1'] == request.POST['password2']:
                    context = {
                        "csrf_token": csrf_token,
                        "ishidden": "",
                        "isnothidden": "hidden",
                        "error_message": ""
                    }
                    renderdata = {}
                    renderdata['context'] = context
                    newpassword = request.POST['password1']
                    x = users.objects.get(
                        id=request.session['user_requested_password'])
                    x.password = newpassword
                    x.save()
                    request.session['user_login'] = str(
                        users.objects.get(id=request.session['user_requested_password']))
                    request.session.modify = True
                    del request.session['user_requested_password']
                    print(request.session['user_login'])
                    return redirect('homepage')

            else:
                context = {
                    "csrf_token": csrf_token,
                    "ishidden": "",
                    "isnothidden": "hidden",
                    "error_message": ""
                }
                renderdata = {}
                renderdata['context'] = context
                template = loader.get_template('resetPassword.html')
                return HttpResponse(template.render(renderdata, request))
        else:
            return redirect('forgotPassword')


def bookinfo(request, id):
    bookdata = Listings.objects.filter(id=id).values()
    # print(type(bookdata))
    context = {
        'id': id,
        'bookdata': bookdata,
        'imgurl': Listings.objects.get(id=id).imgurl,
        'book_title': Listings.objects.get(id=id).book_title
    }
    template = loader.get_template('bookinfo.html')
    return HttpResponse(template.render(context, request))
    return HttpResponse('<p>The id is {}</p>'.format(id))


def cart(request):
    context = {}
    template = loader.get_template('cart.html')
    return HttpResponse(template.render(context, request))
