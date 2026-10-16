FROM nginx:alpine
LABEL maintainer="bartosz hauff"
RUN apk add --no-cache nodejs npm && npm install -g htmlhint
COPY . /usr/share/nginx/html
RUN htmlhint /usr/share/nginx/html/index.html
EXPOSE 80