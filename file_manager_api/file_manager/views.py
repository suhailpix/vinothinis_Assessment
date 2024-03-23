from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
import mimetypes
from django.contrib import messages
import os
import shutil


files = {}

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'txt', 'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']
        if allowed_file(uploaded_file.name):
            filename = uploaded_file.name
            fs = FileSystemStorage()
            if fs.exists(filename):
                fs.delete(filename)
            filename = fs.save(filename, uploaded_file)
            file_path = fs.url(filename)
            files[filename] = {
                "size": uploaded_file.size,
                "mime_type": uploaded_file.content_type,
                "version": 1
            }
            return render(request, 'upload.html', {"message": f"File uploaded successfully in {file_path}"})
        else:
            return render(request, 'upload.html', {"message": "File type not allowed"})
    return render(request, 'upload.html')

def list_files(request):
    if request.method == 'GET':
        files_info = []
        for filename in os.listdir(settings.MEDIA_ROOT):
            file_path = os.path.join(settings.MEDIA_ROOT, filename)
            if os.path.isfile(file_path):
                file_size = os.path.getsize(file_path)
                mime_type, _ = mimetypes.guess_type(file_path)
                files_info.append({
                    'name': filename,
                    'size': file_size,
                    'mime_type': mime_type
                })
        return JsonResponse({'files': files_info})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

def delete_files(request):
    if request.method == 'POST':
        files_to_delete = request.POST.getlist('selected_files[]')  
        
        file_directory = "/api_file_manager/file_manager_api/file_manager/uploads"
        trash_directory = "/api_file_manager/file_manager_api/file_manager/trash"

        for file_name in files_to_delete:
            file_path = os.path.join(file_directory, file_name)
            trash_file_path = os.path.join(trash_directory, file_name)
            try:
                shutil.move(file_path, trash_file_path)
            except FileNotFoundError:
                pass
        
        return render(request, 'upload.html', {"message": "Files moved to trash successfully"})
    else:
        return JsonResponse({'error': 'Invalid request method'})
    

def retrieve_files(request):
    trash_directory = "/api_file_manager/file_manager_api/file_manager/trash"

    files = os.listdir(trash_directory)

    file_list = []
    for file_name in files:
        file_size = os.path.getsize(os.path.join(trash_directory, file_name))
        file_list.append({
            'name': file_name,
            'size': file_size
        })

    return JsonResponse({'files': file_list})

def restore_files(request):
    if request.method == 'POST':
        files_to_restore = request.POST.getlist('selected_files[]')  
        print("files_to_restore", files_to_restore)

        trash_directory = "/api_file_manager/file_manager_api/file_manager/trash"
        target_directory = "/api_file_manager/file_manager_api/file_manager/uploads"

        for file_name in files_to_restore:
            trash_file_path = os.path.join(trash_directory, file_name)
            target_file_path = os.path.join(target_directory, file_name)
            try:
                shutil.move(trash_file_path, target_file_path)
            except FileNotFoundError:
                pass

        return render(request, 'upload.html', {"message": "Files restored successfully"})
    else:
        return JsonResponse({'error': 'Invalid request method'})
