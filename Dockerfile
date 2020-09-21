FROM node:12

# Setting app directory
WORKDIR /

# Installing dependencies
COPY package*.json ./

RUN npm install
RUN npm install mysql

#Bundling Source
COPY . .

#Exposing port to run 
EXPOSE 4000

CMD [ "node", "server.js" ]