from django.db import models
from django.contrib.auth.models import User


class PredictionHistory(models.Model):


    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    nitrogen = models.FloatField()

    phosphorus = models.FloatField()

    potassium = models.FloatField()

    temperature = models.FloatField()

    humidity = models.FloatField()

    ph = models.FloatField()

    rainfall = models.FloatField()

    prediction = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return self.prediction
    

class DiseaseHistory(models.Model):

    disease_name = models.CharField(max_length=100)

    confidence = models.CharField(max_length=20)

    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return self.disease_name