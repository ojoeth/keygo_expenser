FROM docker.io/library/python
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000",  "-w", "4", "wsgi:app"]
