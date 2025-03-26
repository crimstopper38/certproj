from django.shortcuts import render
from django.http import HttpRequest
def homepage(request):
    return render(request, 'home.html')

def renewalpage(request):
    return render(request, 'renewal.html')

def districtpage(request):
    return render(request, 'district.html')

def addonpage(request):
    return render(request, 'addon.html')