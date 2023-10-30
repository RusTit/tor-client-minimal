FROM alpine:latest

RUN apk update \
 && apk upgrade \
 && apk add --no-cache tor \
 && apk add --no-cache lyrebird --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing \
 && rm /var/cache/apk/*

EXPOSE 9150

ADD ./torrc /etc/tor/torrc

USER tor
CMD /usr/bin/tor -f /etc/tor/torrc
