FROM python:3.8.5

# Setting app directory
WORKDIR /app

# Installing dependencies
COPY package*.json ./

RUN pip install mysql-connector
RUN pip install flask
RUN pip install flask-wtf
RUN pip install email_validator
RUN pip install bcrypt
RUN pip install flask-login



#Bundling Source
COPY . /app

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]