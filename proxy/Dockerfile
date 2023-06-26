FROM nginx:1.13-alpine
COPY conf /etc/nginx/conf.d/default.conf

COPY certs/SAN-cycon.nkn.uidaho.edu.crt /etc/nginx/SAN-cycon.nkn.uidaho.edu.crt
COPY certs/SAN-cycon.nkn.uidaho.edu.key /etc/nginx/SAN-cycon.nkn.uidaho.edu.key

