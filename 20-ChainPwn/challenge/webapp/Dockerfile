FROM node:20-alpine
RUN apk add --no-cache python3 make g++
WORKDIR /app
COPY package.json .
RUN npm install --silent
COPY app.js .
EXPOSE 3000
CMD ["node","app.js"]
