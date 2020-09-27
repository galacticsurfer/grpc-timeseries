FROM python:3-stretch
WORKDIR /app
COPY . /app
RUN pip install -U pip
RUN pip install -r requirements.txt
EXPOSE 8011
CMD ["flask", "run", "--host=0.0.0.0", "--port=8011"]