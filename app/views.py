from django.shortcuts import render
from django.http import HttpResponse
from app.forms import FaceRecognitionform
from app.machinelearning import pipeline_model
from django.conf import settings 
from app.models import FaceRecognition
import os
# Create your views here.

def index(req):
    return render(req,'index.html') 

def police(req):
    form = FaceRecognitionform()
    if req.method == 'POST':
        form = FaceRecognitionform(req.POST or None, req.FILES or None)
        if form.is_valid():
            save = form.save(commit=True)
            
            # extract the image object from database
            primary_key = save.pk
            imgobj = FaceRecognition.objects.get(pk=primary_key)
            fileroot = str(imgobj.image)
            filepath = os.path.join(settings.MEDIA_ROOT,fileroot)
            results = pipeline_model(filepath)
            print(results)
            
            return render(req,'police.html',{'form':form,'upload':True,'results':results})
            
            
    return render(req,'police.html',{'form':form,'uplaod':False})





