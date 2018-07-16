FROM nginx:latest

ADD nginx.conf  /etc/nginx/nginx.conf
ADD index.html  /www/data/
ADD 404.html    /www/data/
ADD 50x.html    /www/data/
ADD assets      /www/data/assets
ADD favicon.ico /www/data/

CMD ["nginx", "-g", "daemon off;"]
