FROM node:18

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm install

COPY . .

EXPOSE 5173
EXPOSE 9273

CMD ["npm", "run", "dev", "--", "--host"]