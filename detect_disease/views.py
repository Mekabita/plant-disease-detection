# detect_disease/views.py

from django.shortcuts import render
from .forms import ImageUploadForm
import os
from django.core.files.storage import FileSystemStorage
from PIL import Image
from io import BytesIO
from pathlib import Path
import json
from detect_disease.prediction import predict
import numpy as np

def index(request):
    template_name = 'detect_disease/index.html'
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        # uploaded_image_url = fs.url('static/detect_disease/plant_image.jpg')
        if 'plant-image-upload' in request.POST:
            if form.is_valid():
                uploaded_image = request.FILES['image']
                if not uploaded_image:
                    return render(request, template_name, {'form': form, 'status': 'no-image', 'predict': 'false'})
                image = Image.open(BytesIO(uploaded_image.read()))
                image.convert('RGB')
                for file in os.listdir('detect_disease/static/detect_disease'):
                    os.remove('detect_disease/static/detect_disease/' + file)
                image.save('detect_disease/static/detect_disease/plant_image.jpg', 'JPEG', quality=100)
                return render(request, template_name, {'form': form, 'status': 'uploaded', 'predict': 'false'})
        elif 'plant-image-predict' in request.POST:
            image_file = Path('detect_disease/static/detect_disease/plant_image.jpg')
            if image_file.is_file():
                input_image = Image.open('detect_disease/static/detect_disease/plant_image.jpg')
            else:
                return render(request, template_name, {'form': form})

            input_image = np.array(input_image)
            predicted_class = predict(input_image) 
            print(predicted_class)
            return render(request, template_name, {'form': form, 'status': 'uploaded', 'predict': 'true', 'prediction': predicted_class})
    else:
        form = ImageUploadForm()

    return render(request, template_name, {'form': form})
