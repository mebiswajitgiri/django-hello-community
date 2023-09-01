from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from .forms import DemoForm
def demofeature(request):
    form = DemoForm()
    if request.method == "POST":
        form = DemoForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("added to database")
    return render(request,'demofeature.html', {'forms': form})