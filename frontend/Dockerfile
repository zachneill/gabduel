FROM node:20-alpine3.20 as build

WORKDIR /usr/local/app
COPY ./package.json /usr/local/app
RUN npm install -g @angular/cli
RUN npm install
COPY . .
RUN ng build --configuration=production


FROM nginx:alpine3.20
COPY --from=build /usr/local/app/dist/gabduel/browser /usr/share/nginx/html
EXPOSE 80
CMD ["nginx","-g","daemon off;"]
