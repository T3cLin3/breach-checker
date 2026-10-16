FROM nginx:alpine
LABEL maintainer="bartosz hauff"
LABEL autor="Bartosz Hauff" data="16.10.2026"
RUN apk add --no-cache nodejs npm && npm install -g htmlhint
COPY . /usr/share/nginx/html
RUN date > /usr/share/nginx/html/build.txt
RUN htmlhint /usr/share/nginx/html/index.html
EXPOSE 80