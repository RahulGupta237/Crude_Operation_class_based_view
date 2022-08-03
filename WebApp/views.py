from multiprocessing import context
from unicodedata import name
from django.http import HttpResponseRedirect
from django.shortcuts import render,HttpResponseRedirect
#from django.urls import is_valid_path
from WebApp.models import Student
from WebApp.forms import studentForm
from django.views.generic.base import TemplateView,RedirectView
from django.views import View

# Create your views here.

""" This is Crude operation Create Update and Delete with the help of Class based views in django"""

class StudentAddShowViews(TemplateView):
    """This class Create data and Read data"""
    template_name='CrudeApp/create_read.html'

    def get_context_data(self,*args,**kwargs):
        context= super().get_context_data(**kwargs)
        new=studentForm()
        
        retrieve_data=Student.objects.all()
        context={'forms':new,'data':retrieve_data}
        return context



    def post(self,request):
        new=studentForm(request.POST)
        retrieve_data=Student.objects.all()
        if new.is_valid():
            print("form validation")
            name=new.cleaned_data['name']
            email=new.cleaned_data['email']
            role=new.cleaned_data['role']
            db=Student(name=name,email=email,role=role)
            print(name,email,role)
            new.save()
        return HttpResponseRedirect('/')


class StudentDeleteViews(RedirectView):
    """This class delte the data"""
    url='/'
    def get_redirect_url(self, *args,**kwargs):
        print(kwargs)
        del_id=kwargs['id']
        Student.objects.get(pk=del_id).delete()
        return super().get_redirect_url(*args, **kwargs) # if not return is here page was not working


class UserUpdateViews(View):
    "this calss updated the data"
    def get(self,request,id):
        update_id=Student.objects.get(pk=id)
        new=studentForm(instance=update_id)
        return render(request,'CrudeApp/update.html',{"form":new})

    def post(self,request,id):
        update_id=Student.objects.get(pk=id)
        new=studentForm(request.POST,instance=update_id)
        if new.is_valid():
            print("SuccessFully Updated")
            new.save()
        return render(request,'CrudeApp/update.html',{"form":new})


