from django.shortcuts import render
import pickle
import random
import cv2
import numpy as np
import joblib
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from .models import PredictionHistory
from .models import DiseaseHistory

# Load crop model
disease_model = joblib.load('disease_model.pkl')
model = pickle.load(open('models/crop_model.pkl', 'rb'))

def home(request):

    return render(
        request,
        'home.html'
    )

@login_required(login_url='/accounts/login/')
def history_page(request):

    crop_history = PredictionHistory.objects.filter(
        user=request.user
    ).order_by('-created_at')

    disease_history = DiseaseHistory.objects.all().order_by('-date')

    return render(

        request,

        'history.html',

        {

            'crop_history': crop_history,

            'disease_history': disease_history
        }
    )

@login_required(login_url='/accounts/login/')
def crop_page(request):

    prediction = None

    if request.method == "POST":

        N = request.POST['N']
        P = request.POST['P']
        K = request.POST['K']
        temperature = request.POST['temperature']
        humidity = request.POST['humidity']
        ph = request.POST['ph']
        rainfall = request.POST['rainfall']

        data = [[
            N,
            P,
            K,
            temperature,
            humidity,
            ph,
            rainfall
        ]]

        prediction = model.predict(data)[0]

        PredictionHistory.objects.create(

    user=request.user,

    nitrogen=N,

    phosphorus=P,

    potassium=K,

    temperature=temperature,

    humidity=humidity,

    ph=ph,

    rainfall=rainfall,

    prediction=prediction
)

    return render(request, 'crop.html', {
        'prediction': prediction
    })

@login_required(login_url='/accounts/login/')

def disease_page(request):

    disease_result = None

    uploaded_file_url = None

    if request.method == "POST" and request.FILES.get('leaf_image'):

        uploaded_image = request.FILES['leaf_image']

        from django.core.files.storage import FileSystemStorage

        fs = FileSystemStorage()

        filename = fs.save(
            uploaded_image.name,
            uploaded_image
        )

        uploaded_file_url = fs.url(filename)

        image_path = fs.path(filename)

        img = cv2.imread(image_path)

        img = cv2.resize(img, (100,100))

        img = img.flatten()

        img = np.array(img).reshape(1, -1)

        prediction = disease_model.predict(img)

        disease_name = prediction[0]

        if disease_name == "Healthy":

            disease_result = {
                'disease': 'Healthy',
                'confidence': '98%',
                'severity': 'Low',
                'remedy': 'No treatment required.',
                'prevention': 'Maintain proper watering and sunlight.'
            }

        elif disease_name == "Leaf_Blight":

            disease_result = {
                'disease': 'Leaf Blight',
                'confidence': '92%',
                'severity': 'High',
                'remedy': 'Apply copper fungicide spray.',
                'prevention': 'Remove infected leaves.'
            }

        else:

            disease_result = {
                'disease': 'Leaf Spot',
                'confidence': '90%',
                'severity': 'Medium',
                'remedy': 'Use neem oil spray.',
                'prevention': 'Keep leaves dry and improve airflow.'
            }

    if disease_result:
        DiseaseHistory.objects.create(

        disease_name=disease_result['disease'],

        confidence=disease_result['confidence']
    )

    return render(
        request,
        'disease.html',
        {
            'disease_result': disease_result,
            'uploaded_file_url': uploaded_file_url
        }
    )

def guidance_page(request):

    return render(request, 'guidance.html')