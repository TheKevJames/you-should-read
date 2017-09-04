FROM node:8.4.0

WORKDIR /src
COPY package.json .
RUN npm install && npm cache clean --force

COPY . .
RUN npm run build-prod

CMD ["npm", "run", "start-prod"]
