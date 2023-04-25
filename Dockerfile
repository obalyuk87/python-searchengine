FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt requirements.txt
RUN pip install gunicorn
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 80

CMD [ "gunicorn", "--bind", "0.0.0.0:80", "--timeout", "600", "server:app" ]