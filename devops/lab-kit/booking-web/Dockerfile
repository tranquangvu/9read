FROM nginxinc/nginx-unprivileged:1.27-alpine
COPY nginx.conf /etc/nginx/templates/default.conf.template
COPY index.html /usr/share/nginx/html/index.html
ENV API_UPSTREAM=http://booking-api:8080 NGINX_ENVSUBST_FILTER=API_UPSTREAM
EXPOSE 8080
