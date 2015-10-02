FROM debian:jessie
MAINTAINER Sebastian Ramirez "tiangolo@gmail.com"

ENV ECHOPRINT_PATH=/opt/echoprint

RUN echo "deb http://www.deb-multimedia.org stable main non-free" >> /etc/apt/sources.list && \
    apt-get update && \
    apt-get install --force-yes -y deb-multimedia-keyring && \
    apt-get update && \
    apt-get install -y ffmpeg make g++ libboost1.55-dev zlib1g-dev libtag1-dev

RUN apt-get install -y python-dev python-pip
RUN pip install flask

COPY ./ $ECHOPRINT_PATH/echoprint-codegen/

WORKDIR $ECHOPRINT_PATH/echoprint-codegen/src
RUN make && \
    ln -s $ECHOPRINT_PATH/echoprint-codegen/echoprint-codegen /usr/local/bin

EXPOSE 80

CMD ["python", "/opt/echoprint/echoprint-codegen/api/api.py"]