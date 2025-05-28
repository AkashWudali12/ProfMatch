FROM node:22-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

ARG VITE_QUERY_PROFESSORS_URL_PROD=https://profmatch-production.up.railway.app/get_professors

ENV VITE_QUERY_PROFESSORS_URL_PROD=${VITE_QUERY_PROFESSORS_URL_PROD}

RUN npm run build

EXPOSE 4173

CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0"]