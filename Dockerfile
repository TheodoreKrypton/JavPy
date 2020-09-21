FROM node:buster as build

COPY . /javpy

RUN cd /javpy && npm install --only=prod --unsafe-perm && npm install -g pkg && npm run build

FROM debian:buster-slim

COPY --from=build /javpy/build/javpy-linux .

CMD ["./javpy-linux"]
