FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-alpine3.14

COPY requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY . /app

WORKDIR /app

RUN mkdir /tmp_multiproc

CMD ["uvicorn", "--host", "0.0.0.0", "player2:app"]