FROM python:3-stretch
WORKDIR /app
COPY . /app
RUN pip install -U pip
RUN pip install -r requirements.txt
EXPOSE 8010
CMD ["python", "server.py"]