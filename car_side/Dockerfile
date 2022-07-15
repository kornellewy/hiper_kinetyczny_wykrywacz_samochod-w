FROM python

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 1

RUN pip install --upgrade pip

COPY ./requirements.txt .

# RUN pip install torch torchvision torchaudio
# RUN pip install -U opencv-python
RUN pip install -r requirements.txt
RUN pip install --upgrade pip setuptools wheel
RUN pip install -U Cython
COPY . .
# RUN python -m pip install pycocotools
# RUN python -m pip install -e detectron2
EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "car_side.wsgi:application", "--timeout 3600","--worker-class=gthread"]