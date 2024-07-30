FROM python:3.11
USER root

ENV PYTHONIOENCODING utf-8
WORKDIR /src

COPY ./src/requirements.txt ./

RUN apt-get update && apt-get install -y \
    wget \
    udev \
    && fc-cache -fv \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir -r requirements.txt

ENV FLASK_APP=config:create_app

COPY ./src /src

CMD ["python", "app.py"]