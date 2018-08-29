FROM nginx:1.14.0

ADD nginx.conf  /etc/nginx/nginx.conf
ADD index.html  /www/data/
ADD errors      /www/data/errors
ADD assets      /www/data/assets

CMD ["nginx", "-g", "daemon off;"]
