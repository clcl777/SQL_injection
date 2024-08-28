FROM python:3.11

ENV PYTHONIOENCODING utf-8
WORKDIR /src

COPY ./src/requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY ./src /src

CMD ["python", "app.py"]
