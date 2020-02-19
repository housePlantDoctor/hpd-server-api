FROM python:3.6

EXPOSE 5000

WORKDIR /app

COPY downloads /app
COPY models /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY app.py /app
COPY Config.py /app
COPY ResNet.py /app

CMD python app.py
