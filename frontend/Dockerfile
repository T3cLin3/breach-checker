FROM nginx:alpine
LABEL maintainer="bartosz hauff"
RUN apk add --no-cache nodejs npm && npm install -g htmlhint
COPY index.html style.css script.js /usr/share/nginx/html/
COPY nginx.conf /etc/nginx/conf.d/default.conf
RUN htmlhint /usr/share/nginx/html/index.html
EXPOSE 80