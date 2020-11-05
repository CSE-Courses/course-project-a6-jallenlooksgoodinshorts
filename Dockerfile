FROM python:3.8.5

RUN pip install mysql
RUN pip install mysql-connector
RUN pip install flask==0.10.1
RUN pip install flask-wtf
RUN pip install email_validator
RUN pip install flask-bcrypt
RUN pip install bcrypt
RUN pip install flask-login
RUN pip install gunicorn
RUN pip install textblob==0.15.1
RUN python -m textblob.download_corpora

#Bundling Source
COPY . /app

# Setting app directory
WORKDIR /app

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]