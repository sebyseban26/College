from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import Course,Student,Teacher
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
# Create your views here.
def course(request):
    return render(request,'course.html')

def add_course(request):
    if request.method == 'POST':
        course_name = request.POST['course']
        fees = request.POST['fee']
        crs = Course(coursename=course_name, fees=fees)
        crs.save()
        messages.success(request, "Course added successfully!")
        return redirect('course')
    
def student(request):
    crs=Course.objects.all()
    return render(request,'student.html',{'course':crs})

def add_student(request):
     if request.method=='POST':
        name=request.POST['name']
        address=request.POST['address']
        age=request.POST['age']
        date=request.POST['date']
        course=request.POST['c']
        crs=Course.objects.get(id=course)
        std=Student(studentname=name,address=address,age=age,joiningdate=date,course=crs)
        std.save()
        return redirect('student')

def show_student(request):
    std=Student.objects.all()
    return render(request,'show_student.html',{'student':std})

def edit(request, pk):
    std = Student.objects.get(id=pk)
    crs = Course.objects.all()

    if request.method == 'POST':
        std.studentname = request.POST['name']
        std.address = request.POST['address']
        std.age = request.POST['age']
        std.joiningdate = request.POST['date']
        course_id = request.POST['c']
        std.course = Course.objects.get(id=course_id)
        std.save()
        return redirect('show_student')

    return render(request, 'edit.html', {'student': std, 'course': crs})


def delete(request, pk):
    student =Student.objects.get(id=pk)
    student.delete()
    return redirect('show_student')

###### Teacher #######
def add_teacher(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        username = request.POST.get('username')
        address = request.POST.get('address')
        age = request.POST.get('age')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        cpassword = request.POST.get('confirm_password')
        course_id = request.POST.get('course')
        image = request.FILES.get('image')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'This email is already registered.')
            return redirect('signup_page')

        if Teacher.objects.filter(phone=phone).exists():
            messages.error(request, 'This phone number already exists.')
            return redirect('signup_page')
        
        if password == cpassword:
            if User.objects.filter(username=username).exists():
                messages.info(request,'This username already exists')
                return redirect('signup_page')
            else:
                user=User.objects.create_user(first_name=fname,last_name=lname,username=username,password=password,email=email)
                user.save()
                us=User.objects.get(id=user.id)
                cid=Course.objects.get(id=course_id)
                teacher=Teacher(age=age,address=address,phone=phone,image=image,course=cid,user=us)
                teacher.save()
        else:
            messages.info(request,'Password doesnot match')
            return redirect('signup_page') 
        messages.success(request, "Teacher registered successfully.")   
        return redirect('login_page')
    course = Course.objects.all()
    return render(request, 'signup_page.html', {'course': course})


# def add_teacher(request):
#     if request.method == 'POST':
#         fname = request.POST.get('fname')
#         lname = request.POST.get('lname')
#         username = request.POST.get('username')
#         address = request.POST.get('address')
#         age = request.POST.get('age')
#         email = request.POST.get('email')
#         phone = request.POST.get('phone')
#         password = request.POST.get('password')
#         confirm_password = request.POST.get('confirm_password')
#         course_id = request.POST.get('course')
#         image = request.FILES.get('image')
    #     if password == confirm_password:
    #         if User.objects.filter(username=username).exists():
    #             messages.info(request,'This username already exists')
    #             return redirect('signup_page')
    #         else:
    #             user=User.objects.create_user(first_name=fname,last_name=lname,username=username,password=password,email=email)
    #             user.save()
    #             us=User.objects.get(id=user.id)
    #             cid=Course.objects.get(id=course_id)
    #             teacher=Teacher(age=age,address=address,phone=phone,image=image,course=cid,user=us)
    #             teacher.save()
    #     else:
    #         messages.info(request,'Password doesnot match')
    #         return redirect('signup_page') 
    #     messages.success(request, "Teacher registered successfully.")   
    #     return redirect('login_page')
    # course = Course.objects.all()
    # return render(request, 'signup_page.html', {'course': course})


def show_teachers(request):
    teachers = Teacher.objects.all()
    return render(request, 'show_teachers.html', {'teachers': teachers})

def teacher_delete(request, pk):
    teacher =Teacher.objects.get(id=pk)
    teacher.delete()
    return redirect('show_teachers')

@login_required(login_url='login_page')
def admin_dashboard(request):
    return render(request,'Admin_dashboard.html')
        
def home(request):
    return render(request,'Home_dashboard.html')

def login_fun(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_authenticated:
                if user.is_staff:
                    login(request, user)
                    request.session['user'] = user.username
                    return redirect('Admin_dashboard')
                else:
                    login(request, user)
                    request.session['user'] = user.username
                    return redirect('teacher_dashboard')  
            
        else:
            messages.info(request, 'Invalid Username or Password')
            return redirect('login_page')
    return render(request, 'login_page.html')

@login_required(login_url='login_page')
def teacher_dashboard(request):
    if 'user' in request.session:
        return render(request, 'teacher_dashboard.html')



def profile_card(request):
    teacher = Teacher.objects.get(user=request.user)
    return render(request, 'profile_card.html', {'teacher': teacher})


def edit_teacher(request, pk):
    teacher = Teacher.objects.get(id=pk)
    course = Course.objects.all()

    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        username = request.POST.get('username')
        address = request.POST.get('address')
        age = request.POST.get('age')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        course_id = request.POST.get('course')
        image = request.FILES.get('image')

         # ✅ Check for duplicate email
        if User.objects.filter(email=email).exclude(id=teacher.user.id).exists():
            messages.error(request, 'This email is already registered.')
            return redirect('teacher_edit', pk=pk)

        # ✅ Check for duplicate phone
        if Teacher.objects.filter(phone=phone).exclude(id=teacher.id).exists():
            messages.error(request, 'This phone number already exists.')
            return redirect('teacher_edit', pk=pk)

        # ✅ Check for duplicate username
        if User.objects.filter(username=username).exclude(id=teacher.user.id).exists():
            messages.error(request, 'This username already exists.')
            return redirect('teacher_edit', pk=pk)
        
        user = teacher.user
        user.first_name = fname
        user.last_name = lname
        user.username = username
        user.email = email
        user.save()

        teacher.address = address
        teacher.age = age
        teacher.phone = phone
        if image:
            teacher.image = image
        teacher.course = Course.objects.get(id=course_id)
        teacher.save()

        messages.success(request, "Profile updated successfully!")
        return redirect('profile_card')

    return render(request, 'teacher_edit.html', {'teacher': teacher, 'course': course})

def logout_teacher(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login_page')