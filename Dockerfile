FROM python:3.4

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app
COPY aadsite/requirements.txt ./
RUN pip install -r requirements.txt
COPY aadsite/ .

RUN ["python", "manage.py", "migrate", "--run-syncdb"]

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]