# imports
from django.urls import path
from myapp.views import FileUploadView, UploadedFilesView

urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('files/', UploadedFilesView.as_view(), name='uploaded-files'),
]
