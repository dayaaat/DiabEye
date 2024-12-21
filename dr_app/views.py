from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from dr_app import process
import os

@csrf_exempt
def home(request):
    if request.method == 'GET':
        return render(request, 'home.html')

@csrf_exempt
def about(request):
    if request.method == 'GET':
        return render(request, 'about.html')

@csrf_exempt
def fonction(request):
    if request.method == 'GET':
        return render(request, 'fonction.html')

@csrf_exempt
def demo(request):
    if request.method == 'GET':
        return render(request, 'demo.html')

@csrf_exempt
def process_image(request):
    if request.method == 'POST':
        print("FILES:", request.FILES)  # Debugging
        uploaded_file = request.FILES.get('image')

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        temp_dir = os.path.join(BASE_DIR, 'dr_app', 'uploaded_images')

        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        temp_file_path = os.path.join(temp_dir, uploaded_file.name)

        with open(temp_file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        result = process.process_img(temp_file_path)

        return JsonResponse({
            'result': result[0],
            'accuracy': float(result[2]),
        })

    return JsonResponse({'error': 'Invalid request method'}, status=405)
