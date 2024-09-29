FROM node:20-alpine3.19 as build

WORKDIR /app
COPY ./package.json ./
RUN npm install -g @angular/cli
RUN npm install
COPY . .
RUN ng build --configuration=production


FROM nginx:alpine3.18
COPY --from=build /app/dist/gabduel /usr/share/nginx/html
EXPOSE 80
CMD ["nginx","-g","daemon off;"]
