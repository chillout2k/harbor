FROM alpine
ENV NAME harbor

RUN apk update && apk upgrade && \
 apk add python3 && \
 pip3 install flask-restful requests && \
 mkdir /harbor

COPY app/*.py /harbor/

CMD ["/harbor/harbor.py", "--config", "/config/harbor_config.json"]
