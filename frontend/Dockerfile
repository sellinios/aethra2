# Build stage
FROM node:14 AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install
COPY . .
RUN npm run build

# Production stage with NGINX HTTP/3 support
FROM nginx:mainline-alpine
COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
EXPOSE 443
CMD ["nginx", "-g", "daemon off;"]