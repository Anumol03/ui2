from django.core.files.storage import default_storage
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from functools import wraps
import os

# Mapping of API keys to usernames 'ApiKeyForUser3': 'user3',
API_KEYS = {
    'ApiKeyForUser1': 'user1',
    'ApiKeyForUser2': 'user2',
    'ApiKeyForUser3': 'user3',
    # Add more API keys and corresponding usernames as needed
}

def api_key_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        request = args[1]
        api_key = request.headers.get('X-API-KEY')
        if api_key not in API_KEYS:
            return Response({'message': 'Invalid API Key'}, status=status.HTTP_403_FORBIDDEN)
        request.user = API_KEYS[api_key]  # Add username to the request
        return f(*args, **kwargs)
    return decorated

class FileUploadView(APIView):

    @api_key_required
    def post(self, request, format=None):
        file = request.FILES.get('file')
        if not file:
            return Response({'message': 'No file part'}, status=status.HTTP_400_BAD_REQUEST)

        user_folder = os.path.join(settings.MEDIA_ROOT, request.user)
        os.makedirs(user_folder, exist_ok=True)
        filename = os.path.join(user_folder, file.name)

        with default_storage.open(filename, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        return Response({'message': 'File uploaded successfully'}, status=status.HTTP_200_OK)

class UploadedFilesView(APIView):

    @api_key_required
    def get(self, request, format=None):
        user_folder = os.path.join(settings.MEDIA_ROOT, request.user)
        if not os.path.exists(user_folder):
            return Response({'message': 'No files found'}, status=status.HTTP_404_NOT_FOUND)

        files = os.listdir(user_folder)
        return Response({'files': files}, status=status.HTTP_200_OK)

# Ensure the media root directory exists
if not os.path.exists(settings.MEDIA_ROOT):
    os.makedirs(settings.MEDIA_ROOT)
