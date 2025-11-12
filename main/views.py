from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def homepage(request):
    return render(request, 'homepage.html')

def wish(request):
    return render(request, 'wish.html')

def yourperson(request):
    return render(request, 'yourperson.html')
