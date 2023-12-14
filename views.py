from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.core.mail import send_mail
from .models import MyUser, Product
import requests, datetime
from cs50 import SQL
from django.core.exceptions import ValidationError

db = SQL("sqlite:///products.db")


class Signup(UserCreationForm):
    #first_name = forms.CharField(max_length= 62, widget= forms.TextInput(attrs={'placeholder': 'First name', 'class': 'b'}))
    #last_name = forms.CharField(max_length= 62, widget= forms.TextInput(attrs={'placeholder': 'Last name', 'class': 'b'}))
    
    class Meta:
        model= MyUser
        fields = ["email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super(Signup, self).__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs['class'] = 'b'
        self.fields["password1"].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].widget.attrs['id'] = 'p1'
        self.fields["password2"].widget.attrs['class'] = 'b'
        self.fields["password2"].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].widget.attrs['id'] = 'p2'
        self.fields['email'].widget.attrs['class'] = 'b'
        self.fields["email"].widget.attrs['placeholder'] = 'Email Address'

    



def index(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, password= password, email= email)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect('home')
        else:
            return render(request, "wangdo/index.html", {'message': "Incorrect email or password"})
    return render(request, "wangdo/index.html")

@login_required(login_url='')
def home(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    return render(request, "wangdo/home.html")

@login_required(login_url='')
def log_out(request):
    logout(request)
    return render(request, "wangdo/index.html")

def signup(request):
    if request.method == "POST":
        form = Signup(request.POST)
        if form.is_valid():
            form.save()
            db.execute("CREATE TABLE ? (id INTEGER, data DATETIME, item TEXT, image IMAGE)", form.cleaned_data['email'])
    else:
        form = Signup()
    return render(request, "wangdo/signup.html", {'form': form})

def products(request):
    x = requests.get("https://fakestoreapi.com/products")

    for item in x.json():
        items = Product(
            title= item['title'],
            description= item['description'],
            price= item['price'],
            image= item['image'],
        )
        items.save()
    return render(request, "wangdo/products.html", {'items':Product.objects.all()})

def product(request, id):
    item = Product.objects.get(id= id)
    if request.method == "POST":
        if request.user.is_authenticated:
            user = request.user.email
            item = request.POST['item']
            image = request.POST['image']
            date = datetime.datetime.now()
            db.execute("INSERT INTO ? (data, item, image) VALUES (?,?,?)",user, date, item, image)

    return render(request, "wangdo/product.html", {'item': item})

def cart(request):
    user = ''
    if request.user.is_authenticated:
        user += request.user.email
    items = db.execute("SELECT item, image FROM ?", user)

    if request.method == "POST":
        item = request.POST['id']
        db.execute("DELETE FROM ? WHERE item = ?",user, item)
        return HttpResponseRedirect(reverse('cart'))
    return render(request,"wangdo/cart.html",{'items': items})
    