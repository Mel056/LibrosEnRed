FROM python:3.9
RUN mkdir /app && cd /app
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
COPY ./ /app
EXPOSE 5000
CMD ["python3", "app.py"]