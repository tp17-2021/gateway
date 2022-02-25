FROM nginx:alpine

COPY ./web/conf.d /etc/nginx/conf.d
COPY ./statevector/gateway /usr/share/nginx/statevector/gateway

RUN chmod a+rw /usr/share/nginx/statevector/gateway

COPY ./statevector/config /usr/share/nginx/statevector/config

COPY ./statevector/temporary_key_location /usr/share/nginx/temporary_key_location
