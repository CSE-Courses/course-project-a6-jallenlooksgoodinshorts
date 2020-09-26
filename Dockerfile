FROM python:3.8.5

# Setting app directory
WORKDIR /app

# Installing dependencies
COPY package*.json ./

RUN pip install mysql-connector
RUN pip install flask


#Bundling Source
COPY . /app

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]