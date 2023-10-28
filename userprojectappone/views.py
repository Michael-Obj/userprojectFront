from django.shortcuts import render, redirect
import requests
from django.contrib import messages
# from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def Home(request):
    return render(request, "index.html")

# def Home(request, user):
#     return render(request, "index.html", {"user": user})



def RegisterUserPage(request):
    return render(request, "register.html")



def RegisterUser(request):
    try: 
        user = {
            "username": request.POST["username"],
            "email": request.POST["email"],
            "password": request.POST["password"],
            "confirm_password":request.POST["confirm_password"],
            "first_name": request.POST["first_name"],
            "last_name": request.POST["last_name"]
        }
        
        registeruser = requests.post('http://127.0.0.1:8000/api/user/register', data=user)
        myregisteruser = registeruser.json()

        if myregisteruser["message"] == "Username taken":
            messages.error(request, 'Username taken')
            return redirect("registerforum")
        
        elif myregisteruser["message"] == "Email taken":
            messages.error(request, 'Email already exist')
            return redirect("registerforum")
        
        elif myregisteruser["message"] == "Unmatching password":
            messages.error(request, 'Unmatching password')
            return redirect("registerforum")
        
        else:
            return render(request, "login.html", {"registereduser": myregisteruser})

    except Exception as ex:
        print(ex)


def LoginUserPage(request):
    return render(request, "login.html")



def LoginUser(request):
    try:
        user = {
            "username": request.POST["username"],
            "password": request.POST["password"]
        }

        loginuser = requests.post('http://127.0.0.1:8000/api/user/login', data=user)
        myloginuser = loginuser.json()

        # if myloginuser["username"] and myloginuser["email"] is not None:
        #     return redirect("home")
        
        if myloginuser["message"] == "Incorrect details":
            messages.error(request, 'Incorrect username or password')
            return redirect("loginforum")
            
        else:
            # return redirect("home", user=myloginuser)
            return render(request, "index.html", {"loggeduser": myloginuser})

    except Exception as ex:
        print(ex)



def AdminDashboard(request):
    try:
        userdata = requests.get('http://127.0.0.1:8000/api/user/getall/')
        myuserdata = userdata.json()

        username = request.session['username'] 
        email = request.session['email'] 

        return render(request, "admin-dashboard.html", {"users": myuserdata, "username": username, "email": email})
    
    except Exception as ex:
        print(ex)



def RegisterAdminPage(request):
    return render(request, "admin-register.html")



def RegisterAdmin(request):
    try: 
        admin = {
            "username": request.POST["username"],
            "email": request.POST["email"],
            "password": request.POST["password"],
            "confirm_password":request.POST["confirm_password"],
            "first_name": request.POST["first_name"],
            "last_name": request.POST["last_name"]
        }
        
        registeradmin = requests.post('http://127.0.0.1:8000/api/admin/register', data=admin)
        myregisteradmin = registeradmin.json()

        if myregisteradmin["message"] == "Username taken":
            messages.error(request, 'Username taken')
            return redirect("registeradminforum")
        
        elif myregisteradmin["message"] == "Email taken":
            messages.error(request, 'Email already exist')
            return redirect("registeradminforum")
        
        elif myregisteradmin["message"] == "Unmatching password":
            messages.error(request, 'Unmatching password')
            return redirect("registeradminforum")
        
        else:
            return render(request, "admin-login.html", {"registeredadmin": myregisteradmin})

    except Exception as ex:
        print(ex)



def LoginAdminPage(request):
    return render(request, "admin-login.html")



def LoginAdmin(request):
    try:
        admin = {
            "username": request.POST["username"],
            "password": request.POST["password"]
        }
        
        loginadmin = requests.post('http://127.0.0.1:8000/api/admin/login', data=admin)
        userdata = requests.get('http://127.0.0.1:8000/api/user/getall/')
      
        myloginadmin = loginadmin.json()
        myuserdata = userdata.json()

        if myloginadmin["message"] == "Incorrect details":
            messages.error(request, 'Incorrect username or password')
            return redirect("loginadminforum")
            
        else:
            request.session['username'] = myloginadmin['data']['username']
            request.session['email'] = myloginadmin['data']['email']

            return render(request, "admin-dashboard.html", {"loggedadmin": myloginadmin, "users": myuserdata})

    except Exception as ex:
        print(ex)


# @csrf_exempt
def GetIdUser(request, id):
    try:
        # myName = request.session['name'] 

        getidusers = requests.get('http://127.0.0.1:8000/api/user/getid/' + id)

        mygetiduser = getidusers.json()
        return render(request, "update.html", {"getiduser": mygetiduser})
    
    except Exception as ex:
        print(ex)


   
def UpdateUser(request, id):
    try: 
        user = {
            "email": request.POST["email"],
            "first_name": request.POST["first_name"],
            "last_name": request.POST["last_name"]
        }
        
        # updateuser = requests.put('http://127.0.0.1:8000/api/user/update/' + id +'/', data=user)
        updateuser = requests.put(f'http://127.0.0.1:8000/api/user/update/{id}/', data=user)
        userdata = requests.get('http://127.0.0.1:8000/api/user/getall/')

        myupdateuser = updateuser.json()
        myuserdata = userdata.json()

        admin = {
            "id": 0,
            "username": "",
            "email": ""
        }

        for data in myuserdata:
            if data["is_superuser"] == True:
                admin["id"] = data["id"]
                admin["username"] = data["username"]
                admin["email"] = data["email"]
        
        if myupdateuser["message"] == "Email taken":
            messages.error(request, 'Email already exist')
            return render(request, "update.html")
        
        else:
            return render(request, "admin-dashboard.html", {"users": myuserdata, "admin": admin})

    except Exception as ex:
        print(ex)
        
    

def DeleteUser(request, id):
    try:
        deleteuser = requests.delete('http://127.0.0.1:8000/api/user/delete/' + id)
        mydeleteuser = deleteuser.json()

        if mydeleteuser["message"] == "User data deleted":
            messages.error(request, 'User data deleted')
            return redirect("admindashboard")
            
        else:
            return redirect("admindashboard")     
           
    except Exception as ex:
        print(ex)



# def LogoutUser(request):
#     try:
#         logoutuser = requests.get('http://127.0.0.1:8000/api/user/logout')
#         mylogoutuser = logoutuser.json()

#         if mylogoutuser["message"] == "Successfully logout":
#             return redirect('/') 
    
#     except Exception as ex:
#         print(ex)