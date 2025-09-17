from django.shortcuts import render, redirect, get_object_or_404
from main.forms import NewsForm
from main.models import News
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime
from django.urls import reverse 

'''HttpResponse: untuk mengirim response HTTP ke client
serializers: untuk mengkonversi data dari database ke format XML atau JSON
kita mengatur fungsi show_json atau show_xml supaya ketika
ada aplikasi/mesin lain dapat mengakses data kita. ini tuh kayak template 
yang disepakati secara bersama Seperti "bahasa standar" untuk pertukaran data antar aplikasi
Semua sistem sepakat: "kalau mau kirim data, pakai format XML ya"
'''

@login_required(login_url='/login')
def show_main(request):
    # Menampilkan semua data statis dan semua news yang ada
    news_list = News.objects.all()
    filter_type = request.GET.get("filter", "all")
    
    if filter_type == "all":
        news_list = News.objects.all()
    else:
        news_list = News.objects.filter(user=request.user)

    context = {
        'npm' : '2406397196',
        'name': 'Refki Septian',
        'class': 'PBP C',
        'news_list': news_list,  # ← Semua news dikirim ke template
        'last_login': request.COOKIES.get('last_login', 'Never'),

    }

    return render(request, "main.html", context)

def create_news(request):
    form = NewsForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_main') # pindah ke halaman main

    context = {'form': form}
    return render(request, "create_news.html", context)

@login_required(login_url='/login')
def show_news(request, id):
    news = get_object_or_404(News, pk=id)
    news.increment_views()

    context = {
        'news': news
    }

    return render(request, "news_detail.html", context)

def show_xml(request):
     news_list = News.objects.all()
     xml_data = serializers.serialize("xml", news_list) # serializers digunakan untuk translate objek model menjadi format lain seperti dalam fungsi ini adalah XML.
     return HttpResponse(xml_data, content_type="application/xml")
'''xml_data = isi paketnya
content_type = label "FRAGILE" atau "MAKANAN" di dus supaya browser dan aplikasi lain tau kalau ini xml data
HttpResponse = paket yang sudah dibungkus siap kirim'''

def show_xml_by_id(request, news_id):
   try:
       news_item = News.objects.filter(pk=news_id) # bedanya ini difilter berdasarkan id yang diminta user (bisa lebih dari satu data saja selama sesuai dengan filter)
       xml_data = serializers.serialize("xml", news_item)
       return HttpResponse(xml_data, content_type="application/xml")
   except News.DoesNotExist:
       return HttpResponse(status=404)

def show_json_by_id(request, news_id):
   try:
       news_item = News.objects.get(pk=news_id) # get untuk mengambil single data saja
       json_data = serializers.serialize("json", [news_item])
       return HttpResponse(json_data, content_type="application/json")
   except News.DoesNotExist:
       return HttpResponse(status=404)
   
def show_json(request):
    news_list = News.objects.all()
    json_data = serializers.serialize("json", news_list)
    return HttpResponse(json_data, content_type="application/json")

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
   if request.method == 'POST':
      form = AuthenticationForm(data=request.POST)

      if form.is_valid():
        user = form.get_user()
        login(request, user)
        response = HttpResponseRedirect(reverse("main:show_main"))
        response.set_cookie('last_login', str(datetime.datetime.now()))
        return response

   else:
      form = AuthenticationForm(request)
   context = {'form': form}
   return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

def create_news(request):
    form = NewsForm(request.POST or None)

    if form.is_valid() and request.method == 'POST':
        news_entry = form.save(commit = False)
        news_entry.user = request.user
        news_entry.save()
        return redirect('main:show_main')

    context = {
        'form': form
    }

    return render(request, "create_news.html", context)