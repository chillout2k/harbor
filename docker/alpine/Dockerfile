FROM alpine
ENV NAME harbor

RUN apk update && apk upgrade && \
 apk add python3 && \
 pip3 install flask-restful requests && \
 mkdir /harbor
ADD ./*.py /harbor/

# compose: ./harbor.py --config /config/harbor_config.json
CMD ["/harbor/harbor.py", "--config", "/config/harbor_config.json"]

