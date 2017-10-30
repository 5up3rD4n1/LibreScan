FROM labexperimental/debian:jessie

MAINTAINER LabExperimental <librescan@gmail.com>

RUN useradd -r -u 1001 -g librescan librescan

RUN mkdir /app/socks

ADD ./ /home/librescan/librescan

WORKDIR /home/librescan/librescan

RUN pip3 install -r src/requirements.txt

WORKDIR src/

USER librescan

ENV LS_DEV_MODE=False

VOLUME /home/librescan/LibreScanProjects

VOLUME /home/librescan/.librescan

EXPOSE 8080

CMD ["python3", "main.py", "web"]
