from pathlib import Path

# import cv2

from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.conf import settings

from .forms import FileFieldForm
from .models import CarImage
# from .detectron_car_class import DetectronCarClass

# Create your views here.

class FileFieldView(FormView):
    form_class = FileFieldForm
    template_name = 'car_finder/home.html'
    success_url = reverse_lazy('result_review')
    # detector = DetectronCarClass()

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        file = request.FILES.getlist('file_field')[0]
        if form.is_valid():
            instance = CarImage(image=file, output_image=file)
            instance.save()
            # image = cv2.imread(str(instance.image.path))
            # image, number_of_cars = self.detector.detect(image=image)
            # cv2.imwrite(str(instance.output_image.path), image)
            # instance.number_of_cars = number_of_cars
            # instance.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        
class ResultReviewView(ListView):
    model = CarImage
    context_object_name = 'cars'
    template_name = 'car_finder/result_review.html'
    ordering = ['-created_at']
    