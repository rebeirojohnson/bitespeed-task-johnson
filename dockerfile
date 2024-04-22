FROM python:3.10.7

WORKDIR /.

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

ENV TZ="Asia/Kolkata"

RUN python manage.py migrate

ENTRYPOINT ["python"] 

CMD ["manage.py", "runserver", "0.0.0.0:8000"]
