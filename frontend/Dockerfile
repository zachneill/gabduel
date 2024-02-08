FROM node:20-alpine3.19 as build

WORKDIR /app
COPY ./package.json ./yarn.lock .yarnrc.yml ./
RUN yarn install
COPY . .
RUN yarn build


FROM nginx:alpine3.18
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx","-g","daemon off;"]