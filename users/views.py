from django.shortcuts import render


#----------------------------------------------------------------------------------------------
def UserBasePage(request):
    username = request.session['username']
    return render(request, 'user/userbase.html',{'username':username})

#---------------------------------------------------------------------------------------------

def UserHomePage(request):
    username = request.session['username']
    return render(request, 'users/userhome.html',{"name":username})

#--------------------------------------------------------------------------------------------

def Task1(request):
    return render(request, 'users/task1.html')

#-----------------------------------------------------------------------------------------------

def Task2(request):
    return render(request, 'users/task2.html')

#-----------------------------------------------------------------------------------------------

def Task3(request):
    return render(request, 'users/task3.html')

#-----------------------------------------------------------------------------------------------