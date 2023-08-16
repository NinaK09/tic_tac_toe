FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

COPY requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY . /app

WORKDIR /app

RUN mkdir /tmp_multiproc

EXPOSE 8000

CMD ["uvicorn", "--host", "0.0.0.0", "judge:app"]