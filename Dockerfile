FROM node:buster as build

COPY . /javscript

RUN cd /javscript && npm install --only=prod --unsafe-perm && npm install -g pkg && npm run build

FROM debian:buster-slim

COPY --from=build /javscript/build/javpy-linux .

CMD ["./javpy-linux"]
