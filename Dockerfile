FROM python:3.6.5-alpine3.7
EXPOSE 80

WORKDIR /usr/src/project

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["sh", "-c", "gunicorn -b '0.0.0.0:80' server:app"]