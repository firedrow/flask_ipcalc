FROM python:3.10-alpine
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app.py /code/
COPY ./static /code/static/
COPY ./templates /code/templates/
CMD ["python", "/code/app.py"]