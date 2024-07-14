# Stage 1: Build the application
FROM node:22.4 as build

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install

COPY . .
RUN npm run build

# Stage 2: Serve the application with Nginx
FROM nginx:1.27-alpine

COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

# Optionally copy ads.txt if it exists
COPY ads.txt /usr/share/nginx/html/ads.txt

EXPOSE 80
EXPOSE 443

CMD ["nginx", "-g", "daemon off;"]
