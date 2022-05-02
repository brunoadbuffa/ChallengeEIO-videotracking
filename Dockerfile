FROM python:3.8-slim-buster

RUN apt-get update && apt-get install build-essential -y
RUN apt-get install ffmpeg libsm6 libxext6  -y

WORKDIR /code
ENV PYTHONPATH /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /code

CMD ["/bin/bash"]
