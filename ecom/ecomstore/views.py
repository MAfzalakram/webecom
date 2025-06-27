from django.contrib.auth import update_session_auth_hash  
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . models import Product, Catagory, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password 
from .forms import SignUpForm, UpdateForm, ChangePassword, UserInfoForm
from django import forms
from .utils import send_verification_email
from django.utils.http import urlsafe_base64_decode
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .tokens import email_verification_token
from rest_framework import generics
from .serializers import ProductSerializer, CatagorySerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

#Django rest framework

class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['catagory']
    permission_classes = [IsAuthenticated] 


class CatagoryListAPIView(generics.ListAPIView):
    queryset = Catagory.objects.all()
    serializer_class = CatagorySerializer

class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer



# Create your views here.
def catagoryPage(request, cat):
    try:
        catagory = Catagory.objects.get(name=cat)
        products = Product.objects.filter(catagory=catagory)
        return render(request, 'catagory.html',  {"products": products , "catagory": catagory})

    except: 
        messages.error(request, "Catagory doesn't exit")
        return redirect('home')

@login_required(login_url='login')
def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product' : product})

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def about(request):
    return render(request, 'about.html', {})

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            if hasattr(user, 'profile') and not user.profile.is_email_verified:
                messages.warning(request, "Your email is not verified. Please check your inbox.")
                return render(request, 'login.html', {})

            login(request, user)
            messages.success(request, "You have successfully logged in!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'login.html', {})




def logout_user(request):
    logout(request)
    messages.success(request, "You have successfully loged out !!!!")
    return redirect('home')



def verify_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_object_or_404(User, pk=uid)
    except:
        user = None

    if user and email_verification_token.check_token(user, token):
        user.profile.is_email_verified = True
        user.profile.save()
        messages.success(request, "Email verified successfully. You may now log in.")
        return redirect('login')
    else:
        messages.error(request, "Invalid or expired verification link.")
        return redirect('home')


def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()

            send_verification_email(request, user)

            messages.success(request, "Account created! Please check your email to verify before logging in.")
            return redirect("login")
        else:
            messages.error(request, "There was an error in the form. Please correct it.")
    else:
        form = SignUpForm()

    return render(request, 'register.html', {"form": form})

    


def updatePassword(request):
    if request.user.is_authenticated:
        currentuser = request.user  # already a User object

        if request.method == 'POST':
            form = ChangePassword(user=currentuser, data=request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, currentuser)  # Prevents logout after password change
                messages.success(request, "Password has been updated successfully.")
                return redirect('home')
            else:
                
                return render(request, "updatepassword.html", {"form": form})
        else:
            form = ChangePassword(user=currentuser)
        
        return render(request, "updatepassword.html", {"form": form})  

    else:
        messages.error(request, "You must be logged in to update your password.")
        return redirect('home')

def updateProfile(request):
    if request.user.is_authenticated:
        currentuser, created = Profile.objects.get_or_create(user=request.user)
        info_form = UserInfoForm(request.POST or None , instance=currentuser)
        if info_form.is_valid():
            info_form.save()
            messages.success(request, "Your info has been updated")
            return redirect('home')
        return render(request, "updateProfile.html", {'user_form':info_form})
    else:
        messages.success(request,"You must be login to update profile")
        return redirect('home')

def updateUser(request):
    
    if request.user.is_authenticated:
        currentuser = User.objects.get(id=request.user.id)
        user_form = UpdateForm(request.POST or None , instance=currentuser)
        if user_form.is_valid():
            user_form.save()
            login(request, currentuser)
            messages.success(request, "Profile has been updated sucessfully")
            return redirect('home')
        return render(request, "updateuser.html", {'user_form':user_form})
    else:
        messages.success(request,"You must be login to update profile")
        return redirect('home')
   

    
def catagoryList(request):
    catagories = Catagory.objects.all()
    return render(request, "catagoryList.html", {'catagories': catagories})