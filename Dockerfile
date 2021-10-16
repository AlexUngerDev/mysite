FROM python:3
ARG APPDIR='/opt'
WORKDIR $APPDIR
COPY . $APPDIR
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["python", "manage.py", "migrate"]
CMD ["uwsgi", "--http", ":8000", "--module", "mysite.wsgi"]

