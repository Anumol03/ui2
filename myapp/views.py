from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from functools import wraps
import os

API_TOKEN = "jeztapitest403"

def token_required(f):
    @wraps(f)
    def decorator(request, *args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token or token != API_TOKEN:
            return JsonResponse({'message': 'Token is missing or invalid'}, status=401)
        return f(request, *args, **kwargs)
    return decorator

@csrf_exempt
@token_required
def upload_file(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        if not file:
            return HttpResponse('No file part', status=400)
        filename = os.path.join(settings.MEDIA_ROOT, file.name)
        with open(filename, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        return JsonResponse({'message': 'File uploaded successfully'}, status=200)

def uploaded_files(request):
    files = os.listdir(settings.MEDIA_ROOT)
    return render(request, 'uploaded_files.html', {'files': files})
if not os.path.exists(settings.MEDIA_ROOT):
    os.makedirs(settings.MEDIA_ROOT)
