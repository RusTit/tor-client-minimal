FROM alpine:edge

RUN apk update \
 && apk upgrade \
 && apk add --no-cache tor lyrebird \
 && rm /var/cache/apk/*

EXPOSE 9150

ADD ./torrc /etc/tor/torrc

USER tor
CMD /usr/bin/tor -f /etc/tor/torrc
