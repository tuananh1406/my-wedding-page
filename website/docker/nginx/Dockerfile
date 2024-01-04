FROM nginx:1.21-alpine

RUN rm /etc/nginx/conf.d/default.conf
RUN mkdir -p /etc/ssl
COPY cert_new.pem /etc/ssl/cert.pem
COPY key_new.pem /etc/ssl/key.pem
COPY cloudflare.pem /etc/ssl/
COPY nginx.conf /etc/nginx/conf.d
