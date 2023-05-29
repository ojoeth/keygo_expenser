FROM docker.io/library/python
ADD *.py requirements.txt /app
ADD static /app/static
ADD templates /app/templates
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000",  "-w", "4", "wsgi:app"]
