FROM python:3.10

WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY run.py .
COPY project.db .
COPY project project
ENV FLASK_APP=run.py

CMD gunicorn run:app -b 0.0.0.0:80
