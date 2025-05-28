FROM node:22-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

ARG VITE_BACKEND_URL=http://127.0.0.1:8000
ARG VITE_QUERY_PROFESSORS_URL=http://127.0.0.1:8000/get_professors

ENV VITE_BACKEND_URL=${VITE_BACKEND_URL}
ENV VITE_QUERY_PROFESSORS_URL=${VITE_QUERY_PROFESSORS_URL}

RUN npm run build

EXPOSE 4173

CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0"]