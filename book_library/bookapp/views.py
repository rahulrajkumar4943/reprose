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
import json
import ast

# import custom functions

# Create your views here.


def homepage(request):
    csrf_token = get_token(request)
    listings = Listings.objects.filter(id=-1).values()
    number_of_best_selling = 7  # number of listings shown on homepage
    # show only the first ____ number of listings
    for i in range(number_of_best_selling):
        checkid = str(i+1)
        listings = listings | Listings.objects.filter(id=checkid).values()
        # print(len(listings))
    if 'user_login' in request.session:

        name = users.objects.get(id=request.session['user_login']).firstname

        context = {
            "csrf_token": csrf_token,
            "home_class": "active",
            "about_class": "inactive",
            "contact_class": "inactive",
            "ishidden": "hidden",
            "isnothidden": "",
            "listings": listings,
            "name": name,
        }
    else:
        context = {
            "csrf_token": csrf_token,
            "home_class": "active",
            "about_class": "inactive",
            "contact_class": "inactive",
            "ishidden": "",
            "isnothidden": "hidden",
            "listings": listings,
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
    csrf_token = get_token(request)

    if 'user_login' in request.session:

        name = users.objects.get(id=request.session['user_login']).firstname

        context = {
            "csrf_token": csrf_token,
            "ishidden": "hidden",
            "isnothidden": "",
            "home_class": "inactive",
            "about_class": "active",
            "contact_class": "inactive",
            "name": name,
        }
    else:
        context = {
            "csrf_token": csrf_token,
            "ishidden": "",
            "isnothidden": "hidden",
            "home_class": "inactive",
            "about_class": "active",
            "contact_class": "inactive",
        }

    renderdata = {}
    renderdata['context'] = context
    template = loader.get_template('about.html')
    return HttpResponse(template.render(renderdata, request))


def contact(request):
    csrf_token = get_token(request)

    if request.method == "POST":
        if 'user_login' in request.session:
            email_address = users.objects.get(
                id=request.session['user_login']).email_id

            name = users.objects.get(
                id=request.session['user_login']).firstname

            context = {
                "csrf_token": csrf_token,
                "ishidden": "hidden",
                "isnothidden": "",
                "home_class": "inactive",
                "about_class": "inactive",
                "contact_class": "active",
                "logged_in": True,
                "name": name,
            }
        else:
            email_address = request.POST["email"]

            context = {
                "csrf_token": csrf_token,
                "ishidden": "",
                "isnothidden": "hidden",
                "home_class": "inactive",
                "about_class": "inactive",
                "contact_class": "active",
                "logged_in": False,
            }

        t = time.localtime()

        send_to = 'praneeth.suresh@giis.edu.sg'

        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()

            smtp.login('ispsinstock@gmail.com', 'acsfrsxmxbtcrmbj')

            message = f"""Dear manager,
            User with the email id {email_address} has the following query for you:

            {request.POST["query"]}

            The query was generated at {time.strftime("%H:%M:%S", t)}

            With Regards,
            Computer system
            """

            subject = 'Query for reprose'

            msg = f'Subject: {subject}\n\n{message}'

            smtp.sendmail('ispsinstock@gmail.com',
                          send_to, msg)

            print("Query send to manager.")

        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()

            smtp.login('reprose.xx@gmail.com', 'Garlicbread123')

            message = f"""Dear manager,
            User with the email id {email_address} has the following query for you:

            {request.POST["query"]}

            The query was generated at {time.strftime("%H:%M:%S", t)}

            With Regards,
            Computer system
            """

            subject = 'Query for reprose'

            msg = f'Subject: {subject}\n\n{message}'

            smtp.sendmail('reprose.xx@gmail.com',
                          send_to, msg)

            print("Query send to manager.")

    else:
        if 'user_login' in request.session:

            name = users.objects.get(
                id=request.session['user_login']).firstname

            context = {
                "csrf_token": csrf_token,
                "ishidden": "hidden",
                "isnothidden": "",
                "home_class": "inactive",
                "about_class": "inactive",
                "contact_class": "active",
                "logged_in": True,
                "name": name,
            }
        else:
            context = {
                "csrf_token": csrf_token,
                "ishidden": "",
                "isnothidden": "hidden",
                "home_class": "inactive",
                "about_class": "inactive",
                "contact_class": "active",
                "logged_in": False,
            }

    renderdata = {}
    renderdata['context'] = context
    template = loader.get_template('contact.html')
    return HttpResponse(template.render(renderdata, request))


def test(request):
    template = loader.get_template('test.html')
    return HttpResponse(template.render())


def profile(request):
    if 'user_login' in request.session:

        UserBio = users.objects.get(
            id=request.session['user_login'])

        listings = Listings.objects.filter(userid=UserBio.id).values()

        listings = list(listings)

        context = {
            "ishidden": "hidden",
            "isnothidden": "",
            "home_class": "inactive",
            "about_class": "inactive",
            "contact_class": "inactive",
            "name": UserBio.firstname + " " + UserBio.lastname,
            "email": UserBio.email_id,
            "listings": listings,
            "num_listings": len(listings)
        }
        renderdata = {}
        renderdata['context'] = context
        template = loader.get_template('profile.html')
        return HttpResponse(template.render(renderdata, request))
    else:
        return redirect('login')


def profile_listings(request):
    if 'user_login' in request.session:
        print("listings profile")
        UserBio = users.objects.get(
            id=request.session['user_login'])

        listings = Listings.objects.filter(userid=UserBio.id).values()

        listings = list(listings)

        context = {
            "ishidden": "hidden",
            "isnothidden": "",
            "home_class": "inactive",
            "about_class": "inactive",
            "contact_class": "inactive",
            "name": UserBio.firstname + " " + UserBio.lastname,
            "email": UserBio.email_id,
            "listings": listings,
            "num_listings": len(listings)
        }
        renderdata = {}
        renderdata['context'] = context
        template = loader.get_template('profile_listings.html')
        return HttpResponse(template.render(renderdata, request))
    else:
        return redirect('login')


def browse_listings(request):
    csrf_token = get_token(request)
    listings = Listings.objects.all().values()
    if request.method == "POST":
        if request.POST.get('filter_search'):
            print("filter")
            query = "found"
            if request.POST.get('minprice'):
                min_price = request.POST.get('minprice')
            else:
                min_price = 0

            if request.POST.get('maxprice'):
                max_price = request.POST.get('maxprice')
            else:
                max_price = 1000

            if request.POST.get('condition'):
                condition = request.POST.get('condition')
            else:
                condition = "w"

            if request.POST.get('genre'):
                genre = request.POST.get('genre')
            else:
                genre = ""
            if request.POST.get('age_group'):
                age_group = request.POST.get('age_group')
            else:
                age_group = "1"
            if request.POST.get('saleLend'):
                saleLend = request.POST.get('saleLend')
            else:
                saleLend = "ing"
            listings = Listings.objects.filter(
                price__range=(min_price, max_price), condition__icontains=condition, saleOrBorrow__icontains=saleLend, age_group__icontains=age_group)
        else:
            print("no-filter")
            query = request.POST.get("query")
            listings = Listings.objects.filter(
                book_title__icontains=query) | Listings.objects.filter(description__icontains=query)
            query = "for " + request.POST.get("query")
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

            name = users.objects.get(
                id=request.session['user_login']).firstname

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
                "name": name,
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

            name = users.objects.get(
                id=request.session['user_login']).firstname

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
                "name": name,
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

        name = users.objects.get(id=request.session['user_login']).firstname

        context = {
            "ishidden": "hidden",
            "isnothidden": "",
            "home_class": "inactive",
            "about_class": "inactive",
            "contact_class": "inactive",
            "csrf_token": csrf_token,
            "name": name,
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
            saleOrBorrow = request.POST["listingType"]
            price = request.POST["price"]
            condition = request.POST['condition']
            try:
                data = Listings(userid=request.session['user_login'], book_title=book_title, isbn=isbn,
                                genre=genre, age_group=age, saleOrBorrow=saleOrBorrow, price=price, imgurl=imgurl, description=description, condition=condition, times_viewed=0, borrowed_date=0)
                data.save()
            except ValueError:
                price = 0
                data = Listings(userid=request.session['user_login'], book_title=book_title, isbn=isbn,
                                genre=genre, age_group=age, saleOrBorrow=saleOrBorrow, price=price, imgurl=imgurl, description=description, condition=condition, times_viewed=0, borrowed_date=0)
                data.save()
            return redirect('search')
        else:
            renderdata = {}
            renderdata['context'] = context
            template = loader.get_template('add_listing.html')
            return HttpResponse(template.render(renderdata, request))
    else:
        return redirect('login')


def remove_listing(request):
    bookid = request.POST['remove_listing']
    listings = Listings.objects.get(id=bookid)
    listings.delete()
    return redirect('profile_listings')


def signout(request):
    del request.session['user_login']
    return redirect('homepage')


def forgot(request):
    if 'user_login' in request.session:
        return redirect('homepage')
    else:
        # Create csrf token
        csrf_token = get_token(request)

        # Once form is submitted
        if request.method == "POST":
            if 'user_requested_password' in request.session:
                del request.session['user_requested_password']
            user_email_address = request.POST["email"]
            if users.objects.filter(email_id=user_email_address):
                context = {
                    "csrf_token": csrf_token,
                    "ishidden": "",
                    "isnothidden": "hidden",
                    "error_message": "",
                    "hide": "hidden",
                    "unhide": "",
                }
                renderdata = {}
                renderdata['context'] = context
                # generate random url extension
                url_extension = ''.join(random.choices(
                    string.ascii_lowercase + string.ascii_uppercase + string.digits, k=16))

                # Needs to send email with new password
                print("email address: ", user_email_address)

                # send email to reset password
                with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                    smtp.ehlo()
                    smtp.starttls()
                    smtp.ehlo()

                    smtp.login('ispsinstock@gmail.com', 'acsfrsxmxbtcrmbj')

                    subject = 'Reprose Password Reset'
                    body = f'To reset your password, click on the following link: http://localhost:8000/resetPassword/{url_extension}'

                    msg = f'Subject: {subject}\n\n{body}'

                    smtp.sendmail('ispsinstock@gmail.com',
                                  user_email_address, msg)
                request.session['user_requested_password'] = [users.objects.get(
                    email_id=user_email_address).id]
                request.session['user_requested_password'].insert(
                    1, url_extension)
                template = loader.get_template('forgotPassword.html')
                return HttpResponse(template.render(renderdata, request))
            else:
                context = {
                    "csrf_token": csrf_token,
                    "ishidden": "",
                    "isnothidden": "hidden",
                    "error_message": "email id not found",
                    "hide": "",
                    "unhide": "hidden",
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
                "error_message": "",
                "hide": "",
                "unhide": "hidden",
            }

            renderdata = {}
            renderdata['context'] = context

            template = loader.get_template('forgotPassword.html')
            return HttpResponse(template.render(renderdata, request))


def resetpw(request, extension):
    if 'user_login' in request.session:
        return redirect('homepage')
    elif 'user_requested_password' in request.session:
        if extension == request.session['user_requested_password'][1]:
            print(extension)
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
                            id=request.session['user_requested_password'][0])
                        x.password = newpassword
                        x.save()
                        request.session['user_login'] = str(
                            users.objects.get(id=request.session['user_requested_password'][0]))
                        request.session.modify = True
                        del request.session['user_requested_password']
                        print(request.session['user_login'])
                        return redirect('homepage')
                    else:
                        context = {
                            "csrf_token": csrf_token,
                            "ishidden": "",
                            "isnothidden": "hidden",
                            "error_message": "passwords do not match"
                        }
                        renderdata = {}
                        renderdata['context'] = context
                        template = loader.get_template('resetPassword.html')
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
                    template = loader.get_template('resetPassword.html')
                    return HttpResponse(template.render(renderdata, request))
            else:
                return redirect('forgotPassword')
        else:
            return redirect('forgotPassword')
    else:
        return redirect('forgotPassword')


def bookinfo(request, id):
    if 'may_add_to_cart' in request.session:
        del request.session['may_add_to_cart']
    bookdata = Listings.objects.filter(id=id).values()
    # print(type(bookdata))
    if 'user_login' in request.session:

        name = users.objects.get(id=request.session['user_login']).firstname

        context = {
            "ishidden": "hidden",
            "isnothidden": "",
            "home_class": "inactive",
            "about_class": "inactive",
            "contact_class": "active",
            'id': id,
            "name": name,
        }
    else:
        context = {
            "ishidden": "",
            "isnothidden": "hidden",
            "home_class": "inactive",
            "about_class": "inactive",
            "contact_class": "active",
            'id': id,
        }
    renderdata = {
        "context": context,
        "bookdata": bookdata.values()[0],
    }
    request.session['may_add_to_cart'] = id
    template = loader.get_template('bookinfo.html')
    return HttpResponse(template.render(renderdata, request))
    return HttpResponse('<p>The id is {}</p>'.format(id))


def cart(request):
    if 'user_login' in request.session:
        if 'may_add_to_cart' in request.session:
            isAlrInCart = False
            userdata = users.objects.get(
                id=request.session['user_login']).cart
            print("users cart: ", userdata)
            if userdata == {}:
                current_cart = userdata
            else:
                current_cart = json.loads(userdata)
            for item in current_cart:
                if current_cart[item] == request.session['may_add_to_cart']:
                    isAlrInCart = True
            if not isAlrInCart:
                length = len(current_cart)+1
                all_keys = list(current_cart.keys())
                clashing = False
                for x in all_keys:
                    if length == int(x):
                        clashing = True
                count = 1
                if clashing:
                    for x in all_keys:
                        if not count == int(x):
                            length = count
                            break
                        else:
                            count = count + 1
                current_cart[length] = request.session['may_add_to_cart']
                data = users.objects.get(id=request.session['user_login'])
                data.cart = json.dumps(current_cart)
                data.save()
                print("users updated cart: ", data.cart)
                context = {
                    "ishidden": "hidden",
                    "isnothidden": "",
                    "error_message": "",
                }
            else:
                context = {
                    "ishidden": "hidden",
                    "isnothidden": "",
                    "error_message": "Item has already been added to cart",
                }
            del request.session['may_add_to_cart']
        elif request.method == "POST":
            if request.POST.get('addToCart_button'):
                cart_item = request.POST['addToCart_button']
                isAlrInCart = False
                userdata = users.objects.get(
                    id=request.session['user_login']).cart
                print("users cart: ", userdata)
                if userdata == {}:
                    current_cart = userdata
                else:
                    current_cart = json.loads(userdata)
                for item in current_cart:
                    if current_cart[item] == cart_item:
                        isAlrInCart = True
                if not isAlrInCart:
                    length = len(current_cart)+1
                    all_keys = list(current_cart.keys())
                    clashing = False
                    for x in all_keys:
                        if length == int(x):
                            clashing = True
                            count = 1
                    if clashing:
                        for x in all_keys:
                            if not count == int(x):
                                length = count
                                break
                            else:
                                count = count + 1
                    current_cart[length] = cart_item
                    data = users.objects.get(id=request.session['user_login'])
                    data.cart = json.dumps(current_cart)
                    data.save()
                    print("users updated cart:", data)
                    context = {
                        "ishidden": "hidden",
                        "isnothidden": "",
                        "error_message": "",
                    }
                else:
                    context = {
                        "ishidden": "hidden",
                        "isnothidden": "",
                        "error_message": "Item has already been added to cart",
                    }
            else:
                delete_item = request.POST['delete_button']
                userdata = users.objects.get(
                    id=request.session['user_login']).cart
                current_cart = json.loads(userdata)
                keys_with_value = [
                    key for key, value in current_cart.items() if value == delete_item]
                print("item to be deleted:", keys_with_value)
                context = {
                    "ishidden": "hidden",
                    "isnothidden": "",
                    "error_message": "",
                }
                print("deleting bookid:", current_cart[keys_with_value[0]])
                del current_cart[keys_with_value[0]]
                data = users.objects.get(id=request.session['user_login'])
                data.cart = json.dumps(current_cart)
                data.save()
                print(data)
        else:
            context = {
                "ishidden": "hidden",
                "isnothidden": "",
                "error_message": "",
            }
        if users.objects.get(id=request.session['user_login']).cart == {}:
            cart = users.objects.get(id=request.session['user_login']).cart
        else:
            cart = json.loads(users.objects.get(
                id=request.session['user_login']).cart)
        book_ids = list(cart.values())
        print("books in user's cart: ", book_ids)
        listings = Listings.objects.filter(id__in=book_ids)
        renderdata = {
            "context": context,
            "listings": listings,
            "userid": request.session['user_login']
        }
        renderdata['context'] = context
        template = loader.get_template('cart.html')
        return HttpResponse(template.render(renderdata, request))
    else:
        return redirect('login')


def checkout(request, userid):
    if 'user_login' in request.session:
        if request.session['user_login'] == userid:
            userdata = users.objects.get(id=userid)
            users_cart = json.loads(userdata.cart)
            book_ids = list(users_cart.values())
            listings = Listings.objects.filter(id__in=book_ids)
            total_price = 0
            for book in listings:
                total_price = total_price + book.price
            if total_price >= 50:
                shipping = 0
            else:
                shipping = 5
            tax = 0.08*total_price

            context = {
                "userdata": userdata,
                "listings": listings,
                "total_price": total_price,
                "tax": tax,
                "shipping": shipping,
                "total": total_price + shipping + tax,
                "userid": request.session['user_login'],
            }
            template = loader.get_template("checkout.html")
            return HttpResponse(template.render(context, request))
        else:
            return redirect('cart')
    else:
        return redirect('login')


def payment(request, userid):
    if 'user_login' in request.session:
        if request.session['user_login'] == userid:
            userdata = users.objects.get(id=userid)
            userdata = users.objects.get(id=userid)
            users_cart = json.loads(userdata.cart)
            book_ids = list(users_cart.values())
            listings = Listings.objects.filter(id__in=book_ids)
            total_price = 0
            for book in listings:
                total_price = total_price + book.price
            if total_price >= 50:
                shipping = 0
            else:
                shipping = 5
            total_price += shipping
            tax = 0.08*total_price
            total_price += tax

            context = {
                "total_price": total_price,
            }
            template = loader.get_template("payment.html")
            return HttpResponse(template.render(context, request))
        else:
            return redirect('cart')
    else:
        return redirect('login')
