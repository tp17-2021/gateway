FROM nginx:alpine

COPY ./web/conf.d /etc/nginx/conf.d

COPY ./static-files/config /usr/share/nginx/static-config

COPY ./static-files/temporary_key_location /usr/share/nginx/temporary_key_location
