FROM node:16.3.0-alpine as build
WORKDIR /app
COPY package.json /app/package.json
RUN npm install
COPY . /app
RUN npm run build

EXPOSE 80
CMD ["npm", "start"]
# production environment
# FROM nginx:1.16.0-alpine
# COPY --from=build /app/build /usr/share/nginx/html

# #from https://mherman.org/blog/dockerizing-a-react-app/
# RUN rm /etc/nginx/conf.d/default.conf
# COPY nginx.conf /etc/nginx/conf.d
# CMD ["nginx", "-g", "daemon off;"]
