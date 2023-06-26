FROM nginx:1.13-alpine
COPY conf /etc/nginx/conf.d/default.conf

#COPY certs/cycon.site.crt /etc/nginx/cycon.site.crt
#COPY certs/cycon.site.key /etc/nginx/cycon.site.key

COPY /etc/pki/cycon/SAN-cycon.nkn.uidaho.edu.crt /etc/nginx/SAN-cycon.nkn.uidaho.edu.crt
COPY /etc/pki/cycon/SAN-cycon.nkn.uidaho.edu.key /etc/nginx/SAN-cycon.nkn.uidaho.edu.key

