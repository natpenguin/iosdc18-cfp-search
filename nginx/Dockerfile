FROM nginx:latest

ADD nginx.conf /etc/nginx/nginx.conf
ADD index.html /www/data/

CMD ["nginx", "-g", "daemon off;"]
